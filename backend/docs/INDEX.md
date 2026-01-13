# 📚 Quant-Crew Documentation Index

Welcome to the Quant-Crew AI Investment Research System documentation.

## 🎯 Core Documents

### [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md)
**Complete implementation roadmap and technical specifications**
- System architecture overview
- Development phases and timelines
- Technical stack details
- Project structure
- Cost estimates
- Success metrics

👉 Start here if you want to understand the overall system design and implementation strategy.

---

### [AGENTS_OVERVIEW.md](./AGENTS_OVERVIEW.md)
**Deep dive into AI agent architecture**
- 5 specialized agent roles and capabilities
- Agent collaboration workflow
- Input/output formats
- Communication protocols
- Configuration options
- Monitoring and troubleshooting

👉 Read this to understand how the AI agents work together to generate investment reports.

---

### [QUICKSTART.md](./QUICKSTART.md)
**Get up and running in 15 minutes**
- Installation steps
- Configuration guide
- Basic usage examples
- Testing procedures
- Scheduling setup
- Common troubleshooting

👉 Follow this guide to quickly deploy and test the system.

---

## 📖 Additional Resources

### Configuration Files

- **[app/config/stock_watchlist.yaml](../app/config/stock_watchlist.yaml)**: Define stocks to analyze
- **[app/config/agent_config.yaml](../app/config/agent_config.yaml)**: Agent behavior settings

### Code Structure

```
backend/
├── app/
│   ├── agents/          # AI agent implementations
│   ├── workflows/       # LangGraph orchestration
│   ├── tools/           # Data collection tools
│   ├── services/        # Business logic
│   ├── models/          # Database models
│   ├── schemas/         # API schemas
│   └── api/             # REST endpoints
├── config/              # Configuration files
├── docs/                # Documentation (you are here)
├── scripts/             # Utility scripts
└── tests/               # Test suites
```

---

## 🚦 Getting Started Path

### For Quick Demo
1. Read [QUICKSTART.md](./QUICKSTART.md) → Sections 1-2
2. Run basic usage examples
3. Generate first report

### For Development
1. Read [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) → Architecture section
2. Read [AGENTS_OVERVIEW.md](./AGENTS_OVERVIEW.md) → All sections
3. Review configuration files
4. Follow [QUICKSTART.md](./QUICKSTART.md) → Development section

### For Customization
1. Read [AGENTS_OVERVIEW.md](./AGENTS_OVERVIEW.md) → Configuration section
2. Edit `app/config/agent_config.yaml`
3. Edit `app/config/stock_watchlist.yaml`
4. Test changes with single stock analysis

---

## 🎓 Learning Resources

### Understanding the System

| Topic | Document | Section |
|-------|----------|---------|
| What is Quant-Crew? | IMPLEMENTATION_PLAN.md | Overview |
| How do agents work? | AGENTS_OVERVIEW.md | Agent Team |
| What technologies are used? | IMPLEMENTATION_PLAN.md | Technical Stack |
| How much does it cost? | IMPLEMENTATION_PLAN.md | Cost Estimation |

### Implementation Guides

| Task | Document | Section |
|------|----------|---------|
| Install and setup | QUICKSTART.md | Installation |
| Generate first report | QUICKSTART.md | Basic Usage |
| Schedule weekly reports | QUICKSTART.md | Scheduled Execution |
| Monitor performance | QUICKSTART.md | Monitoring & Debugging |

### Customization

| Goal | Document | Section |
|------|----------|---------|
| Add new stocks | QUICKSTART.md | Configuration |
| Adjust agent behavior | AGENTS_OVERVIEW.md | Configuration |
| Add custom indicators | IMPLEMENTATION_PLAN.md | Technical Stack |
| Create new agent | AGENTS_OVERVIEW.md | Development Guidelines |

---

## 🔧 API Reference

### REST Endpoints

#### Reports
- `POST /api/v1/reports/generate` - Generate new report
- `GET /api/v1/reports` - List reports
- `GET /api/v1/reports/{id}` - Get report details
- `GET /api/v1/reports/{id}/pdf` - Download PDF

#### Analysis
- `POST /api/v1/analysis/stock` - Analyze single stock
- `GET /api/v1/analysis/history/{symbol}` - Get analysis history

#### Configuration
- `GET /api/v1/config/watchlist` - Get stock watchlist
- `PUT /api/v1/config/watchlist` - Update watchlist

See http://localhost:8000/docs for interactive API documentation.

---

## 📊 System Components

### AI Agents (CrewAI)
| Agent | Role | Primary Function |
|-------|------|------------------|
| Market Intelligence Officer | Data Collector | Fetch prices, news, financials |
| Quantitative Strategist | Technical Analyst | Calculate indicators, signals |
| Sentiment Analyst | NLP Processor | Analyze news sentiment |
| Risk Compliance Officer | Quality Control | Challenge findings, identify risks |
| Chief Investment Officer | Synthesizer | Generate final recommendations |

**Details**: See [AGENTS_OVERVIEW.md](./AGENTS_OVERVIEW.md)

### Workflow Orchestration (LangGraph)
- State management across agent interactions
- Iterative refinement loops
- Human-in-the-loop review points
- Conditional routing based on risk assessment

**Details**: See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) → Tier 3

### Data Tools
| Tool | Purpose | Library |
|------|---------|---------|
| YahooFinanceTool | Stock data | yfinance |
| NewsScraperTool | News collection | Custom |
| TechnicalAnalyzerTool | TA indicators | TA-Lib |
| RiskAssessmentTool | Risk scoring | Custom |

**Details**: See [AGENTS_OVERVIEW.md](./AGENTS_OVERVIEW.md) → Tools

---

## 🐛 Troubleshooting

### Quick Fixes

| Issue | Solution | Reference |
|-------|----------|-----------|
| API key error | Set in .env | QUICKSTART.md → Environment Setup |
| TA-Lib install | brew/apt install | QUICKSTART.md → Troubleshooting |
| Agent timeout | Increase timeout | AGENTS_OVERVIEW.md → Troubleshooting |
| High costs | Use mini model | QUICKSTART.md → Troubleshooting |

### Debug Tools
- **LangSmith**: Agent execution traces at https://smith.langchain.com/
- **FastAPI Docs**: Test endpoints at http://localhost:8000/docs
- **Logs**: Check `logs/app.log` for detailed errors

---

## 📈 Development Roadmap

### Current Status: Phase 1 (MVP)
- ✅ Project structure created
- ✅ Configuration files defined
- ✅ Documentation complete
- 🚧 Agent implementation in progress

### Next Milestones
1. **Phase 1 Complete**: Basic 3-agent system working
2. **Phase 2**: Add sentiment + risk agents
3. **Phase 3**: PDF reports + automation
4. **Phase 4**: Demo + promotion

**Timeline**: See [IMPLEMENTATION_PLAN.md](./IMPLEMENTATION_PLAN.md) → Implementation Phases

---

## 🤝 Contributing

### Development Workflow
1. Read relevant documentation
2. Create feature branch
3. Implement changes
4. Write tests
5. Update documentation
6. Submit PR

### Code Standards
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for public APIs
- Add tests for new features
- Update docs when changing behavior

---

## 📞 Support

### Get Help
- **Documentation Issues**: Check this index for relevant docs
- **Technical Problems**: See QUICKSTART.md → Troubleshooting
- **Feature Requests**: Open GitHub issue
- **Questions**: Contact jason@aidatatools.com

### Community
- GitHub: [anthropics/quant-crew](https://github.com/anthropics/quant-crew)
- Blog: [AIDATATOOLS Substack](https://aidatatools.substack.com)

---

## 📄 License

[Add license information here]

---

## 🔗 External Links

### Technologies Used
- [CrewAI](https://docs.crewai.com/) - Multi-agent orchestration
- [LangGraph](https://langchain-ai.github.io/langgraph/) - Workflow management
- [LangSmith](https://smith.langchain.com/) - Observability
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Yahoo Finance](https://github.com/ranaroussi/yfinance) - Market data
- [TA-Lib](https://ta-lib.org/) - Technical analysis

### Learning Resources
- [Multi-Agent Systems](https://langchain-ai.github.io/langgraph/concepts/multi_agent/)
- [Agent Prompt Engineering](https://platform.openai.com/docs/guides/prompt-engineering)
- [Technical Analysis Basics](https://www.investopedia.com/technical-analysis-4689657)

---

**Last Updated**: 2026-01-14

**Version**: 1.0.0-alpha

**Maintainer**: jason@aidatatools.com
