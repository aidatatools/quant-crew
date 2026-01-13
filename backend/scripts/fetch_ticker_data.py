#!/usr/bin/env python3
"""
Fetch and update ticker data.

Usage:
    python fetch_ticker_data.py              # Fetch 1 year for all configured tickers
    python fetch_ticker_data.py 5y           # Fetch 5 years for all configured tickers
    python fetch_ticker_data.py 1mo NVDA TSM # Fetch 1 month for specific tickers
"""
import asyncio
import sys

from app.core.database import async_session_maker
from app.services.ticker_service import fetch_and_store_ticker_data
from app.config import settings


async def main() -> int:
    """Main entry point."""
    # Parse arguments
    args = sys.argv[1:]

    period = "1y"
    tickers = None

    # Check if first arg is a period
    valid_periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "ytd", "max"]

    if args and args[0] in valid_periods:
        period = args[0]
        if len(args) > 1:
            tickers = args[1:]
    elif args:
        tickers = args

    # Show what we're doing
    print("=" * 60)
    print("FETCH TICKER DATA")
    print("=" * 60)
    print(f"Period: {period}")
    print(f"Tickers: {', '.join(tickers) if tickers else ', '.join(settings.ticker_list)}")
    print("=" * 60)

    try:
        async with async_session_maker() as db:
            result = await fetch_and_store_ticker_data(
                db=db,
                tickers=tickers,
                period=period,
            )

            print(f"\n{result['message']}")
            print(f"  Records created: {result['records_created']}")
            print(f"  Records updated: {result['records_updated']}")
            print(f"  Tickers processed: {result['tickers_processed']}")

            if result['errors']:
                print("\nErrors:")
                for error in result['errors']:
                    print(f"  ✗ {error}")

            if result['success']:
                print("\n✓ Data fetch completed successfully!")
                return 0
            else:
                print("\n⚠ Data fetch completed with errors")
                return 1

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
