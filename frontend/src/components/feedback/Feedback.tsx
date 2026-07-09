import { AlertCircle, CheckCircle, Info, Loader2, Sparkles } from "lucide-react";
import { cn } from "../../lib/utils";

// ── 1. Alert ─────────────────────────────────────────────────────────────────
export function Alert({
  variant = "info",
  title,
  description,
  className,
}: {
  variant?: "info" | "success" | "warning" | "error";
  title?: string;
  description: string;
  className?: string;
}) {
  const icons = {
    info: Info,
    success: CheckCircle,
    warning: AlertCircle,
    error: AlertCircle,
  };

  const colors = {
    info: "bg-info/10 text-info border-info/20",
    success: "bg-success/10 text-success border-success/20",
    warning: "bg-warning/10 text-warning border-warning/20",
    error: "bg-destructive/10 text-destructive border-destructive/20",
  };

  const Icon = icons[variant];

  return (
    <div
      className={cn(
        "border rounded-xl p-4 flex gap-3 items-start backdrop-blur-sm",
        colors[variant],
        className
      )}
    >
      <Icon className="h-5 w-5 shrink-0 mt-0.5" />
      <div className="flex flex-col gap-0.5">
        {title && <span className="font-semibold text-sm leading-tight">{title}</span>}
        <span className="text-xs leading-normal opacity-90">{description}</span>
      </div>
    </div>
  );
}

// ── 2. Loading State ──────────────────────────────────────────────────────────
export function LoadingState({ label = "Thinking..." }: { label?: string }) {
  return (
    <div className="flex flex-col items-center justify-center gap-4 py-12 w-full">
      <div className="relative flex items-center justify-center">
        <Loader2 className="h-10 w-10 text-primary animate-spin" />
        <Sparkles className="h-4 w-4 text-primary absolute animate-pulse" />
      </div>
      <span className="text-xs font-semibold text-muted-foreground uppercase tracking-widest animate-pulse">
        {label}
      </span>
    </div>
  );
}

// ── 3. Empty State ────────────────────────────────────────────────────────────
export function EmptyState({
  title,
  description,
  action,
}: {
  title: string;
  description: string;
  action?: React.ReactNode;
}) {
  return (
    <div className="border border-dashed border-border/80 rounded-xl p-10 flex flex-col items-center text-center justify-center gap-4 min-h-[220px]">
      <div className="h-12 w-12 rounded-xl bg-accent/40 flex items-center justify-center">
        <Sparkles className="h-5 w-5 text-muted-foreground" />
      </div>
      <div className="flex flex-col gap-1 max-w-[280px]">
        <h4 className="font-semibold text-sm text-foreground tracking-tight">
          {title}
        </h4>
        <p className="text-xs text-muted-foreground leading-normal">
          {description}
        </p>
      </div>
      {action && <div className="mt-2">{action}</div>}
    </div>
  );
}

// ── 4. Error State ────────────────────────────────────────────────────────────
export function ErrorState({
  title = "Something went wrong",
  description,
  retry,
}: {
  title?: string;
  description: string;
  retry?: () => void;
}) {
  return (
    <div className="border border-destructive/20 bg-destructive/5 rounded-xl p-8 flex flex-col items-center text-center justify-center gap-4">
      <div className="h-10 w-10 rounded-lg bg-destructive/15 flex items-center justify-center">
        <AlertCircle className="h-5 w-5 text-destructive" />
      </div>
      <div className="flex flex-col gap-1 max-w-[280px]">
        <h4 className="font-semibold text-sm text-foreground tracking-tight">
          {title}
        </h4>
        <p className="text-xs text-muted-foreground leading-normal">
          {description}
        </p>
      </div>
      {retry && (
        <button
          onClick={retry}
          className="text-xs text-primary font-semibold hover:underline mt-1"
        >
          Try Again
        </button>
      )}
    </div>
  );
}

// ── 5. Skeleton Loader ────────────────────────────────────────────────────────
export function SkeletonLoader({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "animate-pulse bg-muted rounded-lg w-full h-8",
        className
      )}
    />
  );
}
export function SkeletonCards({ count = 3 }: { count?: number }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full">
      {Array.from({ length: count }).map((_, i) => (
        <div key={i} className="border border-border/40 bg-card/20 rounded-xl p-6 flex flex-col gap-3">
          <SkeletonLoader className="h-5 w-1/3" />
          <SkeletonLoader className="h-3 w-3/4" />
          <SkeletonLoader className="h-3 w-1/2" />
        </div>
      ))}
    </div>
  );
}
