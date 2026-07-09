import * as React from "react";

export function BlankLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground w-full">
      {children}
    </div>
  );
}
