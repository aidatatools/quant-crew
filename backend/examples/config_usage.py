"""
Example: Using the Consolidated Configuration System

This script demonstrates how to use the unified configuration system
that combines environment variables (.env) and YAML files.
"""

from app.config import settings, config_loader


def main():
    """Demonstrate configuration usage."""

    print("=" * 60)
    print("Quant-Crew Configuration System Demo")
    print("=" * 60)

    # Part 1: Environment Variables (from .env)
    print("\n📌 Part 1: Environment Variables")
    print("-" * 60)
    print(f"App Name: {settings.APP_NAME}")
    print(f"Environment: {settings.ENVIRONMENT}")
    print(f"Debug Mode: {settings.DEBUG}")
    print(f"API Prefix: {settings.API_V1_PREFIX}")
    print(f"OpenAI Model: {settings.OPENAI_MODEL}")
    print(f"OpenAI Temperature: {settings.OPENAI_TEMPERATURE}")
    print(f"LangSmith Tracing: {settings.LANGCHAIN_TRACING_V2}")

    # Part 2: Stock Watchlist (from YAML)
    print("\n📊 Part 2: Stock Watchlist")
    print("-" * 60)

    # Get all symbols
    symbols = config_loader.get_watchlist_symbols()
    print(f"Total stocks to analyze: {len(symbols)}")
    print(f"Symbols: {', '.join(symbols)}")

    # Get full watchlist structure
    watchlist = config_loader.stock_watchlist
    print("\nBreakdown by region:")
    for region, stocks in watchlist["stocks"].items():
        print(f"  {region.upper()}: {len(stocks)} stocks")
        for stock in stocks:
            print(f"    - {stock['symbol']}: {stock['name']}")

    # Part 3: Agent Configuration (from YAML)
    print("\n🤖 Part 3: Agent Configuration")
    print("-" * 60)

    # Get LLM settings
    llm_settings = config_loader.get_llm_settings()
    print("LLM Settings:")
    print(f"  Model: {llm_settings['model']}")
    print(f"  Temperature: {llm_settings['temperature']}")
    print(f"  Max Tokens: {llm_settings['max_tokens']}")

    # Get specific agent settings
    print("\nAgent Settings:")
    agents = ["market_intelligence", "quant_strategist", "sentiment_analyst",
              "risk_officer", "cio"]

    for agent_name in agents:
        agent_config = config_loader.get_agent_settings(agent_name)
        print(f"\n  {agent_config['role']}:")
        print(f"    Max Iterations: {agent_config.get('max_iterations', 'N/A')}")
        print(f"    Verbose: {agent_config.get('verbose', 'N/A')}")
        if "challenge_threshold" in agent_config:
            print(f"    Challenge Threshold: {agent_config['challenge_threshold']}")
        if "indicators" in agent_config:
            print(f"    Indicators: {', '.join(agent_config['indicators'])}")

    # Part 4: Practical Usage Examples
    print("\n💡 Part 4: Practical Usage Examples")
    print("-" * 60)

    # Example 1: Generate report for all watchlist stocks
    print("\n1. Generate report for all stocks in watchlist:")
    print(f"   symbols = config_loader.get_watchlist_symbols()")
    print(f"   # Returns: {symbols[:3]}...")
    print(f"   workflow.run_weekly_analysis(stocks=symbols)")

    # Example 2: Configure an agent
    print("\n2. Configure an agent with settings:")
    print(f"   agent_config = config_loader.get_agent_settings('quant_strategist')")
    print(f"   agent = Agent(")
    print(f"       role=agent_config['role'],")
    print(f"       goal=agent_config['goal'],")
    print(f"       max_iterations=agent_config['max_iterations']")
    print(f"   )")

    # Example 3: Use LLM settings
    print("\n3. Initialize LLM with loaded settings:")
    print(f"   llm_settings = config_loader.get_llm_settings()")
    print(f"   llm = ChatOpenAI(")
    print(f"       model=llm_settings['model'],")
    print(f"       temperature=llm_settings['temperature']")
    print(f"   )")

    # Part 5: Configuration File Locations
    print("\n📁 Part 5: Configuration File Locations")
    print("-" * 60)
    print("Environment Variables:")
    print("  File: backend/.env")
    print("  Access: from app.config import settings")
    print("\nYAML Configurations:")
    print("  Files:")
    print("    - backend/app/config/stock_watchlist.yaml")
    print("    - backend/app/config/agent_config.yaml")
    print("  Access: from app.config import config_loader")

    print("\n" + "=" * 60)
    print("Configuration loaded successfully! ✅")
    print("=" * 60)


if __name__ == "__main__":
    main()
