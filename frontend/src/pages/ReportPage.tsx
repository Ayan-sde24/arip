import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import {
  ArrowLeft,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Download,
  Target,
  Sparkles,
} from "lucide-react";
import { getReport, type Recommendation } from "../services/api";
import { PageContainer, SectionContainer, ResponsiveGrid } from "../components/layout/Containers";
import { DashboardCard, GlassCard } from "../components/cards/Cards";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { ScoreRing, LinearProgress } from "../components/ui/Progress";
import { RadarChart, BarChart } from "../components/charts/Charts";
import { Alert, LoadingState, ErrorState } from "../components/feedback/Feedback";
import { Divider } from "../components/ui/Utilities";
import { staggerContainer, fadeInUp } from "../animations/variants";
import { cn } from "../lib/utils";

const PRIORITY_VARIANT = {
  high: "danger",
  medium: "warning",
  low: "new",
} as const;

function RecommendationCard({ rec }: { rec: Recommendation }) {
  return (
    <GlassCard className="flex gap-4 p-5">
      <div
        className={cn(
          "h-8 w-8 rounded-lg flex items-center justify-center shrink-0",
          rec.priority === "high"
            ? "bg-destructive/15"
            : rec.priority === "medium"
            ? "bg-warning/15"
            : "bg-muted"
        )}
      >
        {rec.priority === "high" ? (
          <AlertCircle className="h-4 w-4 text-destructive" />
        ) : rec.priority === "medium" ? (
          <TrendingUp className="h-4 w-4 text-warning" />
        ) : (
          <Sparkles className="h-4 w-4 text-muted-foreground" />
        )}
      </div>
      <div className="flex-1 min-w-0">
        <div className="flex items-center gap-2 mb-1 flex-wrap">
          <span className="font-semibold text-sm text-foreground">{rec.title}</span>
          <Badge variant={PRIORITY_VARIANT[rec.priority]}>{rec.priority}</Badge>
          <span className="text-[10px] uppercase tracking-wider text-muted-foreground font-semibold">
            {rec.category}
          </span>
        </div>
        <p className="text-xs text-muted-foreground leading-relaxed">{rec.detail}</p>
      </div>
    </GlassCard>
  );
}

// ── Demo data used when analysis_id = "demo" ──────────────────────────────────
const DEMO_REPORT = {
  analysis_id: "demo",
  scores: { ats_score: 78, recruiter_score: 71, semantic_score: 84, overall_score: 77 },
  recommendations: [
    {
      priority: "high" as const,
      category: "ATS Keywords",
      title: "Add missing infrastructure keywords",
      detail:
        'The job description mentions "Kubernetes", "Terraform", and "AWS ECS" — none of which appear in your resume. Add these to your skills section and weave them into relevant bullet points.',
    },
    {
      priority: "high" as const,
      category: "Recruiter Appeal",
      title: "Quantify your impact metrics",
      detail:
        "3 of your 5 experience bullet points lack measurable outcomes. Replace vague phrases like 'improved performance' with concrete figures such as 'reduced API latency by 40%'.",
    },
    {
      priority: "medium" as const,
      category: "Summary",
      title: "Rewrite your professional summary",
      detail:
        "Your current summary is generic. Target the exact role by including the job title, your years of relevant experience, and 2 specific technical strengths from the job description.",
    },
    {
      priority: "medium" as const,
      category: "Format",
      title: "Standardize date formats",
      detail:
        "Mixed date formats detected (e.g., 'Jan 2022' vs '2022-01'). Use consistent MM/YYYY format across all experience entries to improve ATS parse accuracy.",
    },
    {
      priority: "low" as const,
      category: "Skills",
      title: "Reorder skills by job relevance",
      detail:
        "Place Python, FastAPI, and PostgreSQL at the top of your skills section since these are the primary technical requirements for this role.",
    },
  ],
  ats_keywords_matched: ["Python", "FastAPI", "PostgreSQL", "REST API", "Docker", "CI/CD", "Git"],
  ats_keywords_missing: ["Kubernetes", "Terraform", "AWS ECS", "Redis", "Prometheus"],
  radar_data: [
    { subject: "Technical Skills", score: 88 },
    { subject: "Experience",       score: 72 },
    { subject: "Education",        score: 80 },
    { subject: "Projects",         score: 85 },
    { subject: "Communication",    score: 68 },
    { subject: "ATS Format",       score: 76 },
  ],
};

export function ReportPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const isDemo = id === "demo";

  const { data, isLoading, error } = useQuery({
    queryKey: ["report", id],
    queryFn: () => getReport(id!),
    enabled: !!id && !isDemo,
    staleTime: Infinity,
  });

  const report = isDemo ? DEMO_REPORT : data;

  if (!isDemo && isLoading) {
    return (
      <PageContainer>
        <LoadingState label="Loading your report…" />
      </PageContainer>
    );
  }

  if (!isDemo && error) {
    return (
      <PageContainer>
        <ErrorState description="Failed to load report. Please try again." />
      </PageContainer>
    );
  }

  if (!report) return null;

  const scoreBar = [
    { name: "ATS",       score: report.scores.ats_score },
    { name: "Recruiter", score: report.scores.recruiter_score },
    { name: "Semantic",  score: report.scores.semantic_score },
    { name: "Overall",   score: report.scores.overall_score },
  ];

  const highCount = report.recommendations.filter((r) => r.priority === "high").length;
  const medCount  = report.recommendations.filter((r) => r.priority === "medium").length;
  const lowCount  = report.recommendations.filter((r) => r.priority === "low").length;

  return (
    <PageContainer>
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="flex flex-col gap-8"
      >
        {/* Toolbar */}
        <motion.div variants={fadeInUp} className="flex items-center justify-between flex-wrap gap-4">
          <button
            onClick={() => navigate(-1)}
            className="flex items-center gap-2 text-sm text-muted-foreground hover:text-foreground transition-colors"
          >
            <ArrowLeft className="h-4 w-4" />
            Back
          </button>
          <div className="flex items-center gap-3">
            {isDemo && <Badge variant="warning">Demo Report</Badge>}
            <Badge variant="success">
              <CheckCircle className="h-3 w-3 mr-1" />
              Complete
            </Badge>
            <Button variant="outline" size="sm" className="flex items-center gap-1.5">
              <Download className="h-3.5 w-3.5" />
              Export PDF
            </Button>
          </div>
        </motion.div>

        {/* Page title */}
        <motion.div variants={fadeInUp}>
          <h1 className="text-3xl font-black tracking-tight text-foreground">
            Resume Intelligence Report
          </h1>
          <p className="text-muted-foreground text-sm mt-1">
            Analysis ID: {report.analysis_id} ·{" "}
            {report.recommendations.length} recommendations ·{" "}
            {highCount} critical, {medCount} moderate, {lowCount} minor
          </p>
        </motion.div>

        <Divider label="Score Overview" />

        {/* Score cards */}
        <motion.div variants={fadeInUp}>
          <ResponsiveGrid cols={4}>
            {scoreBar.map((s) => (
              <GlassCard key={s.name} className="flex flex-col items-center gap-3 py-6">
                <ScoreRing score={s.score} size={80} strokeWidth={6} />
                <span className="text-xs font-bold uppercase tracking-wider text-muted-foreground">
                  {s.name}
                </span>
              </GlassCard>
            ))}
          </ResponsiveGrid>
        </motion.div>

        {/* Charts */}
        <motion.div variants={fadeInUp}>
          <ResponsiveGrid cols={2}>
            <DashboardCard
              title="Competency Radar"
              subtitle="Score breakdown across resume dimensions"
            >
              <RadarChart data={report.radar_data} dataKey="score" angleKey="subject" height={260} />
            </DashboardCard>
            <DashboardCard
              title="Agent Score Comparison"
              subtitle="Per-agent scoring results"
            >
              <BarChart data={scoreBar} dataKey="score" xAxisKey="name" height={260} />
            </DashboardCard>
          </ResponsiveGrid>
        </motion.div>

        <Divider label="ATS Keyword Analysis" />

        {/* Keyword sections */}
        <motion.div variants={fadeInUp}>
          <ResponsiveGrid cols={2}>
            <GlassCard className="flex flex-col gap-3">
              <div className="flex items-center gap-2 mb-1">
                <CheckCircle className="h-4 w-4 text-success" />
                <span className="font-semibold text-sm text-foreground">
                  Matched Keywords
                </span>
                <Badge variant="success">{report.ats_keywords_matched.length}</Badge>
              </div>
              <LinearProgress value={(report.ats_keywords_matched.length / (report.ats_keywords_matched.length + report.ats_keywords_missing.length)) * 100} />
              <div className="flex flex-wrap gap-2 mt-1">
                {report.ats_keywords_matched.map((kw) => (
                  <span
                    key={kw}
                    className="px-2.5 py-1 rounded-full text-[11px] font-medium bg-success/10 text-success border border-success/20"
                  >
                    {kw}
                  </span>
                ))}
              </div>
            </GlassCard>

            <GlassCard className="flex flex-col gap-3">
              <div className="flex items-center gap-2 mb-1">
                <Target className="h-4 w-4 text-destructive" />
                <span className="font-semibold text-sm text-foreground">
                  Missing Keywords
                </span>
                <Badge variant="danger">{report.ats_keywords_missing.length}</Badge>
              </div>
              <Alert
                variant="warning"
                description="Add these to your resume to improve ATS score."
              />
              <div className="flex flex-wrap gap-2 mt-1">
                {report.ats_keywords_missing.map((kw) => (
                  <span
                    key={kw}
                    className="px-2.5 py-1 rounded-full text-[11px] font-medium bg-destructive/10 text-destructive border border-destructive/20"
                  >
                    + {kw}
                  </span>
                ))}
              </div>
            </GlassCard>
          </ResponsiveGrid>
        </motion.div>

        <Divider label="Recommendations" />

        {/* Recommendations list */}
        <motion.div variants={staggerContainer} className="flex flex-col gap-4">
          {report.recommendations.map((rec, i) => (
            <motion.div key={i} variants={fadeInUp} custom={i}>
              <RecommendationCard rec={rec} />
            </motion.div>
          ))}
        </motion.div>

        {/* Bottom CTA */}
        <motion.div variants={fadeInUp}>
          <SectionContainer className="flex flex-col items-center gap-4 py-10 text-center">
            <h3 className="text-xl font-bold text-foreground">
              Ready to apply these improvements?
            </h3>
            <p className="text-sm text-muted-foreground max-w-md">
              Your optimized resume is ready to download, pre-populated with all
              keyword suggestions and rewritten bullet points.
            </p>
            <div className="flex gap-3 flex-wrap justify-center">
              <Button variant="gradient" size="lg" className="flex items-center gap-2">
                <Download className="h-4 w-4" />
                Download Optimized Resume
              </Button>
              <Button variant="outline" size="lg" onClick={() => navigate("/upload")}>
                Analyze Another Resume
              </Button>
            </div>
          </SectionContainer>
        </motion.div>
      </motion.div>
    </PageContainer>
  );
}
