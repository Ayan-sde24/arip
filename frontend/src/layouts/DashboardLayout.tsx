import * as React from "react";

export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="max-w-7xl mx-auto px-4 md:px-8 py-6 flex flex-col gap-6 w-full">
      {children}
    </div>
  );
}
