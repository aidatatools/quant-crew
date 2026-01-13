# Configuration Directory

This directory contains YAML configuration files for the Quant-Crew AI Investment Research system.

## Files

### agent_config.yaml
Configuration for AI agents including:
- LLM settings (model, temperature, tokens)
- Individual agent configurations
- Workflow parameters
- Risk officer thresholds
- LangSmith tracing settings

### stock_watchlist.yaml
Stock symbols and report configuration:
- Taiwan stocks to analyze
- US stocks to analyze
- Report generation settings
- Analysis parameters

## Usage

### Loading Configuration in Code

```python
from app.config import settings, config_loader

# Access environment variables
print(settings.OPENAI_API_KEY)
print(settings.APP_NAME)

# Load YAML configurations
agent_config = config_loader.agent_config
stock_watchlist = config_loader.stock_watchlist

# Get specific settings
market_intel_config = config_loader.get_agent_settings("market_intelligence")
llm_settings = config_loader.get_llm_settings()

# Get all stock symbols
symbols = config_loader.get_watchlist_symbols()
print(symbols)  # ['2330.TW', 'NVDA', ...]
```

### Example: Initialize an Agent

```python
from app.config import config_loader
from crewai import Agent

# Load agent configuration
agent_config = config_loader.get_agent_settings("quant_strategist")
llm_config = config_loader.get_llm_settings()

# Create agent with loaded config
quant_agent = Agent(
    role=agent_config["role"],
    goal=agent_config["goal"],
    backstory=agent_config["backstory"],
    verbose=agent_config.get("verbose", True),
    max_iterations=agent_config.get("max_iterations", 3),
)
```

### Example: Generate Report for Watchlist

```python
from app.config import config_loader
from app.workflows.research_workflow import ResearchWorkflow

# Get all stocks from watchlist
symbols = config_loader.get_watchlist_symbols()

# Generate report
workflow = ResearchWorkflow()
report = workflow.run_weekly_analysis(stocks=symbols)
```

## Configuration Priority

1. **Environment Variables** (`.env` file)
   - Runtime settings like API keys, database URLs
   - Accessed via `settings` object

2. **YAML Files** (this directory)
   - Agent behavior and domain-specific configuration
   - Accessed via `config_loader` object

## Modifying Configuration

### To Change Stock Watchlist
Edit `stock_watchlist.yaml`:
```yaml
stocks:
  taiwan:
    - symbol: "2330.TW"
      name: "TSMC"
```

### To Adjust Agent Behavior
Edit `agent_config.yaml`:
```yaml
agents:
  risk_officer:
    challenge_threshold: 0.8  # Make more strict
```

### To Change LLM Settings
Either edit `.env`:
```bash
OPENAI_MODEL=gpt-4o-mini
OPENAI_TEMPERATURE=0.5
```

Or edit `agent_config.yaml`:
```yaml
llm:
  model: "gpt-4o-mini"
  temperature: 0.5
```

**Note**: Environment variables take precedence over YAML settings for LLM configuration.

## File Structure

```
backend/
├── .env                      # Environment variables (API keys, etc.)
└── app/
    ├── config.py             # Python config loader
    └── config/               # This directory
        ├── README.md         # This file
        ├── agent_config.yaml # Agent settings
        └── stock_watchlist.yaml # Stock symbols
```

## Best Practices

1. **API Keys**: Always use `.env` file, never commit to git
2. **Agent Behavior**: Use YAML files for easy modification
3. **Stock Lists**: Use YAML for better readability
4. **Caching**: Config is cached after first load for performance

## See Also

- [Main Configuration Documentation](../../docs/QUICKSTART.md#configuration)
- [Agent Overview](../../docs/AGENTS_OVERVIEW.md)
- [Implementation Plan](../../docs/IMPLEMENTATION_PLAN.md)
