import { Activity } from "lucide-react";

const DashboardHeader = () => {
  return (
    <header className="mb-10 animate-slide-in">
      <div className="flex items-center gap-3 mb-2">
        <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
          <Activity className="h-5 w-5 text-primary" />
        </div>
        <h1 className="text-3xl md:text-4xl font-bold tracking-tight">
          <span className="gradient-text">quant-crew</span>
        </h1>
      </div>
      <p className="text-muted-foreground text-lg">
        Real-time market data monitoring & analytics
      </p>
    </header>
  );
};

export default DashboardHeader;
