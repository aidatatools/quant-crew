"""
CrewAI Agent Definitions for Quant Research War Room
"""

from app.agents.market_intelligence import MarketIntelligenceAgent
from app.agents.quant_strategist import QuantStrategistAgent
from app.agents.sentiment_analyst import SentimentAnalystAgent
from app.agents.risk_officer import RiskOfficerAgent
from app.agents.cio import ChiefInvestmentOfficerAgent

__all__ = [
    "MarketIntelligenceAgent",
    "QuantStrategistAgent",
    "SentimentAnalystAgent",
    "RiskOfficerAgent",
    "ChiefInvestmentOfficerAgent",
]
