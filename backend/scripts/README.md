# Backend Scripts

Utility scripts for database initialization, data fetching, and maintenance tasks.

## Available Scripts

### 1. init_db_and_fetch.py

**Purpose**: Initialize database and fetch initial ticker data

**What it does**:
- Runs database migrations (via Alembic)
- Fetches historical ticker data from Yahoo Finance
- Populates the database with stock data

**Usage**:
```bash
# Via Taskfile (recommended)
task db:init

# Direct execution
cd backend
uv run python scripts/init_db_and_fetch.py
```

**When to use**:
- First time setup after cloning the repository
- After dropping and recreating the database
- When you need to refresh all ticker data

---

### 2. fetch_ticker_data.py

**Purpose**: Fetch and update ticker data from Yahoo Finance

**What it does**:
- Fetches stock price data for configured tickers
- Updates the database with latest data
- Can be run incrementally (only fetches new data)

**Usage**:
```bash
# Via Taskfile (recommended)
task data:fetch

# Direct execution
cd backend
uv run python scripts/fetch_ticker_data.py
```

**When to use**:
- Daily/regular data updates
- After adding new tickers to watchlist
- Before generating reports

---

## Database Migration Scripts

### Run Migrations
```bash
task db:migrate
```
Applies all pending database migrations.

### Rollback Migration
```bash
task db:migrate:rollback
```
Rolls back the last applied migration.

### Create New Migration
```bash
task db:migrate:create -- "add user table"
```
Creates a new migration file with auto-detected changes.

---

## Taskfile Commands Reference

All scripts can be run via the Taskfile for convenience:

| Command | Description |
|---------|-------------|
| `task db:init` | Initialize database and fetch data |
| `task db:migrate` | Run database migrations |
| `task db:migrate:rollback` | Rollback last migration |
| `task db:migrate:create -- "message"` | Create new migration |
| `task data:fetch` | Fetch ticker data |
| `task test:backend` | Run tests |
| `task test:backend:cov` | Run tests with coverage |
| `task lint:backend` | Lint code |
| `task format:backend` | Format code |
| `task config:demo` | Demo configuration system |

---

## Creating New Scripts

### Best Practices

1. **Use absolute imports from app**
```python
from app.config import settings, config_loader
from app.models.ticker_history import TickerHistory
```

2. **Add proper error handling**
```python
try:
    # Your code
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
```

3. **Make scripts executable**
```bash
chmod +x scripts/your_script.py
```

4. **Add to Taskfile**
```yaml
script:name:
  desc: "Description of your script"
  deps: [setup:backend]
  dir: backend
  cmds:
    - uv run python scripts/your_script.py
```

5. **Document in this README**

---

## Example: Creating a Report Generation Script

```python
#!/usr/bin/env python3
"""
Generate weekly investment research report
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import config_loader
from app.workflows.research_workflow import ResearchWorkflow


def main():
    """Generate weekly report for all watchlist stocks."""
    print("🔄 Generating weekly report...")

    # Get stocks from watchlist
    symbols = config_loader.get_watchlist_symbols()
    print(f"📊 Analyzing {len(symbols)} stocks: {', '.join(symbols)}")

    # Run analysis
    workflow = ResearchWorkflow()
    report = workflow.run_weekly_analysis(stocks=symbols)

    print(f"✅ Report generated: {report['report_id']}")
    print(f"📄 PDF: {report['pdf_path']}")


if __name__ == "__main__":
    main()
```

Save as `scripts/generate_report.py` and add to Taskfile:

```yaml
report:generate:
  desc: "Generate weekly investment report"
  deps: [setup:backend]
  dir: backend
  cmds:
    - uv run python scripts/generate_report.py
```

---

## Scheduling Scripts

### Using Cron (Linux/Mac)

Add to crontab (`crontab -e`):
```bash
# Fetch data daily at 6 PM
0 18 * * * cd /path/to/backend && uv run python scripts/fetch_ticker_data.py

# Generate weekly report every Sunday at 8 PM
0 20 * * 0 cd /path/to/backend && uv run python scripts/generate_report.py
```

### Using Task Scheduler (Windows)

Create a batch file `run_script.bat`:
```batch
@echo off
cd C:\path\to\backend
uv run python scripts\fetch_ticker_data.py
```

Schedule via Task Scheduler GUI.

---

## Environment Variables

Scripts use the same `.env` file as the main application:

```bash
# .env
DATABASE_URL=postgresql://user:password@localhost:5432/quantcrew
OPENAI_API_KEY=sk-...
LANGCHAIN_TRACING_V2=true
```

Make sure `.env` is configured before running scripts.

---

## Troubleshooting

### "Module not found" Error
**Solution**: Ensure you're running from the backend directory or using `task` commands.

### Database Connection Error
**Solution**:
- Check `.env` has correct `DATABASE_URL`
- Ensure PostgreSQL is running
- Test connection: `psql $DATABASE_URL`

### Import Errors
**Solution**:
- Run `task setup:backend` to install dependencies
- Check `sys.path` manipulation in script

### Permission Denied
**Solution**:
```bash
chmod +x scripts/your_script.py
```

---

## Script Template

Use this template for new scripts:

```python
#!/usr/bin/env python3
"""
Brief description of what this script does.
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings, config_loader


def main(args):
    """Main script logic."""
    print("🔄 Starting script...")

    try:
        # Your code here
        pass

    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

    print("✅ Script completed successfully")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script description")
    parser.add_argument("--option", help="Option description")
    args = parser.parse_args()

    main(args)
```

---

## See Also

- [Configuration Guide](../app/config/README.md)
- [Quick Start Guide](../docs/QUICKSTART.md)
- [Implementation Plan](../docs/IMPLEMENTATION_PLAN.md)
