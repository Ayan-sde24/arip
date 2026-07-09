import { motion, AnimatePresence } from "framer-motion";
import { CheckCircle, Loader2, XCircle, Bot, ChevronDown, ChevronUp, X } from "lucide-react";
import * as React from "react";
import { useAIStatusStore, type AgentStatus, type AgentState } from "../../store";
import { cn } from "../../lib/utils";

const STATUS_CONFIG: Record<AgentStatus, { color: string; label: string; pulse: boolean }> = {
  idle:       { color: "text-muted-foreground", label: "Idle",       pulse: false },
  processing: { color: "text-primary",          label: "Processing", pulse: true },
  completed:  { color: "text-success",          label: "Done",       pulse: false },
  error:      { color: "text-destructive",      label: "Error",      pulse: false },
};

function AgentRow({ agent }: { agent: AgentState }) {
  const cfg = STATUS_CONFIG[agent.status];
  return (
    <div className="flex items-center gap-2.5 py-1.5">
      <div className={cn("shrink-0", cfg.color)}>
        {agent.status === "completed" && <CheckCircle className="h-3.5 w-3.5" />}
        {agent.status === "error"     && <XCircle className="h-3.5 w-3.5" />}
        {agent.status === "processing" && (
          <Loader2 className="h-3.5 w-3.5 animate-spin" />
        )}
        {agent.status === "idle" && (
          <div className="h-1.5 w-1.5 rounded-full bg-muted-foreground/40 ml-1" />
        )}
      </div>
      <span className="text-xs font-medium text-foreground flex-1">{agent.label}</span>
      {agent.progress !== undefined && agent.status === "processing" && (
        <span className="text-[10px] text-muted-foreground shrink-0">{agent.progress}%</span>
      )}
      {agent.message && (
        <span className={cn("text-[10px] shrink-0", cfg.color)}>{cfg.label}</span>
      )}
    </div>
  );
}

export function AIStatusDock() {
  const { agents, isVisible, globalStatus, hide } = useAIStatusStore();
  const [expanded, setExpanded] = React.useState(true);
  const cfg = STATUS_CONFIG[globalStatus];

  return (
    <AnimatePresence>
      {isVisible && agents.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 24, scale: 0.95 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0, y: 24, scale: 0.95 }}
          transition={{ duration: 0.3, ease: [0.16, 1, 0.3, 1] }}
          className="fixed bottom-24 right-6 z-50 w-64 bg-card/95 border border-border/80 rounded-2xl shadow-2xl shadow-black/20 backdrop-blur-xl overflow-hidden"
        >
          {/* Header */}
          <div className="flex items-center gap-2.5 px-4 py-3 border-b border-border/30">
            <div className={cn("shrink-0 relative", cfg.color)}>
              <Bot className="h-4 w-4" />
              {cfg.pulse && (
                <span className="absolute -top-0.5 -right-0.5 h-2 w-2 bg-primary rounded-full animate-ping" />
              )}
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-xs font-bold text-foreground leading-none">AI Pipeline</p>
              <p className={cn("text-[10px] mt-0.5 font-medium", cfg.color)}>{cfg.label}</p>
            </div>
            <div className="flex items-center gap-1">
              <button
                onClick={() => setExpanded((e) => !e)}
                className="text-muted-foreground hover:text-foreground transition-colors p-0.5 rounded"
              >
                {expanded ? (
                  <ChevronDown className="h-3.5 w-3.5" />
                ) : (
                  <ChevronUp className="h-3.5 w-3.5" />
                )}
              </button>
              <button
                onClick={hide}
                className="text-muted-foreground hover:text-foreground transition-colors p-0.5 rounded"
              >
                <X className="h-3.5 w-3.5" />
              </button>
            </div>
          </div>

          {/* Agent list */}
          <AnimatePresence>
            {expanded && (
              <motion.div
                initial={{ height: 0 }}
                animate={{ height: "auto" }}
                exit={{ height: 0 }}
                className="overflow-hidden"
              >
                <div className="px-4 py-2 flex flex-col divide-y divide-border/20">
                  {agents.map((agent) => (
                    <AgentRow key={agent.id} agent={agent} />
                  ))}
                </div>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Status bar */}
          {globalStatus === "processing" && (
            <div className="h-0.5 bg-muted overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-primary via-indigo-400 to-primary"
                animate={{ x: ["-100%", "100%"] }}
                transition={{ duration: 1.8, repeat: Infinity, ease: "linear" }}
              />
            </div>
          )}
        </motion.div>
      )}
    </AnimatePresence>
  );
}
