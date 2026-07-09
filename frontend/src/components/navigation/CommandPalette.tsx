import * as React from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  LayoutDashboard,
  Upload,
  FileText,
  History,
  Settings,
  Sparkles,
  ArrowRight,
  Keyboard,
} from "lucide-react";
import { useCommandPaletteStore } from "../../store";
import { cn } from "../../lib/utils";

interface PaletteItem {
  id: string;
  label: string;
  description?: string;
  category: "navigate" | "action" | "recent" | "shortcut";
  icon: React.ElementType;
  shortcut?: string;
  action: () => void;
}

export function CommandPalette() {
  const { isOpen, query, close, setQuery } = useCommandPaletteStore();
  const navigate = useNavigate();
  const inputRef = React.useRef<HTMLInputElement>(null);
  const [selected, setSelected] = React.useState(0);

  const ALL_ITEMS = React.useMemo(
    (): PaletteItem[] => [
      {
        id: "nav-dashboard",
        label: "Dashboard",
        description: "Go to your analysis dashboard",
        category: "navigate",
        icon: LayoutDashboard,
        shortcut: "Ctrl+D",
        action: () => navigate("/dashboard"),
      },
      {
        id: "nav-upload",
        label: "Upload Resume",
        description: "Start a new resume analysis",
        category: "navigate",
        icon: Upload,
        shortcut: "Ctrl+U",
        action: () => navigate("/upload"),
      },
      {
        id: "nav-history",
        label: "Analysis History",
        description: "View all past analyses",
        category: "navigate",
        icon: History,
        action: () => navigate("/history"),
      },
      {
        id: "nav-reports",
        label: "Reports",
        description: "Browse generated reports",
        category: "navigate",
        icon: FileText,
        action: () => navigate("/reports"),
      },
      {
        id: "nav-coach",
        label: "AI Coach",
        description: "Open AI resume coaching",
        category: "navigate",
        icon: Sparkles,
        action: () => navigate("/coach"),
      },
      {
        id: "nav-settings",
        label: "Settings",
        description: "Manage account and preferences",
        category: "navigate",
        icon: Settings,
        action: () => navigate("/settings"),
      },
      {
        id: "action-analyze",
        label: "Start Analysis",
        description: "Run a new multi-agent analysis",
        category: "action",
        icon: ArrowRight,
        shortcut: "Ctrl+J",
        action: () => navigate("/upload"),
      },
      {
        id: "action-demo",
        label: "View Sample Report",
        description: "Open demo report — no backend needed",
        category: "action",
        icon: FileText,
        action: () => navigate("/report/demo"),
      },
      {
        id: "shortcut-keys",
        label: "Keyboard Shortcuts",
        description: "Ctrl+K · Ctrl+U · Ctrl+J · Ctrl+D",
        category: "shortcut",
        icon: Keyboard,
        action: () => {},
      },
    ],
    [navigate]
  );

  const filtered = React.useMemo(() => {
    if (!query.trim()) return ALL_ITEMS;
    const q = query.toLowerCase();
    return ALL_ITEMS.filter(
      (item) =>
        item.label.toLowerCase().includes(q) ||
        item.description?.toLowerCase().includes(q)
    );
  }, [query, ALL_ITEMS]);

  // Reset selection when filtered list changes
  React.useEffect(() => setSelected(0), [filtered.length]);

  // Focus input on open
  React.useEffect(() => {
    if (isOpen) setTimeout(() => inputRef.current?.focus(), 50);
  }, [isOpen]);

  // Keyboard navigation
  React.useEffect(() => {
    if (!isOpen) return;
    function onKey(e: KeyboardEvent) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setSelected((s) => Math.min(s + 1, filtered.length - 1));
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setSelected((s) => Math.max(s - 1, 0));
      } else if (e.key === "Enter") {
        e.preventDefault();
        filtered[selected]?.action();
        close();
      }
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [isOpen, filtered, selected, close]);

  const CATEGORY_LABELS: Record<PaletteItem["category"], string> = {
    navigate: "Navigation",
    action: "Actions",
    recent: "Recent",
    shortcut: "Shortcuts",
  };

  const grouped = filtered.reduce<Record<string, PaletteItem[]>>((acc, item) => {
    const key = item.category;
    acc[key] = acc[key] ? [...acc[key], item] : [item];
    return acc;
  }, {});

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-[100] flex items-start justify-center pt-[15vh] px-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.15 }}
            onClick={close}
            className="absolute inset-0 bg-background/80 backdrop-blur-md"
          />

          {/* Palette box */}
          <motion.div
            initial={{ opacity: 0, y: -16, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -16, scale: 0.97 }}
            transition={{ duration: 0.22, ease: [0.16, 1, 0.3, 1] }}
            className="relative w-full max-w-xl bg-card/95 border border-border/80 rounded-2xl shadow-2xl shadow-black/30 overflow-hidden z-10 flex flex-col"
          >
            {/* Search input */}
            <div className="flex items-center gap-3 px-4 py-3.5 border-b border-border/40">
              <Search className="h-4 w-4 text-muted-foreground shrink-0" />
              <input
                ref={inputRef}
                type="text"
                placeholder="Search commands, pages, actions…"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted-foreground/60 focus:outline-none"
              />
              <button
                onClick={close}
                className="text-[10px] font-semibold text-muted-foreground bg-muted border border-border/60 px-1.5 py-0.5 rounded hover:bg-accent/40 transition-colors"
              >
                ESC
              </button>
            </div>

            {/* Results */}
            <div className="max-h-[380px] overflow-y-auto p-2">
              {filtered.length === 0 ? (
                <div className="py-12 text-center text-xs text-muted-foreground">
                  No results for "{query}"
                </div>
              ) : (
                Object.entries(grouped).map(([category, items]) => (
                  <div key={category} className="mb-2">
                    <p className="px-3 py-1.5 text-[10px] uppercase font-bold tracking-wider text-muted-foreground">
                      {CATEGORY_LABELS[category as PaletteItem["category"]]}
                    </p>
                    {items.map((item) => {
                      const globalIdx = filtered.indexOf(item);
                      const isSelected = globalIdx === selected;
                      return (
                        <button
                          key={item.id}
                          onMouseEnter={() => setSelected(globalIdx)}
                          onClick={() => { item.action(); close(); }}
                          className={cn(
                            "w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-left transition-colors",
                            isSelected ? "bg-primary/10 text-foreground" : "hover:bg-accent/30"
                          )}
                        >
                          <div className={cn(
                            "h-7 w-7 rounded-lg flex items-center justify-center shrink-0 transition-colors",
                            isSelected ? "bg-primary/20" : "bg-muted"
                          )}>
                            <item.icon className={cn("h-3.5 w-3.5", isSelected ? "text-primary" : "text-muted-foreground")} />
                          </div>
                          <div className="flex-1 min-w-0">
                            <p className={cn("text-xs font-semibold leading-tight", isSelected ? "text-foreground" : "text-foreground/80")}>
                              {item.label}
                            </p>
                            {item.description && (
                              <p className="text-[11px] text-muted-foreground truncate">{item.description}</p>
                            )}
                          </div>
                          {item.shortcut && (
                            <kbd className="text-[10px] font-semibold text-muted-foreground bg-muted border border-border/60 px-1.5 py-0.5 rounded shrink-0">
                              {item.shortcut}
                            </kbd>
                          )}
                        </button>
                      );
                    })}
                  </div>
                ))
              )}
            </div>

            {/* Footer */}
            <div className="border-t border-border/30 px-4 py-2 flex items-center gap-4 text-[10px] text-muted-foreground">
              <span className="flex items-center gap-1">
                <kbd className="bg-muted border border-border/60 px-1 rounded">↑↓</kbd> Navigate
              </span>
              <span className="flex items-center gap-1">
                <kbd className="bg-muted border border-border/60 px-1 rounded">↵</kbd> Select
              </span>
              <span className="flex items-center gap-1">
                <kbd className="bg-muted border border-border/60 px-1 rounded">Esc</kbd> Close
              </span>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
