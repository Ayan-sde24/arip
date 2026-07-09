import { motion, AnimatePresence } from "framer-motion";
import { Bot } from "lucide-react";
import { useSidebarStore } from "../../store";
import { SidebarItem } from "./SidebarItem";
import { NAV_ITEMS, BOTTOM_ITEMS } from "./Sidebar";

export function MobileSidebar() {
  const { isMobileOpen, closeMobile } = useSidebarStore();

  return (
    <AnimatePresence>
      {isMobileOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={closeMobile}
            className="fixed inset-0 z-40 bg-background/80 backdrop-blur-sm md:hidden"
          />

          {/* Drawer */}
          <motion.aside
            initial={{ x: "-100%" }}
            animate={{ x: 0 }}
            exit={{ x: "-100%" }}
            transition={{ duration: 0.28, ease: [0.16, 1, 0.3, 1] }}
            className="fixed left-0 top-0 bottom-0 z-50 w-64 bg-card border-r border-border/40 flex flex-col md:hidden shadow-2xl"
          >
            {/* Header */}
            <div className="flex items-center gap-2 px-4 py-4 border-b border-border/40">
              <Bot className="h-5 w-5 text-primary" />
              <span className="font-semibold text-base tracking-tight bg-gradient-to-r from-primary to-indigo-400 bg-clip-text text-transparent">
                ARIP
              </span>
            </div>

            <div className="flex flex-col gap-0.5 p-3 flex-1 overflow-y-auto">
              {NAV_ITEMS.map((item) => (
                <SidebarItem
                  key={item.href}
                  item={item}
                  collapsed={false}
                  onClick={closeMobile}
                />
              ))}
              <div className="border-t border-border/30 my-2" />
              {BOTTOM_ITEMS.map((item) => (
                <SidebarItem
                  key={item.href}
                  item={item}
                  collapsed={false}
                  onClick={closeMobile}
                />
              ))}
            </div>

            {/* Close button */}
            <button
              onClick={closeMobile}
              className="m-3 py-2.5 text-xs font-semibold text-muted-foreground border border-border/40 rounded-lg hover:bg-accent/30 transition-all"
            >
              Close Menu
            </button>
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  );
}
