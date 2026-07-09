import { useEffect } from "react";
import { TopNavbar } from "../components/navigation/TopNavbar";
import { Sidebar, MobileSidebar } from "../components/navigation/Sidebar";
import { CommandPalette } from "../components/navigation/CommandPalette";
import { AIStatusDock } from "../components/navigation/AIStatusDock";
import { QuickActionFAB } from "../components/navigation/QuickActionFAB";
import { GlobalLoader } from "../components/navigation/GlobalLoader";
import { RouteTransition } from "../components/navigation/RouteTransition";
import { ErrorBoundary } from "../components/navigation/ErrorBoundary";
import { useKeyboardShortcuts } from "../hooks/useKeyboardShortcuts";
import { useThemeStore } from "../store";

// ── App Shell ─────────────────────────────────────────────────────────────────
export function AppShell({ children }: { children: React.ReactNode }) {
  const { theme, _applyTheme } = useThemeStore();

  useEffect(() => {
    _applyTheme(theme);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  useKeyboardShortcuts();

  return (
    <div className="min-h-screen flex flex-col bg-background text-foreground">
      <GlobalLoader />
      <CommandPalette />
      <AIStatusDock />

      <TopNavbar />

      <div className="flex flex-1 overflow-hidden">
        <Sidebar />
        <MobileSidebar />

        <main className="flex-1 overflow-y-auto min-h-[calc(100vh-56px)]">
          <ErrorBoundary>
            <RouteTransition>{children}</RouteTransition>
          </ErrorBoundary>
        </main>
      </div>

      <QuickActionFAB />
    </div>
  );
}

// ── Dashboard Layout ──────────────────────────────────────────────────────────
export function DashboardLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="max-w-7xl mx-auto px-4 md:px-8 py-6 flex flex-col gap-6">
      {children}
    </div>
  );
}

// ── Auth Layout ───────────────────────────────────────────────────────────────
export function AuthLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-background px-4 relative overflow-hidden">
      <div className="absolute inset-0 pointer-events-none">
        <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-primary/8 rounded-full blur-[120px]" />
      </div>
      <div className="relative z-10 w-full max-w-md">{children}</div>
    </div>
  );
}

// ── Blank Layout ──────────────────────────────────────────────────────────────
export function BlankLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background text-foreground">{children}</div>
  );
}
