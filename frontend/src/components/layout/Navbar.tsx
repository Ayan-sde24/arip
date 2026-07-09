import { motion } from "framer-motion";
import { Link, useLocation } from "react-router-dom";
import { Bot, Upload } from "lucide-react";
import { ThemeToggle } from "../ui/Utilities";
import { Button } from "../ui/Button";

export function Navbar() {
  const { pathname } = useLocation();
  const isHome = pathname === "/";

  return (
    <motion.nav
      initial={{ y: -10, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="sticky top-0 z-40 w-full bg-background/60 backdrop-blur-md border-b border-border/40 px-6 py-4 flex items-center justify-between"
    >
      {/* Brand */}
      <Link to="/" className="flex items-center gap-2 group">
        <Bot className="h-6 w-6 text-primary group-hover:animate-glow-pulse transition-all" />
        <span className="font-semibold text-lg tracking-tight bg-gradient-to-r from-primary to-indigo-400 bg-clip-text text-transparent">
          ARIP
        </span>
      </Link>

      {/* Nav links (desktop) */}
      <div className="hidden md:flex items-center gap-1">
        {[
          { label: "Home",    href: "/" },
          { label: "Analyze", href: "/upload" },
          { label: "Demo Report", href: "/report/demo" },
        ].map((link) => (
          <Link
            key={link.href}
            to={link.href}
            className={`px-3 py-2 rounded-lg text-sm font-medium transition-colors
              ${pathname === link.href
                ? "text-foreground bg-accent/50"
                : "text-muted-foreground hover:text-foreground hover:bg-accent/30"
              }`}
          >
            {link.label}
          </Link>
        ))}
      </div>

      {/* Right actions */}
      <div className="flex items-center gap-3">
        <ThemeToggle />
        {!isHome && (
          <Link
            to="/upload"
            className="hidden sm:inline-flex items-center gap-2 h-9 px-4 rounded-lg text-sm font-medium bg-primary text-primary-foreground hover:bg-primary/90 transition-colors"
          >
            <Upload className="h-3.5 w-3.5" />
            New Analysis
          </Link>
        )}
      </div>
    </motion.nav>
  );
}
