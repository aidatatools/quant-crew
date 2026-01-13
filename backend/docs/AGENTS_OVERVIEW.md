# 🤖 AI Agents Overview

## System Architecture

The Quant-Crew system uses a team of 5 specialized AI agents orchestrated by CrewAI and LangGraph to generate comprehensive investment research reports.

## Agent Team

### 1. Market Intelligence Officer 📊

**Primary Responsibility**: Data collection and market monitoring

**Capabilities**:
- Fetch real-time stock prices from Yahoo Finance
- Collect financial statements and company metrics
- Scrape financial news from multiple sources
- Extract key data points from earnings reports
- Monitor volume and price changes

**Tools**:
- `YahooFinanceTool`: Stock data retrieval
- `NewsScraperTool`: News aggregation

**Output Format**:
```json
{
  "symbol": "2330.TW",
  "current_price": 1080.0,
  "price_change": 2.86,
  "volume": 125000000,
  "market_cap": "28T TWD",
  "news_summary": [
    {
      "date": "2025-01-08",
      "headline": "TSMC announces 3nm capacity increase",
      "sentiment": "positive"
    }
  ]
}
```

**Agent Prompt Example**:
```
Analyze TSMC (2330.TW) for the week of Jan 6-12, 2025.
Collect:
1. Daily price and volume data
2. Key news headlines
3. Company announcements
4. Peer comparison data
```

---

### 2. Quantitative Strategist 📈

**Primary Responsibility**: Technical analysis and signal generation

**Capabilities**:
- Calculate moving averages (MA5, MA20, MA60)
- Compute RSI, MACD, Bollinger Bands
- Identify trend patterns (support/resistance)
- Generate buy/sell signals
- Backtest strategies

**Tools**:
- `TechnicalAnalyzerTool`: TA-Lib integration
- `BacktestTool`: Historical strategy testing

**Output Format**:
```json
{
  "symbol": "2330.TW",
  "indicators": {
    "MA5": 1065,
    "MA20": 1050,
    "RSI14": 68,
    "MACD": {"signal": "bullish", "value": 12.5},
    "BOLLINGER": {"upper": 1090, "middle": 1070, "lower": 1050}
  },
  "signals": [
    {"type": "MA_CROSSOVER", "direction": "bullish"},
    {"type": "MACD_GOLDEN_CROSS", "confidence": 0.85}
  ],
  "recommendation": "BUY",
  "entry_point": 1085,
  "stop_loss": 1020
}
```

**Agent Prompt Example**:
```
Perform technical analysis on TSMC (2330.TW).
Calculate all configured indicators and provide:
1. Current indicator values
2. Signal interpretations
3. Entry/exit recommendations
4. Risk management levels
```

---

### 3. Sentiment Analyst 😊

**Primary Responsibility**: Market sentiment analysis

**Capabilities**:
- Analyze news article sentiment
- Extract trending keywords
- Calculate sentiment scores (-1 to +1)
- Identify market narrative shifts
- Track social media mentions (future)

**Tools**:
- `NewsSentimentTool`: NLP sentiment analysis
- `TextAnalyzerTool`: Keyword extraction

**Output Format**:
```json
{
  "symbol": "2330.TW",
  "sentiment_score": 0.72,
  "confidence": 0.88,
  "news_sentiment": {
    "positive": 15,
    "neutral": 5,
    "negative": 2
  },
  "trending_keywords": [
    "AI chips",
    "3nm technology",
    "order backlog"
  ],
  "narrative": "Market optimistic about TSMC's AI chip demand"
}
```

**Agent Prompt Example**:
```
Analyze sentiment for TSMC from news and market commentary.
Focus on:
1. Overall sentiment trend
2. Key themes and narratives
3. Sentiment shifts over the week
4. Comparison with sector sentiment
```

---

### 4. Risk Compliance Officer ⚠️

**Primary Responsibility**: Challenge analyses and identify risks

**Capabilities**:
- Stress test investment scenarios
- Identify geopolitical risks
- Assess valuation concerns
- Challenge bullish/bearish biases
- Validate data completeness
- Trigger analysis revisions

**Tools**:
- `RiskAssessmentTool`: Multi-factor risk evaluation

**Output Format**:
```json
{
  "symbol": "2330.TW",
  "risk_level": "MEDIUM",
  "risk_factors": [
    {
      "category": "geopolitical",
      "severity": "medium",
      "description": "Taiwan Strait tensions remain concern"
    },
    {
      "category": "valuation",
      "severity": "medium",
      "description": "P/E ratio 25x above historical average"
    }
  ],
  "stress_tests": {
    "10_percent_revenue_drop": {"impact": "15% price decline"},
    "us_export_restrictions": {"impact": "severe"}
  },
  "challenge_issued": true,
  "revision_required": false
}
```

**Agent Behavior**:
- **Skeptical by default**: Questions all positive recommendations
- **Challenge threshold**: 0.7 probability triggers re-analysis
- **Max revisions**: 2 iterations to prevent infinite loops
- **No delegation**: Must personally review all analyses

**Agent Prompt Example**:
```
Review the analysis for TSMC. Your job is to find flaws.
Challenge:
1. Are there overlooked risks?
2. Is the data complete and accurate?
3. Are assumptions reasonable?
4. What could go wrong?
Issue revision request if concerns are significant.
```

---

### 5. Chief Investment Officer 🎯

**Primary Responsibility**: Final synthesis and recommendations

**Capabilities**:
- Integrate all agent analyses
- Resolve conflicting signals
- Generate executive summaries
- Assign investment ratings
- Define actionable strategies
- Create comprehensive reports

**Tools**:
- `SummarizationTool`: LangChain summarization

**Output Format**:
```json
{
  "symbol": "2330.TW",
  "rating": "OVERWEIGHT",
  "target_price": 1150,
  "upside_potential": 6.5,
  "strategy": {
    "short_term": "Accumulate above 1085",
    "medium_term": "Hold through Q1 earnings",
    "stop_loss": 1020
  },
  "key_insights": [
    "Strong technical momentum with MACD golden cross",
    "Positive sentiment driven by AI chip demand",
    "Geopolitical risks require monitoring"
  ],
  "executive_summary": "TSMC shows strong technical...",
  "confidence_level": 0.82
}
```

**Agent Prompt Example**:
```
As CIO, synthesize all analyses for TSMC:
- Market data shows: [data]
- Technical signals: [signals]
- Sentiment: [sentiment]
- Risks identified: [risks]

Provide:
1. Clear investment rating
2. Target price with rationale
3. Actionable strategy
4. Key considerations
```

---

## Agent Collaboration Workflow

### Sequential Flow
```
1. Market Intelligence Officer
   ↓ (provides data)
2. [Parallel Execution]
   ├─ Quantitative Strategist
   ├─ Sentiment Analyst
   └─ (both analyze independently)
   ↓ (submit findings)
3. Risk Compliance Officer
   ↓ (challenges findings)
4. [Decision Point]
   ├─ If major risks found → Back to Step 1
   └─ If acceptable → Continue
   ↓
5. Chief Investment Officer
   ↓ (synthesizes report)
6. Human Review (optional)
   ↓
7. Final Report Published
```

### Iterative Refinement
The Risk Officer can trigger up to 2 revisions if:
- Data is incomplete or stale
- Analysis contains logical flaws
- Critical risks are overlooked
- Conflicting signals aren't addressed

### Example Iteration Scenario
```
Iteration 1:
- Market Intel: Reports strong earnings
- Quant: Generates BUY signal
- Sentiment: Positive (0.8)
- Risk Officer: "Wait - P/E ratio at 40x is extreme.
                Redo analysis considering valuation."

Iteration 2:
- Market Intel: Adds valuation context vs peers
- Quant: Adjusts recommendation to HOLD
- Sentiment: Still positive
- Risk Officer: "Acceptable. Proceed."

Final:
- CIO: Issues HOLD rating with cautious optimism
```

---

## Agent Communication Protocol

### Inter-Agent Messages
Agents communicate via structured messages:

```python
{
  "from_agent": "quant_strategist",
  "to_agent": "cio",
  "message_type": "analysis_complete",
  "timestamp": "2025-01-12T15:30:00Z",
  "payload": {
    "symbol": "2330.TW",
    "recommendation": "BUY",
    "confidence": 0.85
  }
}
```

### State Management (LangGraph)
```python
class ResearchState(TypedDict):
    stock_symbol: str
    market_data: dict
    technical_analysis: dict
    sentiment_score: float
    risk_assessment: dict
    final_report: str
    revision_count: int
    human_approved: bool
```

---

## Monitoring & Observability

### LangSmith Integration
All agent actions are traced:
- Token usage per agent
- Execution time per step
- Decision rationale
- Error logs
- Cost tracking

### Metrics Dashboard
- Agent execution count
- Average tokens per agent
- Revision frequency
- Human override rate
- Report generation time

---

## Configuration

### Enabling/Disabling Agents
Edit `app/config/agent_config.yaml`:

```yaml
agents:
  sentiment_analyst:
    enabled: false  # Disable sentiment analysis
```

### Adjusting Risk Threshold
```yaml
agents:
  risk_officer:
    challenge_threshold: 0.8  # More strict (fewer challenges)
```

### LLM Model Selection
```yaml
llm:
  model: "gpt-4o-mini"  # Cost savings
  # or "gpt-4o" for higher quality
```

---

## Future Enhancements

### Planned Agent Additions
1. **Macro Economist Agent**: Global economic trend analysis
2. **Sector Specialist Agents**: Deep expertise in specific industries
3. **Options Strategist Agent**: Derivatives strategy recommendations

### Enhanced Capabilities
- Multi-language support (Chinese reports)
- Voice-to-text for verbal analysis
- Real-time alert system
- Portfolio optimization recommendations

---

## Development Guidelines

### Adding a New Agent

1. Create agent file in `app/agents/`:
```python
# app/agents/new_agent.py
from crewai import Agent

class NewAgent:
    def __init__(self, config):
        self.agent = Agent(
            role="New Role",
            goal="Agent goal",
            backstory="Agent backstory",
            tools=[],
            verbose=True
        )
```

2. Register in `app/agents/__init__.py`

3. Update workflow in `app/workflows/research_workflow.py`

4. Add configuration in `app/config/agent_config.yaml`

### Testing Agents
```bash
# Test individual agent
uv run pytest tests/test_agents/test_market_intelligence.py

# Test agent interaction
uv run pytest tests/test_workflows/test_agent_collaboration.py
```

---

## Troubleshooting

### Agent Not Executing
- Check agent enabled in config
- Verify LLM API key set
- Review LangSmith traces for errors

### Infinite Revision Loop
- Check `max_revisions` setting
- Review risk officer threshold
- Examine revision triggers in logs

### High Token Usage
- Reduce `max_tokens` per agent
- Enable caching in config
- Use smaller model for non-critical agents

---

## References

- [CrewAI Documentation](https://docs.crewai.com/)
- [LangGraph Multi-Agent Systems](https://langchain-ai.github.io/langgraph/)
- [Agent Prompt Engineering Best Practices](https://platform.openai.com/docs/guides/prompt-engineering)
