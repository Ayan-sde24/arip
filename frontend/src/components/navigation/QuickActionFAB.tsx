import { motion, AnimatePresence } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { Upload, BarChart2, Plus, X } from "lucide-react";
import * as React from "react";
import { cn } from "../../lib/utils";

const ACTIONS = [
  { icon: Upload,    label: "Upload Resume",  href: "/upload",  color: "bg-primary" },
  { icon: BarChart2, label: "View Reports",   href: "/reports", color: "bg-indigo-500" },
];

export function QuickActionFAB() {
  const [open, setOpen] = React.useState(false);
  const navigate = useNavigate();

  return (
    <div className="fixed bottom-6 right-6 z-50 flex flex-col-reverse items-end gap-3">
      {/* Sub-actions */}
      <AnimatePresence>
        {open &&
          ACTIONS.map((action, i) => (
            <motion.div
              key={action.href}
              initial={{ opacity: 0, y: 16, scale: 0.85 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: 16, scale: 0.85 }}
              transition={{ delay: i * 0.06, duration: 0.2, ease: [0.16, 1, 0.3, 1] }}
              className="flex items-center gap-3"
            >
              <span className="text-xs font-medium text-foreground bg-card border border-border/80 px-2.5 py-1 rounded-lg shadow-sm whitespace-nowrap">
                {action.label}
              </span>
              <button
                onClick={() => { navigate(action.href); setOpen(false); }}
                className={cn(
                  "h-10 w-10 rounded-full flex items-center justify-center text-white shadow-lg transition-transform hover:scale-105 active:scale-95",
                  action.color
                )}
              >
                <action.icon className="h-4 w-4" />
              </button>
            </motion.div>
          ))}
      </AnimatePresence>

      {/* Main FAB */}
      <motion.button
        onClick={() => setOpen((o) => !o)}
        whileHover={{ scale: 1.06 }}
        whileTap={{ scale: 0.94 }}
        className="h-12 w-12 rounded-full bg-gradient-to-br from-primary to-indigo-500 text-white shadow-xl shadow-primary/30 flex items-center justify-center transition-all"
      >
        <motion.div
          animate={{ rotate: open ? 45 : 0 }}
          transition={{ duration: 0.2 }}
        >
          {open ? <X className="h-5 w-5" /> : <Plus className="h-5 w-5" />}
        </motion.div>
      </motion.button>
    </div>
  );
}
