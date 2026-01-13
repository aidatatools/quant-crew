from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.schemas.ticker_history import (
    AvailableTickersResponse,
    TickerDataFetchRequest,
    TickerDataFetchResponse,
    TickerHistory,
)
from app.services.ticker_service import (
    fetch_and_store_ticker_data,
    get_available_tickers,
    get_ticker_history,
)

router = APIRouter()


@router.get("/", response_model=AvailableTickersResponse)
async def get_available_ticker_list(
    db: AsyncSession = Depends(deps.get_db),
) -> AvailableTickersResponse:
    """
    Get list of available tickers.

    Returns:
    - **configured_tickers**: Tickers configured in .env file
    - **tickers_in_database**: Tickers with data in database, including record counts and date ranges
    """
    result = await get_available_tickers(db)

    return AvailableTickersResponse(
        configured_tickers=result["configured_tickers"],
        tickers_in_database=result["tickers_in_database"],
    )


@router.post("/fetch", response_model=TickerDataFetchResponse)
async def fetch_ticker_data(
    request: TickerDataFetchRequest,
    db: AsyncSession = Depends(deps.get_db),
) -> TickerDataFetchResponse:
    """
    Fetch historical data for tickers from yfinance and store in database.

    - **tickers**: List of ticker symbols (optional, defaults to configured tickers)
    - **period**: Data period (1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max)
    """
    result = await fetch_and_store_ticker_data(
        db=db,
        tickers=request.tickers,
        period=request.period,
    )

    return TickerDataFetchResponse(
        success=result["success"],
        message=result["message"],
        records_created=result["records_created"],
        records_updated=result["records_updated"],
    )


@router.get("/{ticker}/history", response_model=list[TickerHistory])
async def get_ticker_data(
    ticker: str,
    start_date: datetime | None = Query(None, description="Start date for filtering"),
    end_date: datetime | None = Query(None, description="End date for filtering"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records"),
    db: AsyncSession = Depends(deps.get_db),
) -> list[TickerHistory]:
    """
    Get historical data for a specific ticker from the database.

    - **ticker**: Ticker symbol (e.g., "NVDA", "2330.TW")
    - **start_date**: Optional start date filter
    - **end_date**: Optional end date filter
    - **limit**: Maximum number of records to return (default: 100, max: 1000)
    """
    history = await get_ticker_history(
        db=db,
        ticker=ticker,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )

    if not history:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data found for ticker {ticker}",
        )

    return history
