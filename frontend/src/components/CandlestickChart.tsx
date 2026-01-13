import {
  ComposedChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
  ReferenceLine,
} from "recharts";

interface OHLCData {
  date: string;
  open: number;
  high: number;
  low: number;
  close: number;
  volume: number;
}

interface CandlestickChartProps {
  data: OHLCData[];
}

// Custom candlestick shape
const CandlestickBar = (props: any) => {
  const { x, y, width, height, payload } = props;
  if (!payload) return null;

  const { open, close, high, low } = payload;
  const isUp = close >= open;
  const color = isUp ? "hsl(var(--chart-up))" : "hsl(var(--chart-down))";

  const candleWidth = Math.max(width * 0.8, 2);
  const wickWidth = 1;

  // Calculate positions
  const priceRange = props.yAxis?.scale?.domain?.() || [low, high];
  const minPrice = priceRange[0];
  const maxPrice = priceRange[1];
  const chartHeight = props.yAxis?.height || 400;
  const yOffset = props.yAxis?.y || 0;

  const priceToY = (price: number) => {
    const ratio = (maxPrice - price) / (maxPrice - minPrice);
    return yOffset + ratio * chartHeight;
  };

  const highY = priceToY(high);
  const lowY = priceToY(low);
  const openY = priceToY(open);
  const closeY = priceToY(close);

  const bodyTop = Math.min(openY, closeY);
  const bodyHeight = Math.abs(closeY - openY) || 1;

  const centerX = x + width / 2;

  return (
    <g>
      {/* Wick */}
      <line
        x1={centerX}
        y1={highY}
        x2={centerX}
        y2={lowY}
        stroke={color}
        strokeWidth={wickWidth}
      />
      {/* Body */}
      <rect
        x={centerX - candleWidth / 2}
        y={bodyTop}
        width={candleWidth}
        height={bodyHeight}
        fill={isUp ? color : color}
        stroke={color}
        strokeWidth={1}
      />
    </g>
  );
};

// Custom tooltip
const CustomTooltip = ({ active, payload }: any) => {
  if (!active || !payload || !payload.length) return null;

  const data = payload[0]?.payload;
  if (!data) return null;

  const isUp = data.close >= data.open;

  return (
    <div className="bg-card/95 backdrop-blur-sm border border-border rounded-lg p-3 shadow-xl">
      <p className="text-sm font-mono text-muted-foreground mb-2">
        {data.date}
      </p>
      <div className="grid grid-cols-2 gap-x-4 gap-y-1 text-sm font-mono">
        <span className="text-muted-foreground">Open:</span>
        <span>${data.open.toFixed(2)}</span>
        <span className="text-muted-foreground">High:</span>
        <span className="text-chart-up">${data.high.toFixed(2)}</span>
        <span className="text-muted-foreground">Low:</span>
        <span className="text-chart-down">${data.low.toFixed(2)}</span>
        <span className="text-muted-foreground">Close:</span>
        <span className={isUp ? "text-chart-up" : "text-chart-down"}>
          ${data.close.toFixed(2)}
        </span>
        <span className="text-muted-foreground">Volume:</span>
        <span>{(data.volume / 1000000).toFixed(2)}M</span>
      </div>
    </div>
  );
};

const CandlestickChart = ({ data }: CandlestickChartProps) => {
  // Calculate price range for Y axis
  const prices = data.flatMap((d) => [d.high, d.low]);
  const minPrice = Math.min(...prices);
  const maxPrice = Math.max(...prices);
  const padding = (maxPrice - minPrice) * 0.1;

  // Transform data for the chart
  const chartData = data.map((item) => ({
    ...item,
    // For bar chart, we need a value - use the body size
    value: Math.abs(item.close - item.open) || 0.01,
    // Store the base for the bar
    base: Math.min(item.open, item.close),
  }));

  return (
    <ResponsiveContainer width="100%" height="100%">
      <ComposedChart
        data={chartData}
        margin={{ top: 20, right: 30, left: 20, bottom: 20 }}
      >
        <XAxis
          dataKey="date"
          axisLine={{ stroke: "hsl(var(--border))" }}
          tickLine={false}
          tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
          tickFormatter={(value) => {
            const date = new Date(value);
            return `${date.getMonth() + 1}/${date.getDate()}`;
          }}
          interval="preserveStartEnd"
        />
        <YAxis
          domain={[minPrice - padding, maxPrice + padding]}
          axisLine={{ stroke: "hsl(var(--border))" }}
          tickLine={false}
          tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 11 }}
          tickFormatter={(value) => `$${value.toFixed(0)}`}
          orientation="right"
        />
        <Tooltip content={<CustomTooltip />} />

        {/* Grid lines */}
        <ReferenceLine
          y={(minPrice + maxPrice) / 2}
          stroke="hsl(var(--border))"
          strokeDasharray="3 3"
        />

        {/* Candlesticks rendered as bars with custom shape */}
        <Bar dataKey="value" shape={<CandlestickBar />}>
          {chartData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={
                entry.close >= entry.open
                  ? "hsl(var(--chart-up))"
                  : "hsl(var(--chart-down))"
              }
            />
          ))}
        </Bar>
      </ComposedChart>
    </ResponsiveContainer>
  );
};

export default CandlestickChart;
