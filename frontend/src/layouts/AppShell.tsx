import * as React from "react";
import { useEffect } from "react";
import {
  TopNavbar,
  Sidebar,
  MobileSidebar,
  CommandPalette,
  AIStatusDock,
  QuickActionFAB,
  GlobalLoader,
  RouteTransition,
  ErrorBoundary,
} from "../components/navigation";
import { useKeyboardShortcuts } from "../hooks/useKeyboardShortcuts";
import { useThemeStore } from "../store";

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
