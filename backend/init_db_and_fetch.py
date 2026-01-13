#!/usr/bin/env python3
"""
Initialize database and fetch ticker data.

This script will:
1. Create all database tables
2. Fetch 1 year of historical data for configured tickers
3. Store the data in PostgreSQL
"""
import asyncio
import sys

import yfinance as yf
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.config import settings
from app.core.database import async_session_maker, engine
from app.models import TickerHistory
from app.core.database import Base


async def init_db() -> None:
    """Create all database tables."""
    print("Creating database tables...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✓ Database tables created successfully")


async def fetch_and_store_data(period: str = "1y") -> None:
    """Fetch and store ticker historical data."""
    tickers = settings.ticker_list
    print(f"\nFetching {period} of data for tickers: {', '.join(tickers)}")

    async with async_session_maker() as db:
        total_created = 0
        total_updated = 0

        for ticker_symbol in tickers:
            try:
                print(f"\n  Processing {ticker_symbol}...")

                # Fetch data from yfinance
                ticker = yf.Ticker(ticker_symbol)
                hist = ticker.history(period=period)

                if hist.empty:
                    print(f"    ✗ No data available for {ticker_symbol}")
                    continue

                records_for_ticker = 0

                # Process each row
                for date_idx, row in hist.iterrows():
                    trade_date = date_idx.date()

                    data = {
                        "ticker": ticker_symbol,
                        "date": trade_date,
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "volume": int(row["Volume"]),
                        "dividends": float(row.get("Dividends", 0)),
                        "stock_splits": float(row.get("Stock Splits", 0)),
                    }

                    # Upsert using PostgreSQL ON CONFLICT
                    stmt = insert(TickerHistory).values(**data)
                    stmt = stmt.on_conflict_do_update(
                        index_elements=["ticker", "date"],
                        set_={
                            "open": stmt.excluded.open,
                            "high": stmt.excluded.high,
                            "low": stmt.excluded.low,
                            "close": stmt.excluded.close,
                            "volume": stmt.excluded.volume,
                            "dividends": stmt.excluded.dividends,
                            "stock_splits": stmt.excluded.stock_splits,
                        },
                    )

                    await db.execute(stmt)
                    records_for_ticker += 1

                await db.commit()
                total_created += records_for_ticker
                print(f"    ✓ Stored {records_for_ticker} records for {ticker_symbol}")

            except Exception as e:
                await db.rollback()
                print(f"    ✗ Error processing {ticker_symbol}: {str(e)}")

        print(f"\n✓ Total records stored: {total_created}")

        # Show summary
        print("\n" + "=" * 60)
        print("DATABASE SUMMARY")
        print("=" * 60)

        for ticker_symbol in tickers:
            result = await db.execute(
                select(TickerHistory)
                .where(TickerHistory.ticker == ticker_symbol)
                .order_by(TickerHistory.date.desc())
                .limit(1)
            )
            latest = result.scalar_one_or_none()

            if latest:
                count_result = await db.execute(
                    select(TickerHistory).where(TickerHistory.ticker == ticker_symbol)
                )
                count = len(list(count_result.scalars().all()))
                print(f"{ticker_symbol:10} - {count:4} records (latest: {latest.date})")
            else:
                print(f"{ticker_symbol:10} - No data")


async def main() -> None:
    """Main entry point."""
    print("=" * 60)
    print("TICKER DATA INITIALIZATION")
    print("=" * 60)
    print(f"Database: {settings.DATABASE_URL.split('@')[-1]}")
    print(f"Tickers: {', '.join(settings.ticker_list)}")
    print("=" * 60)

    try:
        # Initialize database
        await init_db()

        # Fetch and store data
        await fetch_and_store_data(period="1y")

        print("\n✓ Initialization completed successfully!")
        return 0

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
