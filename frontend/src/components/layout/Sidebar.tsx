import { NavLink } from "react-router-dom";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  BrainCircuit,
  Sparkles,
  History,
  Settings,
  FileText,
} from "lucide-react";

const menuItems = [
  { label: "Home",           icon: LayoutDashboard, href: "/" },
  { label: "Analyze Resume", icon: BrainCircuit,    href: "/upload" },
  { label: "Sample Report",  icon: FileText,        href: "/report/demo" },
  { label: "History",        icon: History,         href: "/history" },
  { label: "AI Coach",       icon: Sparkles,        href: "/coach" },
  { label: "Settings",       icon: Settings,        href: "/settings" },
];

export function Sidebar() {
  return (
    <aside className="w-64 bg-card/45 border-r border-border/40 min-h-[calc(100vh-73px)] p-4 flex flex-col gap-6 hidden md:flex">
      <div className="flex flex-col gap-1">
        {menuItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.href}
              to={item.href}
              end={item.href === "/"}
              className={({ isActive }) =>
                `flex items-center gap-3 px-4 py-3 rounded-lg text-sm font-medium cursor-pointer transition-all duration-200 select-none border
                 ${isActive
                   ? "bg-primary/10 text-primary border-primary/20"
                   : "text-muted-foreground hover:bg-accent/40 hover:text-foreground border-transparent"
                 }`
              }
            >
              {({ isActive }) => (
                <>
                  <motion.div whileHover={{ x: 2 }} transition={{ type: "spring", stiffness: 300 }}>
                    <Icon className={`h-4 w-4 ${isActive ? "text-primary" : ""}`} />
                  </motion.div>
                  <span>{item.label}</span>
                </>
              )}
            </NavLink>
          );
        })}
      </div>

      {/* Bottom section */}
      <div className="mt-auto">
        <div className="rounded-lg bg-primary/5 border border-primary/15 p-4 flex flex-col gap-2">
          <span className="text-xs font-bold text-primary uppercase tracking-wider">ARIP v1.0</span>
          <p className="text-[11px] text-muted-foreground leading-relaxed">
            Multi-Agent Resume Intelligence Platform
          </p>
        </div>
      </div>
    </aside>
  );
}
