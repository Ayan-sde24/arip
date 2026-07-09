import * as React from "react";
import { cn } from "../../lib/utils";

export function PageContainer({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div
      className={cn(
        "min-h-screen w-full px-4 py-8 md:px-8 max-w-7xl mx-auto flex flex-col gap-6 animate-fade-in",
        className
      )}
    >
      {children}
    </div>
  );
}

export function SectionContainer({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <section className={cn("flex flex-col gap-4 w-full", className)}>
      {children}
    </section>
  );
}

export function ContentArea({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("flex-1 w-full bg-background", className)}>
      {children}
    </div>
  );
}

export function ResponsiveGrid({
  children,
  cols = 3,
  className,
}: {
  children: React.ReactNode;
  cols?: 1 | 2 | 3 | 4;
  className?: string;
}) {
  const gridCols = {
    1: "grid-cols-1",
    2: "grid-cols-1 md:grid-cols-2",
    3: "grid-cols-1 md:grid-cols-2 lg:grid-cols-3",
    4: "grid-cols-1 md:grid-cols-2 lg:grid-cols-4",
  };

  return (
    <div className={cn("grid gap-6 w-full", gridCols[cols], className)}>
      {children}
    </div>
  );
}

export function GlassPanel({
  children,
  className,
}: {
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <div className={cn("glass-panel rounded-xl p-6", className)}>
      {children}
    </div>
  );
}
