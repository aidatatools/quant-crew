from datetime import date, datetime

from sqlalchemy import Date, DateTime, Float, Index, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.core.database import Base


class TickerHistory(Base):
    __tablename__ = "ticker_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ticker: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    date: Mapped[date] = mapped_column(Date, nullable=False, index=True)

    # OHLCV data
    open: Mapped[float] = mapped_column(Numeric(precision=20, scale=6), nullable=False)
    high: Mapped[float] = mapped_column(Numeric(precision=20, scale=6), nullable=False)
    low: Mapped[float] = mapped_column(Numeric(precision=20, scale=6), nullable=False)
    close: Mapped[float] = mapped_column(Numeric(precision=20, scale=6), nullable=False)
    volume: Mapped[int] = mapped_column(Integer, nullable=False)

    # Optional fields
    dividends: Mapped[float | None] = mapped_column(
        Numeric(precision=20, scale=6), nullable=True, default=0
    )
    stock_splits: Mapped[float | None] = mapped_column(
        Numeric(precision=20, scale=6), nullable=True, default=0
    )

    # Metadata
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        Index("idx_ticker_date", "ticker", "date", unique=True),
    )
