# Ticker Data Setup Guide

This guide explains how to set up and use the ticker historical data system.

## Overview

The system fetches historical stock data from Yahoo Finance (using yfinance) and stores it in PostgreSQL. It includes:

- Database model for storing OHLCV data
- Service layer for fetching and storing data
- REST API endpoints for data access
- CLI scripts for easy data management

## Prerequisites

1. **Database**: PostgreSQL must be running and accessible
2. **Configuration**: Update [.env](.env) file with your settings:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
   TICKERS="2330.TW,TSM,NVDA,GOOG"
   ```

## Setup Instructions

### 1. Create the Database

First, ensure your PostgreSQL database exists. If not, create it:

```bash
# Connect to PostgreSQL
psql -h <host> -U <username> -c "CREATE DATABASE <dbname>;"
```

Using your current settings (from .env):
```bash
psql -h 192.168.50.150 -U quantcrew -c "CREATE DATABASE quntcrew;"
```

### 2. Install Dependencies

```bash
uv sync --extra dev
```

### 3. Initialize Database and Fetch Data (FRESH_INSTALL)

Run the initialization script to:
- Create all database tables
- Fetch 1 year of historical data for all configured tickers
- Store data in PostgreSQL

```bash
uv run python init_db_and_fetch.py
```

This will:
1. Create the `ticker_history` table
2. Fetch 1 year of historical data for: 2330.TW, TSM, NVDA, GOOG
3. Display a summary of stored records

**OR** Use Alembic migrations (alternative method):

```bash
# Run migrations to create tables
uv run alembic upgrade head

# Then fetch data
uv run python fetch_ticker_data.py
```

## Usage

### Fetching Data via CLI

The `fetch_ticker_data.py` script provides flexible data fetching:

```bash
# Fetch 1 year (default) for all configured tickers
uv run python fetch_ticker_data.py

# Fetch 5 years for all configured tickers
uv run python fetch_ticker_data.py 5y

# Fetch 1 month for specific tickers
uv run python fetch_ticker_data.py 1mo NVDA TSM

# Fetch max history for a specific ticker
uv run python fetch_ticker_data.py max 2330.TW
```

**Valid periods**: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max

### Fetching Data via API

Start the API server:

```bash
task run:backend
# OR
uv run uvicorn main:app --reload
```

Access the interactive API docs at: http://localhost:8000/docs

#### API Endpoints

1. **Fetch ticker data** (POST):
   ```bash
   curl -X POST "http://localhost:8000/api/v1/tickers/fetch" \
     -H "Content-Type: application/json" \
     -d '{
       "tickers": ["NVDA", "TSM"],
       "period": "1y"
     }'
   ```

2. **Get ticker history** (GET):
   ```bash
   # Get last 100 records for NVDA
   curl "http://localhost:8000/api/v1/tickers/NVDA/history"

   # Get specific date range
   curl "http://localhost:8000/api/v1/tickers/NVDA/history?start_date=2025-01-01&end_date=2025-12-31&limit=500"
   ```

## Database Schema

The `ticker_history` table stores:

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| ticker | String(20) | Ticker symbol |
| date | Date | Trading date |
| open | Numeric(20,6) | Opening price |
| high | Numeric(20,6) | Highest price |
| low | Numeric(20,6) | Lowest price |
| close | Numeric(20,6) | Closing price |
| volume | Integer | Trading volume |
| dividends | Numeric(20,6) | Dividend amount (if any) |
| stock_splits | Numeric(20,6) | Stock split ratio (if any) |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Indexes**:
- `ticker` (for fast ticker lookups)
- `date` (for date range queries)
- `(ticker, date)` UNIQUE (prevents duplicates)

## Configuration

Edit [.env](.env) to customize:

```env
# Tickers to track (comma-separated)
TICKERS="2330.TW,TSM,NVDA,GOOG,AAPL,MSFT"

# Database connection
DATABASE_URL=postgresql+asyncpg://user:password@host:port/dbname
DATABASE_SCHEMA="dev"  # or "prod"
```

## Files Created

### Models
- [app/models/ticker_history.py](app/models/ticker_history.py) - SQLAlchemy model

### Schemas
- [app/schemas/ticker_history.py](app/schemas/ticker_history.py) - Pydantic schemas

### Services
- [app/services/ticker_service.py](app/services/ticker_service.py) - Business logic

### API Endpoints
- [app/api/v1/endpoints/tickers.py](app/api/v1/endpoints/tickers.py) - REST API

### Migrations
- [alembic/versions/001_add_ticker_history_table.py](alembic/versions/001_add_ticker_history_table.py) - Database migration

### Scripts
- [init_db_and_fetch.py](init_db_and_fetch.py) - Fresh install script
- [fetch_ticker_data.py](fetch_ticker_data.py) - Data fetching script

## Troubleshooting

### Database Connection Error

```
asyncpg.exceptions.InvalidCatalogNameError: database "quntcrew" does not exist
```

**Solution**: Create the database first (see step 1)

### Module Not Found Error

```
ModuleNotFoundError: No module named 'greenlet'
```

**Solution**: Install dependencies
```bash
uv sync --extra dev
```

### No Data for Ticker

If a ticker returns no data, check:
1. Ticker symbol is correct (use Yahoo Finance format)
2. Ticker is actively traded
3. Network connection is working

## Example Usage Flow

```bash
# 1. First time setup
uv run python init_db_and_fetch.py

# 2. Daily updates (run via cron or scheduler)
uv run python fetch_ticker_data.py 1d

# 3. Backfill more history if needed
uv run python fetch_ticker_data.py 5y

# 4. Query data via API
curl "http://localhost:8000/api/v1/tickers/NVDA/history?limit=30"
```

## Next Steps

- Set up a cron job to fetch daily data automatically
- Add more tickers to the TICKERS configuration
- Create visualization dashboards using the API
- Implement technical indicators using the historical data
