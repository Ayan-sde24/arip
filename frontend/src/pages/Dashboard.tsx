import { useNavigate } from "react-router-dom";
import {
  Upload,
  FileText,
  History,
  TrendingUp,
  Activity,
  ArrowRight,
  PlusCircle,
  ChevronRight,
} from "lucide-react";
import { MOCK_ANALYSES } from "../services/mockData";
import { DashboardLayout } from "../layouts/DashboardLayout";
import { DashboardCard, GlassCard } from "../components/cards/Cards";
import { Badge } from "../components/ui/Badge";
import { ScoreRing } from "../components/ui/Progress";
import { BarChart, AreaChart } from "../components/charts/Charts";
import { Button } from "../components/ui/Button";

export function Dashboard() {
  const navigate = useNavigate();

  const activityLogs = [
    { time: "10 mins ago", text: "Successfully completed audit for Senior Full Stack Engineer", type: "success" },
    { time: "2 hours ago", text: "Updated ATS rules definitions database", type: "info" },
    { time: "1 day ago", text: "AI Coach suggested 4 critical skill additions to summary", type: "warning" },
  ];

  const averageScores = {
    overall: 86,
    ats: 89,
    recruiter: 83,
    semantic: 85,
  };

  const chartData = [
    { name: "Parser", score: 98 },
    { name: "ATS Agent", score: 89 },
    { name: "Recruiter AI", score: 83 },
    { name: "Semantic AI", score: 85 },
    { name: "Optimization", score: 92 },
  ];

  const trendData = [
    { date: "07/01", score: 72 },
    { date: "07/03", score: 78 },
    { date: "07/05", score: 85 },
    { date: "07/08", score: 91 },
  ];

  return (
    <DashboardLayout>
      <div className="flex flex-col gap-8 w-full">
        {/* Header */}
        <div className="flex items-center justify-between flex-wrap gap-4">
          <div>
            <h1 className="text-3xl font-black tracking-tight text-foreground">AI Workspace Dashboard</h1>
            <p className="text-sm text-muted-foreground mt-1">Monitor recent optimization runs and platform metrics.</p>
          </div>
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate("/history")}
              className="flex items-center gap-2"
            >
              <History className="h-4 w-4" />
              History
            </Button>
            <Button
              variant="gradient"
              size="sm"
              onClick={() => navigate("/upload")}
              className="flex items-center gap-2"
            >
              <PlusCircle className="h-4 w-4" />
              New Analysis
            </Button>
          </div>
        </div>

        {/* ── METRIC CARDS ─────────────────────────────────────────────────── */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 w-full">
          {[
            { label: "Overall Average", score: averageScores.overall },
            { label: "ATS Score",       score: averageScores.ats },
            { label: "Recruiter Score",  score: averageScores.recruiter },
            { label: "Semantic Score",   score: averageScores.semantic },
          ].map((item, idx) => (
            <GlassCard key={idx} className="flex flex-col items-center gap-3 py-6 relative overflow-hidden">
              <div className="absolute top-2 right-2 h-1.5 w-1.5 rounded-full bg-primary/40" />
              <ScoreRing score={item.score} size={76} strokeWidth={6} />
              <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground mt-2 text-center">
                {item.label}
              </span>
            </GlassCard>
          ))}
        </div>

        {/* ── CHARTS ───────────────────────────────────────────────────────── */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full">
          <DashboardCard title="Agent Score Breakdown" subtitle="Comparison of average scoring modules">
            <BarChart data={chartData} dataKey="score" xAxisKey="name" height={220} />
          </DashboardCard>
          <DashboardCard title="Score Improvement Path" subtitle="Chronological trend of optimization attempts">
            <AreaChart data={trendData} dataKey="score" xAxisKey="date" height={220} />
          </DashboardCard>
        </div>

        {/* ── RECENT ANALYSES & TIMELINE ────────────────────────────────────── */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 w-full">
          {/* Recent list */}
          <div className="lg:col-span-2 flex flex-col gap-4">
            <h3 className="text-sm font-bold text-foreground">Recent Optimization Runs</h3>
            <div className="flex flex-col gap-3">
              {MOCK_ANALYSES.map((run) => (
                <GlassCard
                  key={run.id}
                  onClick={() => navigate(`/report/${run.id}`)}
                  className="p-5 flex items-center justify-between gap-4 cursor-pointer hover:border-primary/30 transition-all border-border/40"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div className="h-10 w-10 rounded-xl bg-accent/20 flex items-center justify-center text-primary shrink-0 border border-border/40">
                      <FileText className="h-5 w-5" />
                    </div>
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-bold text-xs text-foreground truncate">{run.candidateName}</span>
                        <Badge variant="new" className="text-[9px] py-0">{run.id}</Badge>
                      </div>
                      <p className="text-xs text-muted-foreground mt-0.5 truncate">{run.role}</p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 shrink-0">
                    <div className="flex flex-col items-end">
                      <span className="text-sm font-black text-primary">{run.scores.overall}%</span>
                      <span className="text-[9px] text-muted-foreground uppercase font-semibold mt-0.5">{run.date}</span>
                    </div>
                    <ChevronRight className="h-4 w-4 text-muted-foreground" />
                  </div>
                </GlassCard>
              ))}
            </div>
          </div>

          {/* Quick Actions & Activity Feed */}
          <div className="flex flex-col gap-6">
            {/* Quick actions panel */}
            <div className="flex flex-col gap-3">
              <h3 className="text-sm font-bold text-foreground font-sans">Quick Actions</h3>
              <GlassCard
                onClick={() => navigate("/upload")}
                className="p-4 flex items-center justify-between border-border/40 hover:border-primary/20 cursor-pointer"
              >
                <div className="flex items-center gap-3">
                  <Upload className="h-4 w-4 text-primary" />
                  <span className="text-xs font-semibold text-foreground">Optimize New Resume</span>
                </div>
                <ArrowRight className="h-3 w-3 text-muted-foreground" />
              </GlassCard>
              <GlassCard
                onClick={() => navigate("/report/demo")}
                className="p-4 flex items-center justify-between border-border/40 hover:border-primary/20 cursor-pointer"
              >
                <div className="flex items-center gap-3">
                  <TrendingUp className="h-4 w-4 text-indigo-400" />
                  <span className="text-xs font-semibold text-foreground">See Sample Dashboard</span>
                </div>
                <ArrowRight className="h-3 w-3 text-muted-foreground" />
              </GlassCard>
            </div>

            {/* Platform logs feed */}
            <div className="flex flex-col gap-3">
              <h3 className="text-sm font-bold text-foreground">Platform Activity Feed</h3>
              <div className="flex flex-col gap-4 p-4 glass-panel border-border/40">
                {activityLogs.map((log, i) => (
                  <div key={i} className="flex gap-3 items-start last:border-0 pb-3 border-b border-border/20">
                    <Activity className="h-4 w-4 text-primary shrink-0 mt-0.5" />
                    <div>
                      <p className="text-xs text-foreground/80 leading-relaxed">{log.text}</p>
                      <span className="text-[10px] text-muted-foreground mt-1 block font-medium">{log.time}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
