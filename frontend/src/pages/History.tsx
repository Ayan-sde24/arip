import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  Search,
  SlidersHorizontal,
  Trash2,
  Play,
  Calendar,
  ChevronDown,
} from "lucide-react";
import { MOCK_ANALYSES, type MockAnalysis } from "../services/mockData";
import { PageContainer, ResponsiveGrid } from "../components/layout/Containers";
import { GlassCard } from "../components/cards/Cards";
import { Badge } from "../components/ui/Badge";
import { ScoreRing } from "../components/ui/Progress";

export function History() {
  const navigate = useNavigate();
  const [runs, setRuns] = useState<MockAnalysis[]>(MOCK_ANALYSES);
  const [search, setSearch] = useState("");
  const [filterRole, setFilterRole] = useState("all");
  const [sortBy, setSortBy] = useState<"date" | "score">("date");

  // Client-side search and filtering
  const filtered = runs
    .filter((run) => {
      const matchSearch =
        run.candidateName.toLowerCase().includes(search.toLowerCase()) ||
        run.role.toLowerCase().includes(search.toLowerCase()) ||
        run.id.toLowerCase().includes(search.toLowerCase());

      const matchRole =
        filterRole === "all" || run.role.toLowerCase().includes(filterRole.toLowerCase());

      return matchSearch && matchRole;
    })
    .sort((a, b) => {
      if (sortBy === "date") return new Date(b.date).getTime() - new Date(a.date).getTime();
      return b.scores.overall - a.scores.overall;
    });

  function handleDelete(id: string) {
    setRuns((prev) => prev.filter((r) => r.id !== id));
  }

  const uniqueRoles = Array.from(new Set(runs.map((r) => r.role)));

  return (
    <PageContainer>
      <div className="flex flex-col gap-6 w-full">
        {/* Header */}
        <div>
          <h1 className="text-3xl font-black tracking-tight text-foreground">Analysis History</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Browse and query previous audit evaluations run on this machine.
          </p>
        </div>

        {/* ── SEARCH & FILTERS TOOLBAR ────────────────────────────────────── */}
        <div className="flex flex-wrap items-center gap-3 bg-card/25 border border-border/40 p-4 rounded-2xl w-full">
          {/* Search Input */}
          <div className="flex-1 min-w-[200px] relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <input
              type="text"
              placeholder="Search candidate, role, run ID…"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="w-full bg-accent/20 border border-border/60 rounded-lg pl-9 pr-4 py-2 text-xs text-foreground placeholder:text-muted-foreground/60 focus:outline-none focus:border-primary/40"
            />
          </div>

          {/* Role Filter Dropdown */}
          <div className="relative min-w-[150px]">
            <SlidersHorizontal className="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground" />
            <select
              value={filterRole}
              onChange={(e) => setFilterRole(e.target.value)}
              className="w-full bg-accent/20 border border-border/60 rounded-lg pl-9 pr-8 py-2 text-xs text-foreground appearance-none focus:outline-none focus:border-primary/40"
            >
              <option value="all">All Roles</option>
              {uniqueRoles.map((role) => (
                <option key={role} value={role}>
                  {role}
                </option>
              ))}
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground pointer-events-none" />
          </div>

          {/* Sort selection */}
          <div className="relative min-w-[130px]">
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as any)}
              className="w-full bg-accent/20 border border-border/60 rounded-lg px-3 py-2 text-xs text-foreground appearance-none focus:outline-none focus:border-primary/40"
            >
              <option value="date">Sort by Date</option>
              <option value="score">Sort by Score</option>
            </select>
            <ChevronDown className="absolute right-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-muted-foreground pointer-events-none" />
          </div>
        </div>

        {/* ── CARD GRID ────────────────────────────────────────────────────── */}
        <AnimatePresence mode="popLayout">
          {filtered.length === 0 ? (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              className="py-20 text-center text-xs text-muted-foreground"
            >
              No matching records found.
            </motion.div>
          ) : (
            <ResponsiveGrid cols={2} className="w-full">
              {filtered.map((run) => (
                <motion.div
                  key={run.id}
                  layout
                  initial={{ opacity: 0, scale: 0.96 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.96 }}
                  transition={{ duration: 0.2 }}
                >
                  <GlassCard className="p-5 flex items-center justify-between gap-5 relative border-border/40 hover:border-primary/20 transition-all">
                    {/* Run info */}
                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 flex-wrap">
                        <Badge variant="success">Parsed</Badge>
                        <span className="text-[10px] font-bold text-muted-foreground">{run.id}</span>
                      </div>
                      <h3 className="font-bold text-sm text-foreground mt-2 truncate">
                        {run.candidateName}
                      </h3>
                      <p className="text-xs text-muted-foreground truncate">{run.role}</p>

                      <div className="flex items-center gap-2 mt-4 text-[10px] text-muted-foreground font-medium">
                        <Calendar className="h-3.5 w-3.5" />
                        {run.date}
                      </div>

                      {/* Item controls */}
                      <div className="flex items-center gap-3 mt-4 pt-3 border-t border-border/20">
                        <button
                          onClick={() => navigate(`/report/${run.id}`)}
                          className="flex items-center gap-1.5 text-xs font-semibold text-primary hover:text-primary/80 transition-colors"
                        >
                          <Play className="h-3 w-3 fill-current" />
                          Reopen Analysis
                        </button>
                        <button
                          onClick={() => handleDelete(run.id)}
                          className="flex items-center gap-1.5 text-xs font-semibold text-destructive hover:text-destructive/80 transition-colors ml-auto"
                        >
                          <Trash2 className="h-3 w-3" />
                          Delete
                        </button>
                      </div>
                    </div>

                    {/* Overall Score ring */}
                    <div className="shrink-0">
                      <ScoreRing score={run.scores.overall} size={70} strokeWidth={5} />
                    </div>
                  </GlassCard>
                </motion.div>
              ))}
            </ResponsiveGrid>
          )}
        </AnimatePresence>
      </div>
    </PageContainer>
  );
}
