import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  FileText,
  History,
  Settings,
  User,
  LogOut,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  Bot,
  Upload,
} from "lucide-react";
import { useSidebarStore } from "../../store";
import { cn } from "../../lib/utils";
import { SidebarItem, type NavItem } from "./SidebarItem";

export const NAV_ITEMS: NavItem[] = [
  { label: "Dashboard",      href: "/dashboard", icon: LayoutDashboard, end: true },
  { label: "New Analysis",   href: "/upload",    icon: Upload },
  { label: "History",        href: "/history",   icon: History },
  { label: "Reports",        href: "/reports",   icon: FileText },
  { label: "AI Coach",       href: "/coach",     icon: Sparkles },
];

export const BOTTOM_ITEMS: NavItem[] = [
  { label: "Settings", href: "/settings", icon: Settings },
  { label: "Profile",  href: "/profile",  icon: User },
];

export function Sidebar() {
  const { isCollapsed, toggle } = useSidebarStore();
  const navigate = useNavigate();

  return (
    <motion.aside
      initial={false}
      animate={{ width: isCollapsed ? 68 : 240 }}
      transition={{ duration: 0.25, ease: [0.16, 1, 0.3, 1] }}
      className="hidden md:flex flex-col bg-card/50 border-r border-border/40 min-h-[calc(100vh-57px)] shrink-0 overflow-hidden relative"
    >
      {/* Collapse toggle button */}
      <button
        onClick={toggle}
        className="absolute -right-3 top-6 z-10 h-6 w-6 rounded-full border border-border/80 bg-card shadow-sm flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-accent/40 transition-all"
      >
        {isCollapsed ? (
          <ChevronRight className="h-3.5 w-3.5" />
        ) : (
          <ChevronLeft className="h-3.5 w-3.5" />
        )}
      </button>

      <div className="flex flex-col gap-1 p-3 flex-1">
        {/* Main nav */}
        <div className="flex flex-col gap-0.5 pt-2">
          {NAV_ITEMS.map((item) => (
            <SidebarItem key={item.href} item={item} collapsed={isCollapsed} />
          ))}
        </div>

        {/* Spacer */}
        <div className="flex-1" />

        {/* Divider */}
        <div className="border-t border-border/30 my-2" />

        {/* Bottom nav */}
        <div className="flex flex-col gap-0.5">
          {BOTTOM_ITEMS.map((item) => (
            <SidebarItem key={item.href} item={item} collapsed={isCollapsed} />
          ))}

          {/* Logout */}
          <button
            onClick={() => navigate("/")}
            className={cn(
              "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all text-muted-foreground hover:bg-destructive/10 hover:text-destructive border border-transparent select-none w-full",
            )}
          >
            <LogOut className="h-4 w-4 shrink-0" />
            <AnimatePresence>
              {!isCollapsed && (
                <motion.span
                  initial={{ opacity: 0, width: 0 }}
                  animate={{ opacity: 1, width: "auto" }}
                  exit={{ opacity: 0, width: 0 }}
                  transition={{ duration: 0.2 }}
                  className="overflow-hidden whitespace-nowrap"
                >
                  Logout
                </motion.span>
              )}
            </AnimatePresence>
          </button>
        </div>

        {/* Brand badge at bottom */}
        {!isCollapsed && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="mt-3 rounded-lg bg-primary/5 border border-primary/15 p-3"
          >
            <div className="flex items-center gap-2 mb-1">
              <Bot className="h-3.5 w-3.5 text-primary" />
              <span className="text-[11px] font-bold text-primary uppercase tracking-wider">
                ARIP v1.0
              </span>
            </div>
            <p className="text-[10px] text-muted-foreground leading-relaxed">
              Multi-Agent Intelligence Platform
            </p>
          </motion.div>
        )}
      </div>
    </motion.aside>
  );
}
