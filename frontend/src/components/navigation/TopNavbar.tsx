import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { Bot, Menu, Search } from "lucide-react";
import { useSidebarStore, useCommandPaletteStore } from "../../store";
import { ThemeSwitcher } from "./ThemeSwitcher";
import { SearchBar } from "./SearchBar";
import { NotificationDropdown } from "./NotificationDropdown";
import { UserDropdown } from "./UserDropdown";

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
        {/* Quick Search trigger on mobile */}
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
