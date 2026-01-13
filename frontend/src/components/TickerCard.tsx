import { Database, Calendar, TrendingUp } from "lucide-react";

interface TickerData {
  ticker: string;
  record_count: number;
  earliest_date: string;
  latest_date: string;
}

interface TickerCardProps {
  data: TickerData;
  index: number;
}

const TickerCard = ({ data, index }: TickerCardProps) => {
  const formatDate = (dateStr: string) => {
    const date = new Date(dateStr);
    return date.toLocaleDateString('en-US', { 
      month: 'short', 
      day: 'numeric', 
      year: 'numeric' 
    });
  };

  return (
    <div 
      className="group relative overflow-hidden rounded-lg bg-card border border-border p-6 transition-all duration-300 hover:border-primary/50 card-glow"
      style={{ animationDelay: `${index * 100}ms` }}
    >
      {/* Gradient overlay */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
      
      {/* Status indicator */}
      <div className="absolute top-4 right-4 flex items-center gap-2">
        <span className="h-2 w-2 rounded-full bg-accent status-pulse" />
        <span className="text-xs text-muted-foreground font-mono">LIVE</span>
      </div>

      {/* Ticker symbol */}
      <div className="mb-4">
        <h3 className="text-2xl font-bold font-mono tracking-tight text-foreground group-hover:text-primary transition-colors">
          {data.ticker}
        </h3>
      </div>

      {/* Stats grid */}
      <div className="space-y-3">
        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-secondary">
            <Database className="h-4 w-4 text-primary" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground uppercase tracking-wider">Records</p>
            <p className="font-mono text-lg font-semibold text-foreground">
              {data.record_count.toLocaleString()}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-secondary">
            <Calendar className="h-4 w-4 text-primary" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground uppercase tracking-wider">Date Range</p>
            <p className="font-mono text-sm text-foreground">
              {formatDate(data.earliest_date)}
            </p>
            <p className="font-mono text-sm text-muted-foreground">
              → {formatDate(data.latest_date)}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <div className="flex h-8 w-8 items-center justify-center rounded-md bg-secondary">
            <TrendingUp className="h-4 w-4 text-accent" />
          </div>
          <div>
            <p className="text-xs text-muted-foreground uppercase tracking-wider">Coverage</p>
            <p className="font-mono text-sm text-accent font-semibold">
              {Math.round((data.record_count / 365) * 100)}% yearly
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TickerCard;
