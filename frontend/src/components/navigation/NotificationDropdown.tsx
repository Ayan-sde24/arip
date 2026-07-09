import * as React from "react";
import { Bell, X } from "lucide-react";
import { AnimatePresence, motion } from "framer-motion";
import { useNotificationStore } from "../../store";
import { cn } from "../../lib/utils";

export function NotificationDropdown() {
  const { isOpen, toggle, close, notifications, unreadCount, markRead, markAllRead, remove } =
    useNotificationStore();
  const ref = React.useRef<HTMLDivElement>(null);

  React.useEffect(() => {
    function handle(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) close();
    }
    document.addEventListener("mousedown", handle);
    return () => document.removeEventListener("mousedown", handle);
  }, [close]);

  const typeColor = {
    info:    "text-info",
    success: "text-success",
    warning: "text-warning",
    error:   "text-destructive",
  };

  return (
    <div ref={ref} className="relative">
      <button
        onClick={toggle}
        className="relative h-8 w-8 rounded-lg border border-border/60 bg-accent/20 flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-accent/40 transition-all"
      >
        <Bell className="h-3.5 w-3.5" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 h-3.5 w-3.5 bg-primary rounded-full text-[9px] font-bold text-white flex items-center justify-center">
            {unreadCount > 9 ? "9+" : unreadCount}
          </span>
        )}
      </button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -8, scale: 0.97 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -8, scale: 0.97 }}
            transition={{ duration: 0.18 }}
            className="absolute right-0 top-full mt-2 w-80 bg-card border border-border/80 rounded-xl shadow-glass z-50 flex flex-col overflow-hidden"
          >
            <div className="flex items-center justify-between px-4 py-3 border-b border-border/40">
              <span className="text-sm font-semibold text-foreground">Notifications</span>
              <div className="flex items-center gap-2">
                {unreadCount > 0 && (
                  <button
                    onClick={markAllRead}
                    className="text-[10px] font-medium text-primary hover:text-primary/80 transition-colors"
                  >
                    Mark all read
                  </button>
                )}
              </div>
            </div>

            <div className="max-h-72 overflow-y-auto">
              {notifications.length === 0 ? (
                <div className="py-10 text-center text-xs text-muted-foreground">
                  No notifications yet
                </div>
              ) : (
                notifications.map((n) => (
                  <div
                    key={n.id}
                    onClick={() => markRead(n.id)}
                    className={cn(
                      "flex gap-3 px-4 py-3 cursor-pointer hover:bg-accent/30 transition-colors border-b border-border/20 last:border-0",
                      !n.read && "bg-primary/3"
                    )}
                  >
                    <div className={cn("text-xs mt-0.5 shrink-0", typeColor[n.type])}>●</div>
                    <div className="flex-1 min-w-0">
                      <p className={cn("text-xs font-semibold leading-tight", !n.read && "text-foreground")}>
                        {n.title}
                      </p>
                      {n.description && (
                        <p className="text-[11px] text-muted-foreground mt-0.5 leading-snug">
                          {n.description}
                        </p>
                      )}
                    </div>
                    <button
                      onClick={(e) => { e.stopPropagation(); remove(n.id); }}
                      className="text-muted-foreground hover:text-foreground transition-colors shrink-0 mt-0.5"
                    >
                      <X className="h-3 w-3" />
                    </button>
                  </div>
                ))
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
