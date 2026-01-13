from datetime import datetime
from typing import Any

import yfinance as yf
from sqlalchemy import func, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.ticker_history import TickerHistory


async def fetch_and_store_ticker_data(
    db: AsyncSession,
    tickers: list[str] | None = None,
    period: str = "1y",
) -> dict[str, Any]:
    """
    Fetch ticker historical data from yfinance and store in database.

    Args:
        db: Database session
        tickers: List of ticker symbols (defaults to settings.TICKERS)
        period: Data period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)

    Returns:
        Dictionary with operation results
    """
    if tickers is None:
        tickers = settings.ticker_list

    records_created = 0
    records_updated = 0
    errors = []

    for ticker_symbol in tickers:
        try:
            # Fetch data from yfinance
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period=period)

            if hist.empty:
                errors.append(f"{ticker_symbol}: No data available")
                continue

            # Process each row of historical data
            for date_idx, row in hist.iterrows():
                # Convert pandas Timestamp to date
                trade_date = date_idx.date()

                # Prepare data for upsert
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
                    "updated_at": datetime.utcnow(),
                }

                # Use PostgreSQL upsert (ON CONFLICT DO UPDATE)
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
                        "updated_at": stmt.excluded.updated_at,
                    },
                )

                result = await db.execute(stmt)

                # Check if it was an insert or update
                if result.rowcount > 0:
                    # Check if the record existed before
                    check_stmt = select(TickerHistory).where(
                        TickerHistory.ticker == ticker_symbol,
                        TickerHistory.date == trade_date,
                    )
                    existing = await db.execute(check_stmt)
                    if existing.scalar_one_or_none():
                        records_updated += 1
                    else:
                        records_created += 1

            await db.commit()

        except Exception as e:
            await db.rollback()
            errors.append(f"{ticker_symbol}: {str(e)}")

    success = len(errors) == 0
    message = "Data fetched successfully"
    if errors:
        message = f"Completed with {len(errors)} error(s): {'; '.join(errors)}"

    return {
        "success": success,
        "message": message,
        "records_created": records_created,
        "records_updated": records_updated,
        "tickers_processed": len(tickers) - len(errors),
        "errors": errors,
    }


async def get_ticker_history(
    db: AsyncSession,
    ticker: str,
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    limit: int = 100,
) -> list[TickerHistory]:
    """
    Retrieve ticker historical data from database.

    Args:
        db: Database session
        ticker: Ticker symbol
        start_date: Optional start date filter
        end_date: Optional end date filter
        limit: Maximum number of records to return

    Returns:
        List of TickerHistory records
    """
    query = select(TickerHistory).where(TickerHistory.ticker == ticker)

    if start_date:
        query = query.where(TickerHistory.date >= start_date.date())
    if end_date:
        query = query.where(TickerHistory.date <= end_date.date())

    query = query.order_by(TickerHistory.date.desc()).limit(limit)

    result = await db.execute(query)
    return list(result.scalars().all())


async def get_available_tickers(db: AsyncSession) -> dict[str, Any]:
    """
    Get list of available tickers from configuration and database.

    Args:
        db: Database session

    Returns:
        Dictionary with configured tickers and database ticker info
    """
    # Get configured tickers from settings
    configured_tickers = settings.ticker_list

    # Get unique tickers from database with stats
    query = (
        select(
            TickerHistory.ticker,
            func.count(TickerHistory.id).label("record_count"),
            func.min(TickerHistory.date).label("earliest_date"),
            func.max(TickerHistory.date).label("latest_date"),
        )
        .group_by(TickerHistory.ticker)
        .order_by(TickerHistory.ticker)
    )

    result = await db.execute(query)
    tickers_in_db = []

    for row in result:
        tickers_in_db.append(
            {
                "ticker": row.ticker,
                "record_count": row.record_count,
                "earliest_date": row.earliest_date,
                "latest_date": row.latest_date,
            }
        )

    return {
        "configured_tickers": configured_tickers,
        "tickers_in_database": tickers_in_db,
    }
