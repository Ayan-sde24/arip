import { motion } from "framer-motion";
import { cn } from "../../lib/utils";

// ── 1. Glass Card ────────────────────────────────────────────────────────────
export function GlassCard({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <motion.div
      whileHover={{ y: -2 }}
      className={cn(
        "bg-card/45 backdrop-blur-md border border-border/40 hover:border-primary/20 shadow-glass rounded-xl p-6 transition-all duration-300",
        className
      )}
    >
      {children}
    </motion.div>
  );
}

// ── 2. Metric Card ───────────────────────────────────────────────────────────
export function MetricCard({
  title,
  value,
  trend,
  className,
}: {
  title: string;
  value: string | number;
  trend?: { label: string; positive: boolean };
  className?: string;
}) {
  return (
    <div
      className={cn(
        "bg-card/30 border border-border/40 rounded-xl p-6 flex flex-col gap-2 hover:bg-card/50 transition-all",
        className
      )}
    >
      <span className="text-xs font-semibold text-muted-foreground uppercase tracking-wider">
        {title}
      </span>
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-bold tracking-tight text-foreground">
          {value}
        </span>
        {trend && (
          <span
            className={cn(
              "text-xs font-medium",
              trend.positive ? "text-success" : "text-destructive"
            )}
          >
            {trend.positive ? "+" : ""}
            {trend.label}
          </span>
        )}
      </div>
    </div>
  );
}

// ── 3. Dashboard Card ────────────────────────────────────────────────────────
export function DashboardCard({
  title,
  subtitle,
  children,
  className,
}: {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "bg-card/45 border border-border/40 rounded-xl flex flex-col overflow-hidden",
        className
      )}
    >
      <div className="px-6 py-5 border-b border-border/40 flex flex-col gap-0.5">
        <h3 className="font-semibold text-base text-foreground leading-tight">
          {title}
        </h3>
        {subtitle && (
          <span className="text-xs text-muted-foreground">{subtitle}</span>
        )}
      </div>
      <div className="p-6 flex-1 flex flex-col justify-center">{children}</div>
    </div>
  );
}

// ── 4. AIAgentCard ───────────────────────────────────────────────────────────
export function AIAgentCard({
  agentName,
  status,
  description,
  score,
  className,
}: {
  agentName: string;
  status: "idle" | "running" | "completed" | "failed";
  description: string;
  score?: number;
  className?: string;
}) {
  const statusColors = {
    idle: "bg-muted-foreground/20 text-muted-foreground border-muted-foreground/30",
    running: "bg-primary/20 text-primary border-primary/30 animate-pulse",
    completed: "bg-success/20 text-success border-success/30",
    failed: "bg-destructive/20 text-destructive border-destructive/30",
  };

  return (
    <div
      className={cn(
        "bg-card/40 border border-border/40 rounded-xl p-5 flex flex-col gap-4 relative overflow-hidden group hover:border-primary/25 transition-all",
        className
      )}
    >
      <div className="flex items-center justify-between">
        <span className="font-semibold text-sm text-foreground">{agentName}</span>
        <span
          className={cn(
            "text-xs px-2 py-0.5 rounded-full border font-medium uppercase tracking-wide",
            statusColors[status]
          )}
        >
          {status}
        </span>
      </div>

      <p className="text-xs text-muted-foreground leading-normal">{description}</p>

      {score !== undefined && (
        <div className="flex items-center justify-between border-t border-border/30 pt-3 mt-1">
          <span className="text-xs text-muted-foreground">Expert Score:</span>
          <span className="text-sm font-bold text-primary">{score}/100</span>
        </div>
      )}
    </div>
  );
}

// ── 5. Feature Card ──────────────────────────────────────────────────────────
export function FeatureCard({
  title,
  description,
  icon: Icon,
  className,
}: {
  title: string;
  description: string;
  icon: React.ComponentType<{ className?: string }>;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "bg-card/30 border border-border/40 hover:bg-card/55 rounded-xl p-6 flex flex-col gap-3 group transition-all duration-300 hover:border-primary/20",
        className
      )}
    >
      <div className="h-10 w-10 rounded-lg bg-accent/40 flex items-center justify-center group-hover:scale-105 transition-transform">
        <Icon className="h-5 w-5 text-muted-foreground group-hover:text-primary transition-colors" />
      </div>
      <div className="flex flex-col gap-1">
        <h4 className="font-semibold text-sm text-foreground tracking-tight">
          {title}
        </h4>
        <p className="text-xs text-muted-foreground leading-normal">
          {description}
        </p>
      </div>
    </div>
  );
}
