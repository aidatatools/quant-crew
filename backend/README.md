# 🎯 Quant-Crew Backend - AI Investment Research War Room

An AI-powered investment research system that generates comprehensive weekly intelligence reports using multi-agent collaboration (CrewAI + LangGraph).

## 🌟 What is Quant-Crew?

Quant-Crew simulates a professional investment research team with 5 specialized AI agents:
- **Market Intelligence Officer**: Data collection from Yahoo Finance & news sources
- **Quantitative Strategist**: Technical analysis (RSI, MACD, Bollinger Bands, etc.)
- **Sentiment Analyst**: News sentiment analysis and trend detection
- **Risk Compliance Officer**: Adversarial review and risk assessment
- **Chief Investment Officer**: Final synthesis and recommendations

The system uses **iterative refinement** where the Risk Officer can challenge findings and trigger re-analysis, ensuring high-quality investment insights.

## 📚 Documentation

**👉 [Start here: Documentation Index](docs/INDEX.md)**

### Quick Links
- 🚀 [Quick Start Guide](docs/QUICKSTART.md) - Get running in 15 minutes
- 🏗️ [Implementation Plan](docs/IMPLEMENTATION_PLAN.md) - Architecture & roadmap
- 🤖 [Agents Overview](docs/AGENTS_OVERVIEW.md) - Deep dive into AI agents

### Key Features

- **Multi-Agent System**: 5 specialized AI agents working in collaboration
- **Iterative Refinement**: Risk-based challenge and revision loops
- **Technical Analysis**: Built-in TA-Lib indicators (MA, RSI, MACD, etc.)
- **Sentiment Analysis**: News and market sentiment scoring
- **Automated Reports**: Weekly PDF reports with charts
- **LangSmith Integration**: Full observability and cost tracking
- **REST API**: FastAPI with async support
- **Modern Stack**: FastAPI, PostgreSQL, SQLAlchemy 2.0, managed with `uv`

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- PostgreSQL (optional, for data persistence)
- OpenAI API Key
- LangSmith API Key (optional, for monitoring)

### Installation

```bash
# 1. Install dependencies
cd backend
uv sync

# 2. Configure environment
cp .env.example .env
# Edit .env and add your API keys

# 3. Run the application
uv run uvicorn main:app --reload
```

Visit http://localhost:8000/docs for interactive API documentation.

**👉 For detailed setup instructions, see [QUICKSTART.md](docs/QUICKSTART.md)**

## 💡 Example Usage

### Generate Stock Analysis
```bash
curl -X POST "http://localhost:8000/api/v1/analysis/stock" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "2330.TW"}'
```

### Generate Weekly Report
```bash
curl -X POST "http://localhost:8000/api/v1/reports/generate" \
  -H "Content-Type: application/json" \
  -d '{"stocks": ["2330.TW", "NVDA", "AAPL"]}'
```

### Via Python
```python
from app.workflows.research_workflow import ResearchWorkflow

workflow = ResearchWorkflow()
result = workflow.analyze_stock("2330.TW")
print(result)
```

## 📊 Weekly Report Output

The system generates comprehensive reports including:
- **Executive Summary**: CIO's integrated analysis
- **Individual Stock Deep Dives**:
  - Market intelligence (price, volume, news)
  - Technical analysis (indicators, signals, entry/exit points)
  - Sentiment analysis (news sentiment, trending topics)
  - Risk assessment (identified risks, stress tests)
  - Investment rating and strategy
- **Market Focus**: Industry trends, upcoming events
- **Agent Statistics**: Token usage, execution metrics

**Example**: See [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) for sample report format.

## 🏗️ Architecture

```
User Request
     ↓
Market Intelligence Officer (data collection)
     ↓
[Parallel Analysis]
├─ Quantitative Strategist (technical)
├─ Sentiment Analyst (sentiment)
     ↓
Risk Compliance Officer (challenge & validate)
     ↓
[Decision: Pass or Revise?]
     ↓
Chief Investment Officer (synthesis)
     ↓
Final Report (PDF + Email)
```

**Details**: See [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) and [AGENTS_OVERVIEW.md](docs/AGENTS_OVERVIEW.md)

## 🛠️ Technology Stack

### AI/ML
- **CrewAI**: Multi-agent orchestration
- **LangGraph**: Workflow state management
- **LangChain**: LLM interactions
- **LangSmith**: Observability & tracing
- **OpenAI GPT-4o**: LLM backend

### Data & Analysis
- **yfinance**: Yahoo Finance API
- **TA-Lib**: Technical indicators
- **pandas/numpy**: Data processing

### Backend
- **FastAPI**: REST API framework
- **PostgreSQL**: Database
- **SQLAlchemy 2.0**: ORM
- **Alembic**: Migrations
- **Pydantic v2**: Validation

## 📁 Project Structure

```
backend/
├── app/
│   ├── agents/              # 🤖 AI agent implementations
│   │   ├── market_intelligence.py
│   │   ├── quant_strategist.py
│   │   ├── sentiment_analyst.py
│   │   ├── risk_officer.py
│   │   └── cio.py
│   ├── workflows/           # 🔄 LangGraph orchestration
│   │   └── research_workflow.py
│   ├── tools/               # 🛠️ Data collection tools
│   │   ├── yahoo_finance_tool.py
│   │   ├── news_scraper.py
│   │   ├── ta_analyzer.py
│   │   └── risk_assessment.py
│   ├── services/            # 💼 Business logic
│   │   ├── report_service.py
│   │   └── chart_service.py
│   ├── models/              # 🗄️ Database models
│   ├── schemas/             # 📋 API schemas
│   └── api/v1/endpoints/    # 🌐 REST endpoints
├── config/                  # ⚙️ Configuration
│   ├── stock_watchlist.yaml
│   └── agent_config.yaml
├── docs/                    # 📚 Documentation
│   ├── INDEX.md
│   ├── QUICKSTART.md
│   ├── IMPLEMENTATION_PLAN.md
│   └── AGENTS_OVERVIEW.md
├── outputs/                 # 📊 Generated reports
│   ├── weekly_reports/
│   └── charts/
└── scripts/                 # 🔧 Utility scripts
```

## ⚙️ Configuration

### Stock Watchlist
Edit [app/config/stock_watchlist.yaml](app/config/stock_watchlist.yaml):
```yaml
stocks:
  taiwan:
    - symbol: "2330.TW"
      name: "TSMC"
  us:
    - symbol: "NVDA"
      name: "NVIDIA"
```

### Agent Behavior
Edit [app/config/agent_config.yaml](app/config/agent_config.yaml):
```yaml
agents:
  risk_officer:
    challenge_threshold: 0.7  # Adjust strictness
    max_revisions: 2
```

**See [QUICKSTART.md](docs/QUICKSTART.md) for full configuration options.**

## Development

### Adding Dependencies

Add a new dependency:
```bash
cd backend
uv add <package-name>
```

Add a development dependency:
```bash
uv add --dev <package-name>
```

### Code Quality

Format code with Black:
```bash
uv run black app/
```

Lint code with Ruff:
```bash
uv run ruff check app/
```

Type checking with mypy:
```bash
uv run mypy app/
```

### Testing

Run tests:
```bash
uv run pytest
```

With coverage:
```bash
uv run pytest --cov=app --cov-report=html
```

### Database Migrations

Create a new migration:
```bash
uv run alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
uv run alembic upgrade head
```

Rollback migration:
```bash
uv run alembic downgrade -1
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── config.py            # Configuration settings
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py          # API dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py    # API v1 router
│   │       └── endpoints/
│   │           ├── __init__.py
│   │           ├── health.py
│   │           └── items.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── security.py      # Security utilities
│   │   └── database.py      # Database connection
│   ├── models/
│   │   ├── __init__.py
│   │   └── item.py          # SQLAlchemy models
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── item.py          # Pydantic schemas
│   └── services/
│       ├── __init__.py
│       └── item.py          # Business logic
├── alembic/
│   ├── versions/
│   ├── env.py
│   ├── script.py.mako
│   └── README
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── main.py                  # Application entry point
├── .env.example
├── .gitignore
├── alembic.ini
├── pyproject.toml
├── uv.lock                  # Generated by uv
└── README.md
```

## 🌐 API Endpoints

### Reports
- `POST /api/v1/reports/generate` - Generate weekly report
- `GET /api/v1/reports` - List all reports
- `GET /api/v1/reports/{id}` - Get report details
- `GET /api/v1/reports/{id}/pdf` - Download PDF

### Analysis
- `POST /api/v1/analysis/stock` - Analyze single stock
- `GET /api/v1/analysis/history/{symbol}` - Analysis history

### Ticker Data
- `GET /api/v1/tickers/{symbol}` - Get stock data
- `GET /api/v1/tickers/{symbol}/history` - Historical prices

### Health
- `GET /api/v1/health` - System health check

**Interactive docs**: http://localhost:8000/docs

## 📅 Automated Scheduling

Schedule weekly report generation:

```python
# scripts/scheduler.py
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()

@scheduler.scheduled_job('cron', day_of_week='sun', hour=18)
def weekly_report():
    workflow = ResearchWorkflow()
    workflow.run_weekly_analysis()

scheduler.start()
```

Run with: `uv run python scripts/scheduler.py`

**See [QUICKSTART.md](docs/QUICKSTART.md) → Scheduled Execution**

## 💰 Cost Estimation

**Per weekly report (10 stocks)**:
- Market Intelligence: ~$1.50
- Quant Analysis: ~$0.60
- Sentiment Analysis: ~$1.60
- Risk Review: ~$0.40
- CIO Synthesis: ~$0.10
- **Total: ~$4.20 USD**

Monthly (4 reports): ~$16.80

**Details**: See [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md) → Cost Estimation

## 🔍 Monitoring & Observability

### LangSmith Integration
All agent executions are traced in LangSmith:
- Token usage per agent
- Execution time
- Decision rationale
- Cost tracking

Configure in `.env`:
```bash
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=ls-your-key
LANGCHAIN_PROJECT=quant-research-warroom
```

Visit https://smith.langchain.com/ to view traces.

## 🧪 Testing

```bash
# Run all tests
uv run pytest

# Test specific agent
uv run pytest tests/test_agents/test_market_intelligence.py

# With coverage
uv run pytest --cov=app --cov-report=html
```

## 📈 Development Roadmap

### ✅ Phase 1: MVP (Current)
- Project structure
- Configuration setup
- Documentation

### 🚧 Phase 2: Core Agents (In Progress)
- Market Intelligence Officer
- Quantitative Strategist
- Basic workflow

### 📋 Phase 3: Full System (Planned)
- All 5 agents
- Iterative refinement
- PDF reports

### 🚀 Phase 4: Production (Future)
- Automated scheduling
- Email distribution
- Web dashboard

**Full roadmap**: [IMPLEMENTATION_PLAN.md](docs/IMPLEMENTATION_PLAN.md)

## 🤝 Contributing

1. Read the [documentation](docs/INDEX.md)
2. Create feature branch
3. Implement with tests
4. Update docs
5. Submit PR

## 📞 Support & Contact

- **Documentation**: [docs/INDEX.md](docs/INDEX.md)
- **Issues**: Open GitHub issue
- **Email**: jason@aidatatools.com
- **Blog**: [AIDATATOOLS Substack](https://aidatatools.substack.com)

## 🔗 Resources

- [CrewAI Docs](https://docs.crewai.com/)
- [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/)
- [LangSmith](https://smith.langchain.com/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Yahoo Finance API](https://github.com/ranaroussi/yfinance)

## 📄 License

[Add license here]

---

**Built with CrewAI, LangGraph, and FastAPI** | **Powered by OpenAI GPT-4o**
