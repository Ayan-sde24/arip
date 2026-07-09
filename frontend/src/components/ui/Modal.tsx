import * as React from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle, Search, X } from "lucide-react";
import { cn } from "../../lib/utils";

// ── 1. Dialog ────────────────────────────────────────────────────────────────
export function Dialog({
  isOpen,
  onClose,
  title,
  children,
  className,
}: {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
  className?: string;
}) {
  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-background/80 backdrop-blur-sm"
          />

          {/* Modal box */}
          <motion.div
            initial={{ scale: 0.95, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.95, opacity: 0 }}
            transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
            className={cn(
              "relative bg-card border border-border/80 rounded-xl shadow-glass w-full max-w-lg overflow-hidden z-10 flex flex-col max-h-[90vh]",
              className
            )}
          >
            <div className="px-6 py-5 border-b border-border/40 flex items-center justify-between">
              <h3 className="font-semibold text-base text-foreground leading-none">
                {title}
              </h3>
              <button
                onClick={onClose}
                className="text-muted-foreground hover:text-foreground hover:bg-accent/40 p-1.5 rounded-lg transition-all"
              >
                <X className="h-4 w-4" />
              </button>
            </div>
            <div className="p-6 overflow-y-auto flex-1">{children}</div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

// ── 2. Confirmation Dialog ───────────────────────────────────────────────────
export function ConfirmationDialog({
  isOpen,
  onClose,
  onConfirm,
  title,
  description,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
}: {
  isOpen: boolean;
  onClose: () => void;
  onConfirm: () => void;
  title: string;
  description: string;
  confirmLabel?: string;
  cancelLabel?: string;
}) {
  return (
    <Dialog isOpen={isOpen} onClose={onClose} title={title} className="max-w-md">
      <div className="flex flex-col gap-6">
        <div className="flex gap-3 items-start">
          <div className="h-10 w-10 rounded-lg bg-warning/15 flex items-center justify-center shrink-0">
            <AlertTriangle className="h-5 w-5 text-warning" />
          </div>
          <span className="text-xs text-muted-foreground leading-normal">
            {description}
          </span>
        </div>
        <div className="flex justify-end gap-3">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold text-foreground bg-accent/40 hover:bg-accent/60 rounded-lg transition-all"
          >
            {cancelLabel}
          </button>
          <button
            onClick={() => {
              onConfirm();
              onClose();
            }}
            className="px-4 py-2 text-xs font-semibold text-white bg-destructive hover:bg-destructive/90 rounded-lg transition-all"
          >
            {confirmLabel}
          </button>
        </div>
      </div>
    </Dialog>
  );
}

// ── 3. Command Palette ────────────────────────────────────────────────────────
export function CommandPalette({
  isOpen,
  onClose,
  items,
  onSelect,
}: {
  isOpen: boolean;
  onClose: () => void;
  items: { label: string; value: string; category?: string }[];
  onSelect: (value: string) => void;
}) {
  const [query, setQuery] = React.useState("");

  const filtered = items.filter((item) =>
    item.label.toLowerCase().includes(query.toLowerCase())
  );

  return (
    <AnimatePresence>
      {isOpen && (
        <div className="fixed inset-0 z-50 flex items-start justify-center p-4 pt-[15vh]">
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={onClose}
            className="absolute inset-0 bg-background/80 backdrop-blur-sm"
          />

          {/* Box */}
          <motion.div
            initial={{ y: -20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            exit={{ y: -20, opacity: 0 }}
            className="relative bg-card border border-border/80 rounded-xl shadow-glass w-full max-w-lg overflow-hidden z-10 flex flex-col"
          >
            <div className="flex items-center px-4 py-3 border-b border-border/40 gap-3">
              <Search className="h-4 w-4 text-muted-foreground" />
              <input
                type="text"
                placeholder="Type a command or search..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="flex-1 bg-transparent border-0 text-sm focus-visible:outline-none text-foreground placeholder:text-muted-foreground/60"
              />
              <button
                onClick={onClose}
                className="text-xs text-muted-foreground hover:text-foreground px-2 py-1 rounded bg-accent/40"
              >
                ESC
              </button>
            </div>
            <div className="max-h-[300px] overflow-y-auto p-2 flex flex-col gap-0.5">
              {filtered.length > 0 ? (
                filtered.map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      onSelect(item.value);
                      onClose();
                    }}
                    className="w-full text-left px-3 py-2.5 text-xs text-foreground hover:bg-accent/40 rounded-lg transition-all flex items-center justify-between"
                  >
                    <span>{item.label}</span>
                    {item.category && (
                      <span className="text-[10px] uppercase font-semibold text-muted-foreground tracking-wider bg-muted px-1.5 py-0.5 rounded">
                        {item.category}
                      </span>
                    )}
                  </button>
                ))
              ) : (
                <span className="text-center py-6 text-xs text-muted-foreground">
                  No matching commands found.
                </span>
              )}
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}
