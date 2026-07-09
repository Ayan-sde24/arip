import { cn } from "../../lib/utils";

export function Badge({
  variant = "new",
  children,
  className,
}: {
  variant?: "ai" | "new" | "success" | "warning" | "danger" | "premium";
  children: React.ReactNode;
  className?: string;
}) {
  const styles = {
    ai: "bg-primary/10 text-primary border-primary/20",
    new: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
    success: "bg-success/15 text-success border-success/20",
    warning: "bg-warning/15 text-warning border-warning/20",
    danger: "bg-destructive/15 text-destructive border-destructive/20",
    premium:
      "bg-gradient-to-r from-amber-500/20 to-yellow-600/20 text-yellow-500 border-yellow-500/30 font-semibold",
  };

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-medium tracking-wide uppercase transition-colors select-none",
        styles[variant],
        className
      )}
    >
      {children}
    </span>
  );
}

export function StatusBadge({
  status,
  className,
}: {
  status: "active" | "inactive" | "pending" | "critical";
  className?: string;
}) {
  const maps = {
    active: { variant: "success", label: "Active" },
    inactive: { variant: "new", label: "Inactive" },
    pending: { variant: "warning", label: "Pending" },
    critical: { variant: "danger", label: "Critical" },
  } as const;

  const current = maps[status];

  return (
    <Badge variant={current.variant} className={className}>
      {current.label}
    </Badge>
  );
}
