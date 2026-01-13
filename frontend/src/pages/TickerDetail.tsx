import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, TrendingUp, TrendingDown } from "lucide-react";
import { Button } from "@/components/ui/button";
import CandlestickChart from "@/components/CandlestickChart";

// Mock OHLC data - replace with actual API call
const generateMockOHLC = (ticker: string) => {
  const data = [];
  let basePrice = ticker === "NVDA" ? 850 : ticker === "GOOG" ? 175 : ticker === "TSM" ? 180 : 950;
  const startDate = new Date("2025-01-13");

  for (let i = 0; i < 60; i++) {
    const date = new Date(startDate);
    date.setDate(date.getDate() + i);
    
    const volatility = basePrice * 0.02;
    const open = basePrice + (Math.random() - 0.5) * volatility;
    const close = open + (Math.random() - 0.5) * volatility * 2;
    const high = Math.max(open, close) + Math.random() * volatility * 0.5;
    const low = Math.min(open, close) - Math.random() * volatility * 0.5;
    const volume = Math.floor(Math.random() * 10000000) + 1000000;

    data.push({
      date: date.toISOString().split("T")[0],
      open: Number(open.toFixed(2)),
      high: Number(high.toFixed(2)),
      low: Number(low.toFixed(2)),
      close: Number(close.toFixed(2)),
      volume,
    });

    basePrice = close;
  }

  return data;
};

const TickerDetail = () => {
  const { ticker } = useParams<{ ticker: string }>();
  const navigate = useNavigate();

  if (!ticker) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <p className="text-destructive font-mono">Ticker not found</p>
      </div>
    );
  }

  const ohlcData = generateMockOHLC(ticker);
  const latestData = ohlcData[ohlcData.length - 1];
  const previousData = ohlcData[ohlcData.length - 2];
  const priceChange = latestData.close - previousData.close;
  const priceChangePercent = (priceChange / previousData.close) * 100;
  const isPositive = priceChange >= 0;

  return (
    <div className="min-h-screen bg-background">
      {/* Background gradient */}
      <div className="fixed inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5 pointer-events-none" />

      <div className="relative h-screen flex flex-col">
        {/* Header */}
        <header className="flex items-center justify-between p-4 md:p-6 border-b border-border">
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => navigate("/")}
              className="hover:bg-muted"
            >
              <ArrowLeft className="h-5 w-5" />
            </Button>
            <div>
              <h1 className="text-2xl md:text-3xl font-bold font-mono gradient-text">
                {ticker}
              </h1>
              <p className="text-sm text-muted-foreground">
                Candlestick Chart • 60 Days
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-2xl font-bold font-mono">
                ${latestData.close.toFixed(2)}
              </p>
              <div
                className={`flex items-center justify-end gap-1 text-sm font-mono ${
                  isPositive ? "text-chart-up" : "text-chart-down"
                }`}
              >
                {isPositive ? (
                  <TrendingUp className="h-4 w-4" />
                ) : (
                  <TrendingDown className="h-4 w-4" />
                )}
                <span>
                  {isPositive ? "+" : ""}
                  {priceChange.toFixed(2)} ({priceChangePercent.toFixed(2)}%)
                </span>
              </div>
            </div>
          </div>
        </header>

        {/* Chart Container */}
        <div className="flex-1 p-4 md:p-6">
          <div className="h-full card-glow rounded-xl p-4">
            <CandlestickChart data={ohlcData} />
          </div>
        </div>

        {/* Footer Stats */}
        <footer className="border-t border-border p-4 md:p-6">
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">
                Open
              </p>
              <p className="font-mono font-semibold">
                ${latestData.open.toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">
                High
              </p>
              <p className="font-mono font-semibold text-chart-up">
                ${latestData.high.toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">
                Low
              </p>
              <p className="font-mono font-semibold text-chart-down">
                ${latestData.low.toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">
                Close
              </p>
              <p className="font-mono font-semibold">
                ${latestData.close.toFixed(2)}
              </p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground uppercase tracking-wider">
                Volume
              </p>
              <p className="font-mono font-semibold">
                {(latestData.volume / 1000000).toFixed(2)}M
              </p>
            </div>
          </div>
        </footer>
      </div>
    </div>
  );
};

export default TickerDetail;
