import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import {
  ArrowLeft,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Download,
  Target,
  Sparkles,
  Zap,
  ChevronRight,
} from "lucide-react";
import { PageContainer, SectionContainer, ResponsiveGrid } from "../components/layout/Containers";
import { DashboardCard, GlassCard } from "../components/cards/Cards";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { ScoreRing, LinearProgress } from "../components/ui/Progress";
import { RadarChart, BarChart } from "../components/charts/Charts";
import { Alert } from "../components/feedback/Feedback";
import { Divider } from "../components/ui/Utilities";
import { staggerContainer, fadeInUp } from "../animations/variants";
import { MOCK_RADAR_DATA } from "../services/mockData";
import { cn } from "../lib/utils";

const PRIORITY_VARIANT = {
  high: "danger",
  medium: "warning",
  low: "new",
} as const;

export function ResultsPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<"all" | "high" | "medium" | "low">("all");

  const report = {
    analysis_id: id || "demo",
    scores: { ats_score: 88, recruiter_score: 80, semantic_score: 84, overall_score: 85, optimization_score: 88 },
    recommendations: [
      {
        priority: "high" as const,
        category: "ATS Keywords",
        title: "Integrate Kubernetes & AWS ECS",
        detail: 'The job description lists Kubernetes and AWS ECS as preferred skills. Weaving these directly into your Summary or Skills sections will significantly boost your score.',
      },
      {
        priority: "high" as const,
        category: "Recruiter Appeal",
        title: "Quantify Client Retention Metrics",
        detail: "3 experience statements describe metrics qualitatively. Highlight hard metrics such as 'increased retention by 12%' rather than just 'improving growth'.",
      },
      {
        priority: "medium" as const,
        category: "Summary",
        title: "Align Summary with Senior Role",
        detail: "Target the exact role title 'Senior Full Stack Engineer (AI Platform)' inside your summary to align with initial recruiter screens.",
      },
      {
        priority: "medium" as const,
        category: "Formatting",
        title: "Resolve Date Format Inconsistencies",
        detail: "Standardize date intervals (e.g. use '2020 - 2023' uniformly) to avoid ATS date range parser misreads.",
      },
      {
        priority: "low" as const,
        category: "Skills",
        title: "Inject Caching Skillsets",
        detail: "Add Redis references under backend skills. Redis is a preferred specification parameter inside the target job description.",
      },
    ],
    ats_keywords_matched: ["React", "TypeScript", "Node.js", "PostgreSQL", "REST APIs", "Docker", "Git"],
    ats_keywords_missing: ["Kubernetes", "AWS ECS", "Terraform", "Redis", "Prometheus"],
  };

  const highCount = report.recommendations.filter((r) => r.priority === "high").length;
  const medCount  = report.recommendations.filter((r) => r.priority === "medium").length;
  const lowCount  = report.recommendations.filter((r) => r.priority === "low").length;

  const filteredRecs = report.recommendations.filter((r) => {
    if (activeTab === "all") return true;
    return r.priority === activeTab;
  });

  const scoresBreakdown = [
    { name: "ATS Score",       score: report.scores.ats_score },
    { name: "Recruiter AI",    score: report.scores.recruiter_score },
    { name: "Semantic Match",   score: report.scores.semantic_score },
    { name: "Optimization",   score: report.scores.optimization_score },
  ];

  return (
    <PageContainer>
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="flex flex-col gap-8 w-full"
      >
        {/* Toolbar */}
        <motion.div variants={fadeInUp} className="flex items-center justify-between flex-wrap gap-4 shrink-0">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-xs font-semibold text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            Back to Workspace
          </button>
          <div className="flex items-center gap-3">
            <Badge variant="success">
              <CheckCircle className="h-3 w-3 mr-1" />
              Audit Complete
            </Badge>
            <Button variant="outline" size="sm" className="flex items-center gap-1.5">
              <Download className="h-3.5 w-3.5" />
              Export PDF
            </Button>
          </div>
        </motion.div>

        {/* Header */}
        <motion.div variants={fadeInUp}>
          <h1 className="text-3xl font-black tracking-tight text-foreground">Optimization Results Dashboard</h1>
          <p className="text-sm text-muted-foreground mt-1">
            Analysis ID: {report.analysis_id} · {report.recommendations.length} action items · {highCount} critical recommendations.
          </p>
        </motion.div>

        <Divider label="Audit Metric Breakdown" />

        {/* Scores circular ring dashboard */}
        <motion.div variants={fadeInUp}>
          <ResponsiveGrid cols={4}>
            {scoresBreakdown.map((s, idx) => (
              <GlassCard key={idx} className="flex flex-col items-center gap-3 py-6 relative overflow-hidden">
                <ScoreRing score={s.score} size={84} strokeWidth={6} />
                <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground mt-1">
                  {s.name}
                </span>
              </GlassCard>
            ))}
          </ResponsiveGrid>
        </motion.div>

        {/* Charts & Competencies breakdown */}
        <motion.div variants={fadeInUp}>
          <ResponsiveGrid cols={2}>
            <DashboardCard title="Competency Distribution" subtitle="Normalized dimensions of parsed work experience">
              <RadarChart data={MOCK_RADAR_DATA} dataKey="score" angleKey="subject" height={240} />
            </DashboardCard>
            <DashboardCard title="Agent Calibration comparison" subtitle="Scoring variations by auditing module">
              <BarChart data={scoresBreakdown} dataKey="score" xAxisKey="name" height={240} />
            </DashboardCard>
          </ResponsiveGrid>
        </motion.div>

        <Divider label="Skills Matching & Gap Analysis" />

        {/* Matched vs Missing Skillsets */}
        <motion.div variants={fadeInUp}>
          <ResponsiveGrid cols={2}>
            <GlassCard className="flex flex-col gap-3">
              <div className="flex items-center gap-2 mb-1">
                <CheckCircle className="h-4 w-4 text-success" />
                <span className="font-bold text-xs text-foreground uppercase tracking-wider">Matched Skillset Keywords</span>
                <Badge variant="success" className="text-[10px]">{report.ats_keywords_matched.length}</Badge>
              </div>
              <LinearProgress
                value={
                  (report.ats_keywords_matched.length /
                    (report.ats_keywords_matched.length + report.ats_keywords_missing.length)) *
                  100
                }
              />
              <div className="flex flex-wrap gap-1.5 mt-2">
                {report.ats_keywords_matched.map((kw) => (
                  <span
                    key={kw}
                    className="px-2.5 py-1 rounded-full text-[10px] font-medium bg-success/10 text-success border border-success/20"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            </GlassCard>

            <GlassCard className="flex flex-col gap-3">
              <div className="flex items-center gap-2 mb-1">
                <Target className="h-4 w-4 text-destructive" />
                <span className="font-bold text-xs text-foreground uppercase tracking-wider">Missing Skillset Gaps</span>
                <Badge variant="danger" className="text-[10px]">{report.ats_keywords_missing.length}</Badge>
              </div>
              <Alert
                variant="warning"
                description="Inject these terms to prevent automatic filtering in enterprise applicant systems."
              />
              <div className="flex flex-wrap gap-1.5 mt-2">
                {report.ats_keywords_missing.map((kw) => (
                  <span
                    key={kw}
                    className="px-2.5 py-1 rounded-full text-[10px] font-medium bg-destructive/10 text-destructive border border-destructive/20"
                  >
                    + {kw}
                  </span>
                ))}
              </div>
            </GlassCard>
          </ResponsiveGrid>
        </motion.div>

        <Divider label="Audit Action Items" />

        {/* Recommendations list with tabs */}
        <motion.div variants={fadeInUp} className="flex flex-col gap-4">
          <div className="flex items-center gap-2 overflow-x-auto pb-1">
            {[
              { id: "all",    label: `All Items (${report.recommendations.length})` },
              { id: "high",   label: `Critical (${highCount})` },
              { id: "medium", label: `Moderate (${medCount})` },
              { id: "low",    label: `Minor (${lowCount})` },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={cn(
                  "px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors border",
                  activeTab === tab.id
                    ? "bg-primary/10 text-primary border-primary/20"
                    : "text-muted-foreground hover:bg-accent/40 hover:text-foreground border-transparent"
                )}
              >
                {tab.label}
              </button>
            ))}
          </div>

          <div className="flex flex-col gap-3">
            {filteredRecs.map((rec, i) => (
              <GlassCard key={i} className="flex gap-4 p-5 border-border/40 hover:border-primary/15 transition-all">
                <div
                  className={cn(
                    "h-8 w-8 rounded-lg flex items-center justify-center shrink-0 mt-0.5",
                    rec.priority === "high"
                      ? "bg-destructive/10"
                      : rec.priority === "medium"
                      ? "bg-warning/10"
                      : "bg-primary/10"
                  )}
                >
                  {rec.priority === "high" ? (
                    <AlertCircle className="h-4 w-4 text-destructive" />
                  ) : rec.priority === "medium" ? (
                    <TrendingUp className="h-4 w-4 text-warning" />
                  ) : (
                    <Sparkles className="h-4 w-4 text-primary" />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2.5 flex-wrap">
                    <span className="text-xs font-bold text-foreground">{rec.title}</span>
                    <Badge variant={PRIORITY_VARIANT[rec.priority]}>{rec.priority}</Badge>
                    <span className="text-[9px] uppercase tracking-wider text-muted-foreground font-semibold">
                      {rec.category}
                    </span>
                  </div>
                  <p className="text-xs text-muted-foreground mt-1 leading-relaxed">
                    {rec.detail}
                  </p>
                </div>
              </GlassCard>
            ))}
          </div>
        </motion.div>

        {/* Transition call to action */}
        <motion.div variants={fadeInUp}>
          <SectionContainer className="flex flex-col items-center gap-4 py-8 text-center glass-panel border-border/40">
            <Zap className="h-8 w-8 text-primary" />
            <div>
              <h3 className="text-lg font-bold text-foreground">Interactive AI Resume Optimizer</h3>
              <p className="text-xs text-muted-foreground max-w-md mt-1 leading-relaxed">
                Launch the split-pane AI Resume Optimizer to interactively review suggested changes and apply optimizations to your final copy.
              </p>
            </div>
            <Button
              variant="gradient"
              size="lg"
              onClick={() => navigate("/coach")}
              className="flex items-center gap-2"
            >
              Open AI Resume Coach
              <ChevronRight className="h-4 w-4" />
            </Button>
          </SectionContainer>
        </motion.div>
      </motion.div>
    </PageContainer>
  );
}
