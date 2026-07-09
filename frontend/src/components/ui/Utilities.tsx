import * as React from "react";
import { Moon, Sun } from "lucide-react";
import { useTheme } from "../theme-provider";
import { cn } from "../../lib/utils";

// ── 1. Theme Toggle ──────────────────────────────────────────────────────────
export function ThemeToggle() {
  const { theme, setTheme } = useTheme();

  return (
    <button
      onClick={() => setTheme(theme === "dark" ? "light" : "dark")}
      className="h-9 w-9 rounded-lg border border-border/80 bg-accent/30 flex items-center justify-center cursor-pointer hover:bg-accent/60 transition-all text-foreground/80 hover:text-foreground"
    >
      {theme === "dark" ? (
        <Sun className="h-4 w-4" />
      ) : (
        <Moon className="h-4 w-4" />
      )}
    </button>
  );
}

// ── 2. Divider ───────────────────────────────────────────────────────────────
export function Divider({
  label,
  className,
}: {
  label?: string;
  className?: string;
}) {
  return (
    <div className={cn("relative flex py-4 items-center w-full", className)}>
      <div className="flex-grow border-t border-border/40" />
      {label && (
        <span className="flex-shrink mx-4 text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
          {label}
        </span>
      )}
      <div className="flex-grow border-t border-border/40" />
    </div>
  );
}

// ── 3. Avatar ────────────────────────────────────────────────────────────────
export function Avatar({
  src,
  fallback,
  className,
}: {
  src?: string;
  fallback: string;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "h-8 w-8 rounded-full overflow-hidden border border-border/80 bg-accent/40 flex items-center justify-center select-none shrink-0",
        className
      )}
    >
      {src ? (
        <img src={src} alt="avatar" className="h-full w-full object-cover" />
      ) : (
        <span className="text-xs font-semibold text-foreground/80 uppercase">
          {fallback.slice(0, 2)}
        </span>
      )}
    </div>
  );
}

// ── 4. Tooltip ───────────────────────────────────────────────────────────────
export function Tooltip({
  content,
  children,
}: {
  content: string;
  children: React.ReactNode;
}) {
  return (
    <div className="relative group flex items-center">
      {children}
      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-2.5 py-1.5 bg-card border border-border/80 rounded-lg text-[10px] font-medium text-foreground tracking-wide whitespace-nowrap shadow-lg opacity-0 group-hover:opacity-100 transition-opacity duration-200 pointer-events-none z-50">
        {content}
      </div>
    </div>
  );
}

// ── 5. Breadcrumb ────────────────────────────────────────────────────────────
export function Breadcrumb({ items }: { items: { label: string; href?: string }[] }) {
  return (
    <nav className="flex items-center gap-2 select-none text-xs text-muted-foreground">
      {items.map((item, idx) => (
        <React.Fragment key={idx}>
          {idx > 0 && <span className="opacity-40">/</span>}
          {item.href ? (
            <a
              href={item.href}
              className="hover:text-primary transition-colors cursor-pointer"
            >
              {item.label}
            </a>
          ) : (
            <span className="text-foreground font-medium">{item.label}</span>
          )}
        </React.Fragment>
      ))}
    </nav>
  );
}

// ── 6. Scrollable Container ──────────────────────────────────────────────────
export function ScrollableContainer({
  children,
  maxHeight = "300px",
  className,
}: {
  children: React.ReactNode;
  maxHeight?: string;
  className?: string;
}) {
  return (
    <div
      style={{ maxHeight }}
      className={cn(
        "overflow-y-auto w-full pr-1.5 scrollbar-thin scrollbar-thumb-muted",
        className
      )}
    >
      {children}
    </div>
  );
}
