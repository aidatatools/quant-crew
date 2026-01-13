import { useState, useEffect } from "react";
import DashboardHeader from "@/components/DashboardHeader";
import StatsHeader from "@/components/StatsHeader";
import ConfiguredTickers from "@/components/ConfiguredTickers";
import TickerCard from "@/components/TickerCard";
import { Loader2 } from "lucide-react";

interface TickerData {
  ticker: string;
  record_count: number;
  earliest_date: string;
  latest_date: string;
}

interface ApiData {
  configured_tickers: string[];
  tickers_in_database: TickerData[];
}

// Mock data - replace with actual API call
const mockData: ApiData = {
  configured_tickers: ["2330.TW", "TSM", "NVDA", "GOOG"],
  tickers_in_database: [
    {
      ticker: "2330.TW",
      record_count: 243,
      earliest_date: "2025-01-13",
      latest_date: "2026-01-13",
    },
    {
      ticker: "GOOG",
      record_count: 252,
      earliest_date: "2025-01-13",
      latest_date: "2026-01-13",
    },
    {
      ticker: "NVDA",
      record_count: 252,
      earliest_date: "2025-01-13",
      latest_date: "2026-01-13",
    },
    {
      ticker: "TSM",
      record_count: 252,
      earliest_date: "2025-01-13",
      latest_date: "2026-01-13",
    },
  ],
};

const Index = () => {
  const [data, setData] = useState<ApiData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate API fetch - replace with actual fetch call
    const fetchData = async () => {
      try {
        // Replace this with your actual API endpoint:
        // const response = await fetch('YOUR_API_ENDPOINT');
        // const json = await response.json();
        // setData(json);
        
        // Using mock data for now
        await new Promise((resolve) => setTimeout(resolve, 800));
        setData(mockData);
      } catch (error) {
        console.error("Failed to fetch data:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="flex flex-col items-center gap-4">
          <Loader2 className="h-8 w-8 text-primary animate-spin" />
          <p className="text-muted-foreground font-mono text-sm">Loading data...</p>
        </div>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-destructive font-mono">Failed to load data</p>
      </div>
    );
  }

  const totalRecords = data.tickers_in_database.reduce(
    (sum, ticker) => sum + ticker.record_count,
    0
  );

  const tickersInDb = data.tickers_in_database.map((t) => t.ticker);

  return (
    <div className="min-h-screen bg-background">
      {/* Background gradient */}
      <div className="fixed inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5 pointer-events-none" />
      
      <div className="relative container mx-auto px-4 py-8 md:py-12 max-w-6xl">
        <DashboardHeader />
        
        <StatsHeader
          totalTickers={data.tickers_in_database.length}
          totalRecords={totalRecords}
          configuredCount={data.configured_tickers.length}
        />

        <ConfiguredTickers
          configured={data.configured_tickers}
          inDatabase={tickersInDb}
        />

        <div className="mb-6">
          <h2 className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-4">
            Database Records
          </h2>
        </div>

        <div className="ticker-grid">
          {data.tickers_in_database.map((ticker, index) => (
            <TickerCard key={ticker.ticker} data={ticker} index={index} />
          ))}
        </div>

        {/* Footer */}
        <footer className="mt-12 pt-8 border-t border-border text-center">
          <p className="text-muted-foreground text-sm font-mono">
            quant-crew © {new Date().getFullYear()} • Real-time market analytics
          </p>
        </footer>
      </div>
    </div>
  );
};

export default Index;
