import { NavLink, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  LayoutDashboard,
  BrainCircuit,
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

export interface NavItem {
  label: string;
  href: string;
  icon: React.ElementType;
  badge?: string;
  end?: boolean;
}

const NAV_ITEMS: NavItem[] = [
  { label: "Dashboard",      href: "/dashboard", icon: LayoutDashboard, end: true },
  { label: "New Analysis",   href: "/upload",    icon: Upload },
  { label: "History",        href: "/history",   icon: History },
  { label: "Reports",        href: "/reports",   icon: FileText },
  { label: "AI Coach",       href: "/coach",     icon: Sparkles },
];

const BOTTOM_ITEMS: NavItem[] = [
  { label: "Settings", href: "/settings", icon: Settings },
  { label: "Profile",  href: "/profile",  icon: User },
];

// ── Sidebar Item ──────────────────────────────────────────────────────────────
export function SidebarItem({
  item,
  collapsed,
  onClick,
}: {
  item: NavItem;
  collapsed: boolean;
  onClick?: () => void;
}) {
  return (
    <NavLink
      to={item.href}
      end={item.end}
      onClick={onClick}
      className={({ isActive }) =>
        cn(
          "relative flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all duration-200 select-none group border",
          isActive
            ? "bg-primary/10 text-primary border-primary/20 shadow-sm"
            : "text-muted-foreground hover:bg-accent/40 hover:text-foreground border-transparent"
        )
      }
    >
      {({ isActive }) => (
        <>
          {/* Active indicator bar */}
          {isActive && (
            <motion.div
              layoutId="sidebar-active"
              className="absolute left-0 top-1/2 -translate-y-1/2 w-0.5 h-5 bg-primary rounded-full"
            />
          )}
          <item.icon
            className={cn(
              "h-4 w-4 shrink-0 transition-colors",
              isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"
            )}
          />
          <AnimatePresence>
            {!collapsed && (
              <motion.span
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: "auto" }}
                exit={{ opacity: 0, width: 0 }}
                transition={{ duration: 0.2 }}
                className="overflow-hidden whitespace-nowrap"
              >
                {item.label}
              </motion.span>
            )}
          </AnimatePresence>
          {item.badge && !collapsed && (
            <span className="ml-auto text-[10px] font-bold bg-primary/20 text-primary px-1.5 py-0.5 rounded-full">
              {item.badge}
            </span>
          )}
        </>
      )}
    </NavLink>
  );
}

// ── Desktop Sidebar ───────────────────────────────────────────────────────────
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
          <ChevronRight className="h-3 w-3" />
        ) : (
          <ChevronLeft className="h-3 w-3" />
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
              "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all text-muted-foreground hover:bg-destructive/10 hover:text-destructive border border-transparent select-none",
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

// ── Mobile Sidebar Drawer ─────────────────────────────────────────────────────
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
