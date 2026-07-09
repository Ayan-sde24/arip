import { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import {
  CheckCircle,
  Loader2,
  AlertCircle,
  Clock,
  Terminal,
  ArrowRight,
  Brain,
  FileText,
  Briefcase,
} from "lucide-react";
import {
  MOCK_RESUME_TEXT,
  MOCK_JD_TEXT,
} from "../services/mockData";
import { GlassCard } from "../components/cards/Cards";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { useAIStatusStore } from "../store";

interface PipelineStage {
  id: string;
  label: string;
  status: "idle" | "running" | "completed" | "error";
  time?: string;
  log?: string;
}

const INITIAL_STAGES: PipelineStage[] = [
  { id: "uploaded",  label: "Resume Uploaded",      status: "idle", time: "0.2s", log: "Parsing PDF file stream successfully" },
  { id: "doc_intel", label: "Document Intelligence", status: "idle", time: "0.8s", log: "Extracting block segments and hierarchy" },
  { id: "res_build", label: "Resume Builder",       status: "idle", time: "0.5s", log: "Compiling structures to normalized JSON schemas" },
  { id: "job_build", label: "Job Builder",          status: "idle", time: "0.4s", log: "Deconstructing job spec requirement entities" },
  { id: "semantic",  label: "Semantic Engine",      status: "idle", time: "1.2s", log: "Calculating similarity vector dot products" },
  { id: "ats",       label: "ATS Agent",            status: "idle", time: "0.7s", log: "Scanning density margins and date consistency" },
  { id: "recruiter", label: "Recruiter Agent",      status: "idle", time: "1.1s", log: "Auditing career metric indicators and wording" },
  { id: "coach",     label: "Resume Coach",         status: "idle", time: "0.9s", log: "Compiling replacement candidate suggest sentences" },
  { id: "report",    label: "Report Generation",    status: "idle", time: "0.3s", log: "Formulating scoring matrices files" },
];

export function AnalysisWorkspace() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [stages, setStages] = useState<PipelineStage[]>(INITIAL_STAGES);
  const [activeStep, setActiveStep] = useState(0);
  const [terminalLogs, setTerminalLogs] = useState<string[]>([]);
  const [processing, setProcessing] = useState(true);
  const setStoreAgents = useAIStatusStore((s) => s.setAgents);
  const updateStoreAgent = useAIStatusStore((s) => s.updateAgent);

  // Set store visibility when workspace mounts
  useEffect(() => {
    setStoreAgents(
      INITIAL_STAGES.map((s) => ({
        id: s.id,
        label: s.label,
        status: "idle",
      }))
    );
  }, [setStoreAgents]);

  useEffect(() => {
    if (activeStep >= stages.length) {
      setProcessing(false);
      return;
    }

    // Set active stage to running
    const updated = stages.map((s, idx) => {
      if (idx === activeStep) return { ...s, status: "running" as const };
      if (idx < activeStep) return { ...s, status: "completed" as const };
      return s;
    });
    setStages(updated);

    // Update global store
    updateStoreAgent(stages[activeStep].id, { status: "processing" });

    // Append log
    const current = stages[activeStep];
    setTerminalLogs((prev) => [
      ...prev,
      `[AI Workspace] [${new Date().toLocaleTimeString()}] Starting: ${current.label}...`,
      `[AI Workspace] [${new Date().toLocaleTimeString()}] Log: ${current.log}`,
    ]);

    // Transition timers
    const timer = setTimeout(() => {
      // Set active stage to completed
      setStages((prev) =>
        prev.map((s, idx) => {
          if (idx === activeStep) return { ...s, status: "completed" as const };
          return s;
        })
      );
      updateStoreAgent(stages[activeStep].id, { status: "completed", progress: 100 });

      setTerminalLogs((prev) => [
        ...prev,
        `[AI Workspace] [${new Date().toLocaleTimeString()}] Done: ${current.label} (took ${current.time})`,
      ]);

      setActiveStep((a) => a + 1);
    }, 1200);

    return () => clearTimeout(timer);
  }, [activeStep]); // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="flex flex-col h-[calc(100vh-56px)] bg-background select-none">
      {/* Top action header */}
      <div className="border-b border-border/40 bg-card/20 px-6 py-3 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <Badge variant="ai">Running</Badge>
          <span className="text-xs font-bold text-foreground">Workspace Run: {id}</span>
        </div>
        <AnimatePresence>
          {!processing && (
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
            >
              <Button
                variant="gradient"
                size="sm"
                onClick={() => navigate(`/report/${id || "demo"}`)}
                className="flex items-center gap-2"
              >
                View Full Results
                <ArrowRight className="h-4 w-4" />
              </Button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* ── THREE-COLUMN WORKSPACE ────────────────────────────────────────── */}
      <div className="flex-1 flex overflow-hidden w-full">
        {/* LEFT COLUMN: Resume Text */}
        <div className="w-[30%] border-r border-border/40 flex flex-col bg-card/10 overflow-hidden">
          <div className="px-4 py-3 border-b border-border/40 flex items-center gap-2 bg-card/25 shrink-0">
            <FileText className="h-4 w-4 text-primary" />
            <span className="text-xs font-bold text-foreground uppercase tracking-wider">Source Resume</span>
          </div>
          <div className="flex-1 p-5 overflow-y-auto font-mono text-[10px] text-muted-foreground whitespace-pre-wrap leading-relaxed select-text">
            {MOCK_RESUME_TEXT}
          </div>
        </div>

        {/* CENTER COLUMN: AI Pipeline */}
        <div className="w-[40%] flex flex-col overflow-y-auto p-5 gap-4 bg-background">
          <div className="flex items-center gap-2 border-b border-border/20 pb-3 mb-2 shrink-0">
            <Brain className="h-4 w-4 text-primary" />
            <span className="text-xs font-bold text-foreground uppercase tracking-wider">Multi-Agent Processing Stack</span>
          </div>

          <div className="flex flex-col gap-2.5">
            {stages.map((stage, idx) => (
              <motion.div
                key={stage.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: idx * 0.05 }}
              >
                <GlassCard
                  className={`px-4 py-3 flex items-center justify-between transition-all duration-300 border border-border/40
                    ${stage.status === "running" ? "border-primary/50 bg-primary/5" : ""}
                    ${stage.status === "completed" ? "bg-success/3 border-success/15" : ""}
                  `}
                >
                  <div className="flex items-center gap-3">
                    {stage.status === "running" && <Loader2 className="h-4 w-4 text-primary animate-spin" />}
                    {stage.status === "completed" && <CheckCircle className="h-4 w-4 text-success" />}
                    {stage.status === "idle" && <Clock className="h-4 w-4 text-muted-foreground" />}
                    {stage.status === "error" && <AlertCircle className="h-4 w-4 text-destructive" />}

                    <span className={`text-xs font-bold
                      ${stage.status === "running" ? "text-primary" : "text-foreground/80"}
                      ${stage.status === "completed" ? "text-foreground" : ""}
                      ${stage.status === "idle" ? "text-muted-foreground" : ""}
                    `}>
                      {stage.label}
                    </span>
                  </div>

                  {stage.time && (stage.status === "completed" || stage.status === "running") && (
                    <span className="text-[10px] font-mono text-muted-foreground bg-accent/20 px-2 py-0.5 rounded">
                      {stage.time}
                    </span>
                  )}
                </GlassCard>
              </motion.div>
            ))}
          </div>
        </div>

        {/* RIGHT COLUMN: Job Description */}
        <div className="w-[30%] border-l border-border/40 flex flex-col bg-card/10 overflow-hidden">
          <div className="px-4 py-3 border-b border-border/40 flex items-center gap-2 bg-card/25 shrink-0">
            <Briefcase className="h-4 w-4 text-indigo-400" />
            <span className="text-xs font-bold text-foreground uppercase tracking-wider">Target Job Specification</span>
          </div>
          <div className="flex-1 p-5 overflow-y-auto font-mono text-[10px] text-muted-foreground whitespace-pre-wrap leading-relaxed select-text">
            {MOCK_JD_TEXT}
          </div>
        </div>
      </div>

      {/* BOTTOM PANEL: Live Audit Logs */}
      <div className="h-40 border-t border-border/40 flex flex-col bg-card/30 shrink-0">
        <div className="px-4 py-2 border-b border-border/40 flex items-center gap-2 bg-card/25 shrink-0">
          <Terminal className="h-3.5 w-3.5 text-primary" />
          <span className="text-[10px] font-bold text-foreground uppercase tracking-wider">Terminal Output stream</span>
        </div>
        <div className="flex-1 p-3 overflow-y-auto font-mono text-[10px] text-muted-foreground flex flex-col gap-1 select-text bg-black/40">
          {terminalLogs.map((log, i) => (
            <div key={i} className="flex gap-2">
              <span className="text-primary shrink-0">&gt;</span>
              <span>{log}</span>
            </div>
          ))}
          {processing && (
            <div className="flex items-center gap-1.5 text-primary">
              <span>&gt; Thinking...</span>
              <span className="animate-pulse">_</span>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
