import { CheckCircle2, Circle } from "lucide-react";

interface ConfiguredTickersProps {
  configured: string[];
  inDatabase: string[];
}

const ConfiguredTickers = ({ configured, inDatabase }: ConfiguredTickersProps) => {
  return (
    <div className="mb-8 animate-fade-in" style={{ animationDelay: "200ms" }}>
      <h2 className="text-sm font-medium text-muted-foreground uppercase tracking-wider mb-4">
        Configured Tickers
      </h2>
      <div className="flex flex-wrap gap-3">
        {configured.map((ticker) => {
          const isInDb = inDatabase.includes(ticker);
          return (
            <div
              key={ticker}
              className={`
                flex items-center gap-2 px-4 py-2 rounded-full font-mono text-sm font-medium
                border transition-all duration-200
                ${isInDb 
                  ? 'bg-accent/10 border-accent/30 text-accent' 
                  : 'bg-secondary border-border text-muted-foreground'
                }
              `}
            >
              {isInDb ? (
                <CheckCircle2 className="h-4 w-4" />
              ) : (
                <Circle className="h-4 w-4" />
              )}
              {ticker}
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default ConfiguredTickers;
