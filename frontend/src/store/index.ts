import { create } from "zustand";
import { persist } from "zustand/middleware";

// ── Theme ─────────────────────────────────────────────────────────────────────
interface ThemeStore {
  theme: "dark" | "light" | "system";
  setTheme: (t: "dark" | "light" | "system") => void;
  resolvedTheme: "dark" | "light";
  _applyTheme: (t: "dark" | "light" | "system") => void;
}

export const useThemeStore = create<ThemeStore>()(
  persist(
    (set, get) => ({
      theme: "dark",
      resolvedTheme: "dark",
      setTheme: (theme) => {
        set({ theme });
        get()._applyTheme(theme);
      },
      _applyTheme: (theme) => {
        const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
        const resolved: "dark" | "light" =
          theme === "system" ? (prefersDark ? "dark" : "light") : theme;
        document.documentElement.classList.toggle("dark", resolved === "dark");
        set({ resolvedTheme: resolved });
      },
    }),
    { name: "arip-theme" }
  )
);

// ── Sidebar ───────────────────────────────────────────────────────────────────
interface SidebarStore {
  isCollapsed: boolean;
  isMobileOpen: boolean;
  toggle: () => void;
  collapse: () => void;
  expand: () => void;
  openMobile: () => void;
  closeMobile: () => void;
}

export const useSidebarStore = create<SidebarStore>()(
  persist(
    (set) => ({
      isCollapsed: false,
      isMobileOpen: false,
      toggle: () => set((s) => ({ isCollapsed: !s.isCollapsed })),
      collapse: () => set({ isCollapsed: true }),
      expand: () => set({ isCollapsed: false }),
      openMobile: () => set({ isMobileOpen: true }),
      closeMobile: () => set({ isMobileOpen: false }),
    }),
    { name: "arip-sidebar" }
  )
);

// ── Command Palette ───────────────────────────────────────────────────────────
interface CommandPaletteStore {
  isOpen: boolean;
  query: string;
  open: () => void;
  close: () => void;
  setQuery: (q: string) => void;
}

export const useCommandPaletteStore = create<CommandPaletteStore>()((set) => ({
  isOpen: false,
  query: "",
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false, query: "" }),
  setQuery: (query) => set({ query }),
}));

// ── Notifications ─────────────────────────────────────────────────────────────
export interface Notification {
  id: string;
  title: string;
  description?: string;
  type: "info" | "success" | "warning" | "error";
  timestamp: number;
  read: boolean;
}

interface NotificationStore {
  notifications: Notification[];
  isOpen: boolean;
  unreadCount: number;
  open: () => void;
  close: () => void;
  toggle: () => void;
  add: (n: Omit<Notification, "id" | "timestamp" | "read">) => void;
  markRead: (id: string) => void;
  markAllRead: () => void;
  remove: (id: string) => void;
  clear: () => void;
}

export const useNotificationStore = create<NotificationStore>()((set, get) => ({
  notifications: [],
  isOpen: false,
  unreadCount: 0,
  open: () => set({ isOpen: true }),
  close: () => set({ isOpen: false }),
  toggle: () => set((s) => ({ isOpen: !s.isOpen })),
  add: (n) => {
    const notification: Notification = {
      ...n,
      id: Math.random().toString(36).slice(2),
      timestamp: Date.now(),
      read: false,
    };
    set((s) => ({
      notifications: [notification, ...s.notifications].slice(0, 50),
      unreadCount: s.unreadCount + 1,
    }));
  },
  markRead: (id) =>
    set((s) => ({
      notifications: s.notifications.map((n) =>
        n.id === id ? { ...n, read: true } : n
      ),
      unreadCount: Math.max(0, s.unreadCount - 1),
    })),
  markAllRead: () =>
    set((s) => ({
      notifications: s.notifications.map((n) => ({ ...n, read: true })),
      unreadCount: 0,
    })),
  remove: (id) =>
    set((s) => ({
      notifications: s.notifications.filter((n) => n.id !== id),
      unreadCount: s.notifications.find((n) => n.id === id && !n.read)
        ? Math.max(0, s.unreadCount - 1)
        : s.unreadCount,
    })),
  clear: () => set({ notifications: [], unreadCount: 0 }),
}));

// ── AI Status ─────────────────────────────────────────────────────────────────
export type AgentStatus = "idle" | "processing" | "completed" | "error";

export interface AgentState {
  id: string;
  label: string;
  status: AgentStatus;
  progress?: number;
  message?: string;
}

interface AIStatusStore {
  agents: AgentState[];
  isVisible: boolean;
  globalStatus: AgentStatus;
  setAgents: (agents: AgentState[]) => void;
  updateAgent: (id: string, update: Partial<AgentState>) => void;
  resetAll: () => void;
  show: () => void;
  hide: () => void;
}

export const useAIStatusStore = create<AIStatusStore>()((set, get) => ({
  agents: [],
  isVisible: false,
  globalStatus: "idle",
  setAgents: (agents) => set({ agents, isVisible: true }),
  updateAgent: (id, update) => {
    set((s) => {
      const agents = s.agents.map((a) => (a.id === id ? { ...a, ...update } : a));
      const statuses = agents.map((a) => a.status);
      const globalStatus: AgentStatus = statuses.some((s) => s === "error")
        ? "error"
        : statuses.some((s) => s === "processing")
        ? "processing"
        : statuses.every((s) => s === "completed")
        ? "completed"
        : "idle";
      return { agents, globalStatus };
    });
  },
  resetAll: () => set({ agents: [], globalStatus: "idle", isVisible: false }),
  show: () => set({ isVisible: true }),
  hide: () => set({ isVisible: false }),
}));

// ── Global Loader ─────────────────────────────────────────────────────────────
interface GlobalLoaderStore {
  isLoading: boolean;
  message: string;
  show: (msg?: string) => void;
  hide: () => void;
}

export const useGlobalLoaderStore = create<GlobalLoaderStore>()((set) => ({
  isLoading: false,
  message: "Loading…",
  show: (message = "Loading…") => set({ isLoading: true, message }),
  hide: () => set({ isLoading: false }),
}));
