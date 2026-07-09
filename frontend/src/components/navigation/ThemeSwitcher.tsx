import * as React from "react";
import { Moon, Sun, Monitor, CheckCheck } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import { useThemeStore } from "../../store";
import { cn } from "../../lib/utils";

export function ThemeSwitcher() {
  const { theme, setTheme } = useThemeStore();
  const [open, setOpen] = React.useState(false);
  const ref = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    function handle(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handle);
    return () => document.removeEventListener("mousedown", handle);
  }, []);

  const options = [
    { value: "dark",   label: "Dark",   icon: Moon },
    { value: "light",  label: "Light",  icon: Sun },
    { value: "system", label: "System", icon: Monitor },
  ] as const;

  const CurrentIcon = options.find((o) => o.value === theme)?.icon ?? Moon;

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className="h-8 w-8 rounded-lg border border-border/60 bg-accent/20 flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-accent/40 transition-all"
      >
        <CurrentIcon className="h-3.5 w-3.5" />
      </button>
      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.97 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 top-full mt-2 w-36 bg-card border border-border/80 rounded-xl shadow-glass overflow-hidden z-50"
          >
            {options.map((opt) => (
              <button
                key={opt.value}
                onClick={() => { setTheme(opt.value); setOpen(false); }}
                className={cn(
                  "flex items-center gap-2.5 w-full px-3 py-2 text-xs font-medium hover:bg-accent/40 transition-colors",
                  theme === opt.value ? "text-primary" : "text-muted-foreground"
                )}
              >
                <opt.icon className="h-3.5 w-3.5" />
                {opt.label}
                {theme === opt.value && <CheckCheck className="h-3 w-3 ml-auto" />}
              </button>
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
