import * as React from "react";
import { useNavigate } from "react-router-dom";
import { User, Settings, LogOut, ChevronDown } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";

export function UserDropdown() {
  const [open, setOpen] = React.useState(false);
  const ref = React.useRef<HTMLDivElement>(null);
  const navigate = useNavigate();

  React.useEffect(() => {
    function handle(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false);
    }
    document.addEventListener("mousedown", handle);
    return () => document.removeEventListener("mousedown", handle);
  }, []);

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((o) => !o)}
        className="flex items-center gap-2 h-8 px-2 rounded-lg border border-border/60 bg-accent/20 hover:bg-accent/40 transition-all"
      >
        <div className="h-5 w-5 rounded-full bg-gradient-to-br from-primary to-indigo-400 flex items-center justify-center text-[9px] font-bold text-white">
          A
        </div>
        <ChevronDown className="h-3 w-3 text-muted-foreground" />
      </button>

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.97 }}
            transition={{ duration: 0.15 }}
            className="absolute right-0 top-full mt-2 w-52 bg-card border border-border/80 rounded-xl shadow-glass z-50 overflow-hidden"
          >
            {/* User info */}
            <div className="px-4 py-3 border-b border-border/40">
              <p className="text-xs font-semibold text-foreground">ARIP User</p>
              <p className="text-[11px] text-muted-foreground">user@example.com</p>
            </div>

            {/* Menu items */}
            {[
              { icon: User,     label: "Profile",  href: "/profile" },
              { icon: Settings, label: "Settings", href: "/settings" },
            ].map((item) => (
              <button
                key={item.href}
                onClick={() => { navigate(item.href); setOpen(false); }}
                className="flex items-center gap-2.5 w-full px-4 py-2.5 text-xs font-medium text-muted-foreground hover:bg-accent/40 hover:text-foreground transition-colors"
              >
                <item.icon className="h-3.5 w-3.5" />
                {item.label}
              </button>
            ))}

            <div className="border-t border-border/30 my-1" />
            <button
              onClick={() => { navigate("/"); setOpen(false); }}
              className="flex items-center gap-2.5 w-full px-4 py-2.5 text-xs font-medium text-destructive hover:bg-destructive/10 transition-colors"
            >
              <LogOut className="h-3.5 w-3.5" />
              Sign out
            </button>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
