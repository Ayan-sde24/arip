import {
  ResponsiveContainer,
  BarChart as RechartsBarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  LineChart as RechartsLineChart,
  Line,
  PieChart as RechartsPieChart,
  Pie,
  Cell,
  RadarChart as RechartsRadarChart,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  Radar,
  AreaChart as RechartsAreaChart,
  Area,
} from "recharts";

// ── 1. Reusable Tooltip styling ──
const customTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-card border border-border/80 p-2.5 rounded-lg shadow-lg backdrop-blur-md">
        <p className="text-xs font-semibold text-foreground uppercase tracking-wide">
          {payload[0].name}
        </p>
        <p className="text-sm font-bold text-primary">{payload[0].value}</p>
      </div>
    );
  }
  return null;
};

// ── 2. Bar Chart ─────────────────────────────────────────────────────────────
export function BarChart({
  data,
  dataKey,
  xAxisKey,
  height = 240,
}: {
  data: any[];
  dataKey: string;
  xAxisKey: string;
  height?: number;
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsBarChart data={data}>
        <XAxis
          dataKey={xAxisKey}
          stroke="hsl(var(--muted-foreground))"
          fontSize={10}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke="hsl(var(--muted-foreground))"
          fontSize={10}
          tickLine={false}
          axisLine={false}
        />
        <Tooltip content={customTooltip} />
        <Bar dataKey={dataKey} fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
      </RechartsBarChart>
    </ResponsiveContainer>
  );
}

// ── 3. Line Chart ────────────────────────────────────────────────────────────
export function LineChart({
  data,
  dataKey,
  xAxisKey,
  height = 240,
}: {
  data: any[];
  dataKey: string;
  xAxisKey: string;
  height?: number;
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsLineChart data={data}>
        <XAxis
          dataKey={xAxisKey}
          stroke="hsl(var(--muted-foreground))"
          fontSize={10}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke="hsl(var(--muted-foreground))"
          fontSize={10}
          tickLine={false}
          axisLine={false}
        />
        <Tooltip content={customTooltip} />
        <Line
          type="monotone"
          dataKey={dataKey}
          stroke="hsl(var(--primary))"
          strokeWidth={2}
          dot={{ strokeWidth: 2, r: 3 }}
        />
      </RechartsLineChart>
    </ResponsiveContainer>
  );
}

// ── 4. Pie Chart ─────────────────────────────────────────────────────────────
export function PieChart({
  data,
  height = 240,
}: {
  data: { name: string; value: number }[];
  height?: number;
}) {
  const COLORS = ["hsl(var(--primary))", "hsl(var(--secondary))", "hsl(var(--muted-foreground))"];

  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsPieChart>
        <Tooltip content={customTooltip} />
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius={60}
          outerRadius={80}
          paddingAngle={4}
          dataKey="value"
        >
          {data.map((_, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
      </RechartsPieChart>
    </ResponsiveContainer>
  );
}

// ── 5. Radar Chart ───────────────────────────────────────────────────────────
export function RadarChart({
  data,
  dataKey,
  angleKey,
  height = 240,
}: {
  data: any[];
  dataKey: string;
  angleKey: string;
  height?: number;
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsRadarChart cx="50%" cy="50%" outerRadius="75%" data={data}>
        <PolarGrid stroke="hsl(var(--border))" />
        <PolarAngleAxis dataKey={angleKey} tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 10 }} />
        <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: "hsl(var(--muted-foreground))", fontSize: 9 }} />
        <Radar
          name="Analysis score"
          dataKey={dataKey}
          stroke="hsl(var(--primary))"
          fill="hsl(var(--primary))"
          fillOpacity={0.25}
        />
      </RechartsRadarChart>
    </ResponsiveContainer>
  );
}

// ── 6. Area Chart ────────────────────────────────────────────────────────────
export function AreaChart({
  data,
  dataKey,
  xAxisKey,
  height = 240,
}: {
  data: any[];
  dataKey: string;
  xAxisKey: string;
  height?: number;
}) {
  return (
    <ResponsiveContainer width="100%" height={height}>
      <RechartsAreaChart data={data}>
        <XAxis
          dataKey={xAxisKey}
          stroke="hsl(var(--muted-foreground))"
          fontSize={10}
          tickLine={false}
          axisLine={false}
        />
        <YAxis
          stroke="hsl(var(--muted-foreground))"
          fontSize={10}
          tickLine={false}
          axisLine={false}
        />
        <Tooltip content={customTooltip} />
        <defs>
          <linearGradient id="colorArea" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="hsl(var(--primary))" stopOpacity={0.4} />
            <stop offset="95%" stopColor="hsl(var(--primary))" stopOpacity={0} />
          </linearGradient>
        </defs>
        <Area
          type="monotone"
          dataKey={dataKey}
          stroke="hsl(var(--primary))"
          fillOpacity={1}
          fill="url(#colorArea)"
        />
      </RechartsAreaChart>
    </ResponsiveContainer>
  );
}
