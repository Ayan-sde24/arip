import { Search } from "lucide-react";
import { useCommandPaletteStore } from "../../store";

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
