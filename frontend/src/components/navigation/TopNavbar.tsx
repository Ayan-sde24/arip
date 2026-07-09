import * as React from "react";
import { Link, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Bot,
  Menu,
  Search,
  Bell,
  Sun,
  Moon,
  Monitor,
  User,
  Settings,
  LogOut,
  ChevronDown,
  CheckCheck,
  X,
  Upload,
  BarChart2,
  LayoutDashboard,
  Zap,
} from "lucide-react";
import {
  useSidebarStore,
  useThemeStore,
  useCommandPaletteStore,
  useNotificationStore,
} from "../../store";
import { cn } from "../../lib/utils";
import { Badge } from "../ui/Badge";

// ── Theme Switcher ────────────────────────────────────────────────────────────
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

// ── Search Bar ────────────────────────────────────────────────────────────────
export function SearchBar() {
  const { open } = useCommandPaletteStore();
  return (
    <button
      onClick={open}
      className="hidden md:flex items-center gap-2 h-8 px-3 rounded-lg border border-border/60 bg-accent/20 text-muted-foreground hover:bg-accent/40 hover:text-foreground transition-all text-xs font-medium min-w-[180px]"
    >
      <Search className="h-3.5 w-3.5 shrink-0" />
      <span className="flex-1 text-left">Search…</span>
      <kbd className="text-[10px] font-semibold bg-muted px-1.5 py-0.5 rounded border border-border/60">
        ⌘K
      </kbd>
    </button>
  );
}

// ── Notification Dropdown ─────────────────────────────────────────────────────
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

// ── User Dropdown ─────────────────────────────────────────────────────────────
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

// ── Top Navbar ────────────────────────────────────────────────────────────────
export function TopNavbar() {
  const { openMobile } = useSidebarStore();
  const { open: openPalette } = useCommandPaletteStore();

  return (
    <motion.header
      initial={{ y: -10, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ duration: 0.4, ease: [0.16, 1, 0.3, 1] }}
      className="sticky top-0 z-40 w-full h-14 bg-background/70 backdrop-blur-xl border-b border-border/40 flex items-center px-4 gap-3 shrink-0"
    >
      {/* Mobile menu button */}
      <button
        onClick={openMobile}
        className="md:hidden h-8 w-8 rounded-lg border border-border/60 flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-accent/40 transition-all shrink-0"
      >
        <Menu className="h-4 w-4" />
      </button>

      {/* Brand */}
      <Link to="/" className="flex items-center gap-2 shrink-0 group mr-2">
        <div className="h-7 w-7 rounded-lg bg-gradient-to-br from-primary to-indigo-500 flex items-center justify-center shadow-lg shadow-primary/20">
          <Bot className="h-4 w-4 text-white" />
        </div>
        <span className="hidden sm:block font-bold text-sm tracking-tight bg-gradient-to-r from-primary to-indigo-400 bg-clip-text text-transparent">
          ARIP
        </span>
      </Link>

      {/* Search */}
      <div className="flex-1">
        <SearchBar />
      </div>

      {/* Right actions */}
      <div className="flex items-center gap-2 shrink-0">
        {/* Quick Ctrl+K hint on mobile */}
        <button
          onClick={openPalette}
          className="md:hidden h-8 w-8 rounded-lg border border-border/60 bg-accent/20 flex items-center justify-center text-muted-foreground hover:bg-accent/40 transition-all"
        >
          <Search className="h-3.5 w-3.5" />
        </button>

        <ThemeSwitcher />
        <NotificationDropdown />
        <UserDropdown />
      </div>
    </motion.header>
  );
}
