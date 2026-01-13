from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class TickerHistoryBase(BaseModel):
    ticker: str
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int
    dividends: float | None = 0.0
    stock_splits: float | None = 0.0


class TickerHistoryCreate(TickerHistoryBase):
    pass


class TickerHistory(TickerHistoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime


class TickerDataFetchRequest(BaseModel):
    tickers: list[str] | None = None
    period: str = "1y"


class TickerDataFetchResponse(BaseModel):
    success: bool
    message: str
    records_created: int
    records_updated: int


class TickerInfo(BaseModel):
    ticker: str
    record_count: int
    earliest_date: date | None = None
    latest_date: date | None = None


class AvailableTickersResponse(BaseModel):
    configured_tickers: list[str]
    tickers_in_database: list[TickerInfo]
