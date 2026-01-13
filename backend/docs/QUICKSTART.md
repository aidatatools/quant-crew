# 🚀 Quick Start Guide

## Prerequisites

- Python 3.11+
- PostgreSQL (optional, for persistence)
- OpenAI API Key
- LangSmith API Key (optional, for monitoring)

## Installation

### 1. Install Dependencies

```bash
cd backend
uv sync
```

This will install:
- FastAPI
- CrewAI
- LangGraph
- LangChain
- yfinance
- pandas, numpy
- TA-Lib (technical analysis)

### 2. Environment Setup

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here

# LangSmith (Optional - for monitoring)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-your-key-here
LANGCHAIN_PROJECT=quant-research-warroom

# Database (Optional)
DATABASE_URL=postgresql://user:password@localhost/quantcrew

# Application
ENVIRONMENT=development
DEBUG=true
```

### 3. Database Setup (Optional)

If using PostgreSQL for persistence:

```bash
# Create database
createdb quantcrew

# Run migrations
uv run alembic upgrade head
```

## Running the Application

### Start the API Server

```bash
uv run uvicorn main:app --reload
```

The API will be available at: http://localhost:8000

### Access API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Basic Usage

### 1. Generate a Single Stock Analysis

#### Via API
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{
    "symbol": "2330.TW",
    "analysis_date": "2025-01-12"
  }'
```

#### Via Python Script
```python
from app.workflows.research_workflow import ResearchWorkflow

workflow = ResearchWorkflow()
result = workflow.analyze_stock("2330.TW")
print(result)
```

### 2. Generate Weekly Report

#### Via API
```bash
curl -X POST "http://localhost:8000/api/v1/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "report_type": "weekly",
    "stocks": ["2330.TW", "NVDA"]
  }'
```

#### Via CLI Script
```bash
cd backend
uv run python scripts/generate_report.py --stocks 2330.TW NVDA
```

### 3. View Generated Reports

```bash
# List all reports
curl http://localhost:8000/api/v1/reports

# Get specific report
curl http://localhost:8000/api/v1/reports/{report_id}

# Download PDF
curl http://localhost:8000/api/v1/reports/{report_id}/pdf -o report.pdf
```

## Configuration

### Modify Stock Watchlist

Edit `app/app/config/stock_watchlist.yaml`:

```yaml
stocks:
  taiwan:
    - symbol: "2330.TW"
      name: "TSMC"

  us:
    - symbol: "NVDA"
      name: "NVIDIA"
```

### Adjust Agent Behavior

Edit `app/app/config/agent_config.yaml`:

```yaml
agents:
  risk_officer:
    challenge_threshold: 0.7  # Lower = more strict
    max_revisions: 2

  quant_strategist:
    indicators:
      - MA5
      - MA20
      - RSI14
```

## Example Workflows

### Complete Analysis Pipeline

```python
from app.workflows.research_workflow import ResearchWorkflow
from app.services.report_service import ReportService

# 1. Run analysis
workflow = ResearchWorkflow()
analysis_results = workflow.run_weekly_analysis(
    stocks=["2330.TW", "NVDA", "AAPL"]
)

# 2. Generate report
report_service = ReportService()
report = report_service.create_report(
    analysis_results=analysis_results,
    format="pdf"
)

# 3. Distribute report
report_service.email_report(
    report_id=report.id,
    recipients=["jason@aidatatools.com"]
)
```

### Agent Interaction Example

```python
from app.agents import MarketIntelligenceAgent, QuantStrategistAgent

# Initialize agents
market_agent = MarketIntelligenceAgent()
quant_agent = QuantStrategistAgent()

# Market agent collects data
market_data = market_agent.collect_data("2330.TW")

# Quant agent analyzes
technical_analysis = quant_agent.analyze(market_data)

print(f"Signal: {technical_analysis['recommendation']}")
print(f"Entry: {technical_analysis['entry_point']}")
```

### Monitor with LangSmith

```python
from langsmith import Client
from langsmith.run_helpers import traceable

client = Client()

@traceable(name="Weekly Report Generation")
def generate_weekly_report(stocks):
    workflow = ResearchWorkflow()
    return workflow.run_weekly_analysis(stocks)

# This will be tracked in LangSmith dashboard
result = generate_weekly_report(["2330.TW", "NVDA"])
```

## Testing

### Run All Tests
```bash
uv run pytest
```

### Test Specific Agent
```bash
uv run pytest tests/test_agents/test_market_intelligence.py -v
```

### Test with Coverage
```bash
uv run pytest --cov=app --cov-report=html
```

### Integration Test
```bash
# Test full workflow
uv run pytest tests/integration/test_full_workflow.py
```

## Scheduled Execution

### Using APScheduler

Edit `scripts/scheduler.py`:

```python
from apscheduler.schedulers.blocking import BlockingScheduler
from app.workflows.research_workflow import ResearchWorkflow

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='sun', hour=18)
def weekly_report_job():
    """Run every Sunday at 6 PM"""
    workflow = ResearchWorkflow()
    workflow.run_weekly_analysis()

scheduler.start()
```

Run scheduler:
```bash
uv run python scripts/scheduler.py
```

### Using Cron (Production)

Add to crontab:
```bash
# Run every Sunday at 18:00
0 18 * * 0 cd /path/to/backend && /path/to/uv run python scripts/generate_report.py
```

## Monitoring & Debugging

### View LangSmith Traces

1. Go to https://smith.langchain.com/
2. Select project: `quant-research-warroom`
3. View individual agent executions and token usage

### Check Application Logs

```bash
tail -f logs/app.log
```

### Debug Agent Execution

Enable verbose logging in config:
```yaml
agents:
  market_intelligence:
    verbose: true  # See agent reasoning
```

### Cost Tracking

```python
from app.services.cost_tracker import CostTracker

tracker = CostTracker()
report_cost = tracker.get_report_cost(report_id)
monthly_cost = tracker.get_monthly_cost()

print(f"Report cost: ${report_cost:.2f}")
print(f"Monthly total: ${monthly_cost:.2f}")
```

## Troubleshooting

### Common Issues

#### 1. "OpenAI API Key not found"
**Solution**: Add `OPENAI_API_KEY` to `.env` file

#### 2. "TA-Lib not installed"
**Solution**:
```bash
# macOS
brew install ta-lib
uv sync

# Ubuntu
sudo apt-get install ta-lib
uv sync
```

#### 3. "Database connection failed"
**Solution**: Ensure PostgreSQL is running or disable DB features in config

#### 4. "Agent timeout"
**Solution**: Increase timeout in `app/config/agent_config.yaml`:
```yaml
workflow:
  timeout_seconds: 900  # 15 minutes
```

#### 5. "High API costs"
**Solution**:
- Use `gpt-4o-mini` for non-critical agents
- Enable caching
- Reduce `max_tokens`

### Getting Help

- Check [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) for architecture details
- Review [AGENTS_OVERVIEW.md](./AGENTS_OVERVIEW.md) for agent documentation
- Open an issue on GitHub
- Contact: jason@aidatatools.com

## Next Steps

1. **Customize Agents**: Modify agent prompts in `app/config/agent_config.yaml`
2. **Add Stocks**: Update `app/config/stock_watchlist.yaml`
3. **Schedule Reports**: Set up automated execution
4. **Monitor Performance**: Review LangSmith dashboards
5. **Iterate**: Refine agent behaviors based on report quality

## Development Roadmap

### Phase 1 (Current)
- ✅ Basic 3-agent system
- ✅ Yahoo Finance integration
- ✅ Technical analysis

### Phase 2 (In Progress)
- [ ] Sentiment analysis agent
- [ ] Risk officer agent
- [ ] Iterative refinement workflow

### Phase 3 (Planned)
- [ ] PDF report generation
- [ ] Email distribution
- [ ] Web dashboard

### Phase 4 (Future)
- [ ] Twitter sentiment integration
- [ ] Real-time alerts
- [ ] Portfolio optimization

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [CrewAI Docs](https://docs.crewai.com/)
- [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/tutorials/)
- [Yahoo Finance API](https://github.com/ranaroussi/yfinance)
- [TA-Lib Manual](https://ta-lib.org/)

---

**Ready to generate your first AI-powered investment report!** 🚀
