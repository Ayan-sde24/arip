import * as React from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useQuery } from "@tanstack/react-query";
import { ArrowRight, CheckCircle, Loader2, XCircle, Clock } from "lucide-react";
import { getAnalysis, type AgentResult } from "../services/api";
import { GlassPanel } from "../components/layout/Containers";
import { GlassCard } from "../components/cards/Cards";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { LinearProgress, ScoreRing } from "../components/ui/Progress";
import { staggerContainer, fadeInUp } from "../animations/variants";
import { cn } from "../lib/utils";

const AGENT_META: Record<string, { label: string; description: string }> = {
  parser: {
    label: "Document Parser",
    description: "Extracting sections, entities, and structured data.",
  },
  semantic: {
    label: "Semantic Matcher",
    description: "Computing conceptual alignment with job requirements.",
  },
  ats: {
    label: "ATS Intelligence",
    description: "Evaluating ATS keyword density and format compliance.",
  },
  recruiter: {
    label: "Recruiter Agent",
    description: "Simulating recruiter evaluation of impact and narrative.",
  },
  coach: {
    label: "Resume Coach",
    description: "Generating optimized rewrites and keyword suggestions.",
  },
};

function AgentStatusIcon({ status }: { status: AgentResult["status"] }) {
  if (status === "completed") return <CheckCircle className="h-4 w-4 text-success" />;
  if (status === "failed") return <XCircle className="h-4 w-4 text-destructive" />;
  if (status === "running") return <Loader2 className="h-4 w-4 text-primary animate-spin" />;
  return <Clock className="h-4 w-4 text-muted-foreground" />;
}

function agentVariant(status: AgentResult["status"]) {
  if (status === "completed") return "success" as const;
  if (status === "failed") return "danger" as const;
  if (status === "running") return "ai" as const;
  return "new" as const;
}

export function AnalysisPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const { data, error } = useQuery({
    queryKey: ["analysis", id],
    queryFn: () => getAnalysis(id!),
    refetchInterval: (data) =>
      data?.state?.data?.status === "completed" || data?.state?.data?.status === "failed"
        ? false
        : 2500,
    enabled: !!id,
  });

  const isComplete = data?.status === "completed";
  const isFailed = data?.status === "failed";

  const agents: AgentResult[] = data?.agents ?? [
    { agent: "parser",    status: "pending" },
    { agent: "semantic",  status: "pending" },
    { agent: "ats",       status: "pending" },
    { agent: "recruiter", status: "pending" },
    { agent: "coach",     status: "pending" },
  ];

  const completedCount = agents.filter((a) => a.status === "completed").length;
  const progressPct = Math.round((completedCount / agents.length) * 100);

  return (
    <div className="max-w-3xl mx-auto px-6 py-16">
      <motion.div
        variants={staggerContainer}
        initial="hidden"
        animate="visible"
        className="flex flex-col gap-8"
      >
        {/* Header */}
        <motion.div variants={fadeInUp} className="text-center">
          <Badge variant="ai" className="mb-4">Step 2 of 2</Badge>
          <h1 className="text-4xl font-black tracking-tight text-foreground mb-3">
            {isComplete ? "Analysis Complete" : isFailed ? "Analysis Failed" : "Running Analysis"}
          </h1>
          <p className="text-muted-foreground">
            {isComplete
              ? `${data?.candidate_name ? `${data.candidate_name} · ` : ""}${data?.job_title ?? "Role"} · Analysis ID: ${id}`
              : isFailed
              ? "An error occurred during analysis. Please try again."
              : "Your multi-agent pipeline is running. Results appear below as each agent completes."}
          </p>
        </motion.div>

        {/* Overall progress bar */}
        {!isFailed && (
          <motion.div variants={fadeInUp}>
            <GlassPanel className="flex flex-col gap-3">
              <div className="flex items-center justify-between text-sm">
                <span className="font-medium text-foreground">Pipeline Progress</span>
                <span className="text-muted-foreground text-xs">{completedCount}/{agents.length} agents</span>
              </div>
              <LinearProgress value={progressPct} />
              {isComplete && (
                <p className="text-xs text-success font-medium">
                  ✓ All agents completed successfully
                </p>
              )}
            </GlassPanel>
          </motion.div>
        )}

        {/* Agent cards */}
        <motion.div variants={staggerContainer} className="flex flex-col gap-4">
          {agents.map((agent, i) => {
            const meta = AGENT_META[agent.agent] ?? {
              label: agent.agent,
              description: "Processing…",
            };
            return (
              <motion.div key={agent.agent} variants={fadeInUp} custom={i}>
                <GlassCard
                  className={cn(
                    "flex items-center gap-5 px-5 py-4 transition-all duration-300",
                    agent.status === "running" && "border-primary/40 bg-primary/5"
                  )}
                >
                  <div className="shrink-0">
                    <AgentStatusIcon status={agent.status} />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-0.5">
                      <span className="font-semibold text-sm text-foreground">
                        {meta.label}
                      </span>
                      <Badge variant={agentVariant(agent.status)} className="text-[9px] py-0">
                        {agent.status}
                      </Badge>
                    </div>
                    <p className="text-xs text-muted-foreground truncate">{meta.description}</p>
                  </div>
                  {agent.score !== undefined && (
                    <div className="shrink-0">
                      <ScoreRing score={agent.score} size={52} strokeWidth={4} />
                    </div>
                  )}
                </GlassCard>
              </motion.div>
            );
          })}
        </motion.div>

        {/* Scores summary — visible when complete */}
        {isComplete && data?.scores && (
          <motion.div
            variants={fadeInUp}
            initial="hidden"
            animate="visible"
          >
            <GlassPanel className="flex flex-col gap-4">
              <h3 className="font-semibold text-sm text-foreground">Score Summary</h3>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: "ATS Score",       value: data.scores.ats_score },
                  { label: "Recruiter Score",  value: data.scores.recruiter_score },
                  { label: "Semantic Match",   value: data.scores.semantic_score },
                  { label: "Overall",          value: data.scores.overall_score },
                ].map((s) => (
                  <div key={s.label} className="flex flex-col items-center gap-2">
                    <ScoreRing score={s.value} size={64} strokeWidth={5} />
                    <span className="text-[10px] font-semibold uppercase tracking-wider text-muted-foreground text-center">
                      {s.label}
                    </span>
                  </div>
                ))}
              </div>
            </GlassPanel>
          </motion.div>
        )}

        {/* CTA */}
        {isComplete && (
          <motion.div variants={fadeInUp} className="flex justify-center">
            <Button
              variant="gradient"
              size="lg"
              onClick={() => navigate(`/report/${id}`)}
              className="flex items-center gap-2"
            >
              View Full Report
              <ArrowRight className="h-4 w-4" />
            </Button>
          </motion.div>
        )}

        {isFailed && (
          <motion.div variants={fadeInUp} className="flex justify-center">
            <Button
              variant="outline"
              size="lg"
              onClick={() => navigate("/upload")}
            >
              Try Again
            </Button>
          </motion.div>
        )}

        {error && (
          <motion.div variants={fadeInUp}>
            <GlassPanel className="text-center py-4">
              <p className="text-xs text-destructive">
                Error loading analysis. Please refresh or try again.
              </p>
            </GlassPanel>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
