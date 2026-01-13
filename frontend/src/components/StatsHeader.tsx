import { Activity, Server, Layers, Clock } from "lucide-react";

interface StatsHeaderProps {
  totalTickers: number;
  totalRecords: number;
  configuredCount: number;
}

const StatsHeader = ({ totalTickers, totalRecords, configuredCount }: StatsHeaderProps) => {
  const stats = [
    {
      label: "Configured Tickers",
      value: configuredCount,
      icon: Layers,
      suffix: "",
    },
    {
      label: "Active in Database",
      value: totalTickers,
      icon: Server,
      suffix: "",
    },
    {
      label: "Total Records",
      value: totalRecords,
      icon: Activity,
      suffix: "",
    },
    {
      label: "Last Updated",
      value: "Now",
      icon: Clock,
      suffix: "",
      isText: true,
    },
  ];

  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      {stats.map((stat, index) => (
        <div
          key={stat.label}
          className="relative overflow-hidden rounded-lg bg-secondary/50 border border-border p-4 animate-fade-in"
          style={{ animationDelay: `${index * 50}ms` }}
        >
          <div className="flex items-center justify-between">
            <stat.icon className="h-5 w-5 text-primary" />
            <span className="h-1.5 w-1.5 rounded-full bg-accent" />
          </div>
          <div className="mt-3">
            <p className="text-xs text-muted-foreground uppercase tracking-wider mb-1">
              {stat.label}
            </p>
            <p className="text-2xl font-bold font-mono text-foreground">
              {stat.isText ? stat.value : (stat.value as number).toLocaleString()}
              {stat.suffix}
            </p>
          </div>
        </div>
      ))}
    </div>
  );
};

export default StatsHeader;
