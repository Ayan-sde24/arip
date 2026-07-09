import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  Sparkles,
  Check,
  X,
  Copy,
  CheckCheck,
  RotateCcw,
  FileEdit,
} from "lucide-react";
import { Badge } from "../components/ui/Badge";
import { Button } from "../components/ui/Button";
import { MOCK_RESUME_TEXT, MOCK_OPTIMIZER_CHANGES } from "../services/mockData";
import { cn } from "../lib/utils";

export function ResumeOptimizer() {
  const [suggestions, setSuggestions] = useState(MOCK_OPTIMIZER_CHANGES);
  const [selectedSuggestion, setSelectedSuggestion] = useState<string>("opt-1");
  const [originalResume, setOriginalResume] = useState(MOCK_RESUME_TEXT);
  const [copied, setCopied] = useState(false);

  function handleAccept(id: string) {
    const sug = suggestions.find((s) => s.id === id);
    if (!sug) return;

    // Apply replacement to original resume copy
    if (originalResume.includes(sug.original)) {
      setOriginalResume((prev) => prev.replace(sug.original, sug.suggested));
    }

    setSuggestions((prev) =>
      prev.map((s) => (s.id === id ? { ...s, accepted: true, rejected: false } : s))
    );
  }

  function handleReject(id: string) {
    setSuggestions((prev) =>
      prev.map((s) => (s.id === id ? { ...s, rejected: true, accepted: false } : s))
    );
  }

  function handleReset() {
    setOriginalResume(MOCK_RESUME_TEXT);
    setSuggestions(MOCK_OPTIMIZER_CHANGES);
  }

  function handleCopyToClipboard() {
    navigator.clipboard.writeText(originalResume);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  }

  const activeSuggestion = suggestions.find((s) => s.id === selectedSuggestion);

  return (
    <div className="flex flex-col h-[calc(100vh-56px)] bg-background">
      {/* Top bar */}
      <div className="border-b border-border/40 bg-card/20 px-6 py-3 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <Badge variant="premium">
            <Sparkles className="h-3 w-3 mr-1 text-primary animate-pulse" />
            AI Coach Engine
          </Badge>
          <span className="text-xs font-bold text-foreground">Interactive Inline Optimizer</span>
        </div>
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={handleReset}
            className="flex items-center gap-1.5"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            Reset
          </Button>
          <Button
            variant="gradient"
            size="sm"
            onClick={handleCopyToClipboard}
            className="flex items-center gap-1.5"
          >
            {copied ? (
              <>
                <CheckCheck className="h-3.5 w-3.5 text-white" />
                Copied!
              </>
            ) : (
              <>
                <Copy className="h-3.5 w-3.5" />
                Copy Final Resume
              </>
            )}
          </Button>
        </div>
      </div>

      {/* ── WORKSPACE PANELS ──────────────────────────────────────────────── */}
      <div className="flex-1 flex overflow-hidden w-full">
        {/* LEFT COLUMN: Suggesions Queue */}
        <div className="w-[30%] border-r border-border/40 flex flex-col bg-card/10 overflow-hidden shrink-0">
          <div className="px-4 py-3 border-b border-border/40 flex items-center gap-2 bg-card/25 shrink-0">
            <FileEdit className="h-4 w-4 text-primary" />
            <span className="text-xs font-bold text-foreground uppercase tracking-wider">Audit Suggestions</span>
          </div>

          <div className="flex-1 p-3 overflow-y-auto flex flex-col gap-3">
            {suggestions.map((sug) => (
              <div
                key={sug.id}
                onClick={() => setSelectedSuggestion(sug.id)}
                className={cn(
                  "p-4 rounded-xl border transition-all cursor-pointer flex flex-col gap-2 relative overflow-hidden",
                  selectedSuggestion === sug.id
                    ? "bg-primary/5 border-primary/40 shadow-sm"
                    : "bg-card/40 border-border/40 hover:border-primary/20",
                  sug.accepted && "border-success/30 bg-success/3",
                  sug.rejected && "border-destructive/20 opacity-60"
                )}
              >
                <div className="flex items-center justify-between">
                  <span className="text-[10px] font-bold uppercase tracking-wider text-muted-foreground">
                    {sug.section} Section
                  </span>
                  {sug.accepted && <Badge variant="success">Accepted</Badge>}
                  {sug.rejected && <Badge variant="danger">Rejected</Badge>}
                </div>
                <p className="text-xs font-bold text-foreground leading-snug">{sug.explanation}</p>

                {/* Accept/Reject buttons */}
                {!sug.accepted && !sug.rejected && (
                  <div className="flex items-center gap-2 mt-2">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleAccept(sug.id);
                      }}
                      className="flex items-center gap-1 px-2.5 py-1 text-[10px] font-bold bg-success/15 hover:bg-success/25 text-success rounded-lg transition-colors border border-success/20"
                    >
                      <Check className="h-3 w-3" />
                      Accept
                    </button>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleReject(sug.id);
                      }}
                      className="flex items-center gap-1 px-2.5 py-1 text-[10px] font-bold bg-destructive/10 hover:bg-destructive/20 text-destructive rounded-lg transition-colors border border-destructive/20"
                    >
                      <X className="h-3 w-3" />
                      Reject
                    </button>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>

        {/* RIGHT COLUMN: Split View Resume Text Compare */}
        <div className="flex-1 flex overflow-hidden bg-background">
          {/* Original/Current Resume panel */}
          <div className="flex-1 border-r border-border/40 flex flex-col overflow-hidden">
            <div className="px-4 py-3 border-b border-border/40 bg-card/15 shrink-0">
              <span className="text-xs font-bold text-foreground uppercase tracking-wider">Current Working Draft</span>
            </div>
            <div className="flex-1 p-5 overflow-y-auto font-mono text-xs text-muted-foreground whitespace-pre-wrap leading-relaxed select-text">
              {originalResume}
            </div>
          </div>

          {/* AI Optimizer preview proposal panel */}
          <div className="flex-1 flex flex-col overflow-hidden bg-card/5">
            <div className="px-4 py-3 border-b border-border/40 bg-card/15 shrink-0 flex items-center justify-between">
              <span className="text-xs font-bold text-primary uppercase tracking-wider">AI Suggested Preview</span>
            </div>
            <div className="flex-1 p-5 overflow-y-auto flex flex-col gap-4">
              <AnimatePresence mode="wait">
                {activeSuggestion ? (
                  <motion.div
                    key={activeSuggestion.id}
                    initial={{ opacity: 0, y: 8 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: 8 }}
                    className="flex flex-col gap-4 h-full"
                  >
                    <div className="flex flex-col gap-1.5 p-4 rounded-xl bg-destructive/10 border border-destructive/15">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-destructive">Original sentence to replace:</span>
                      <p className="text-xs text-muted-foreground italic font-mono leading-relaxed select-text">
                        "{activeSuggestion.original}"
                      </p>
                    </div>

                    <div className="flex flex-col gap-1.5 p-4 rounded-xl bg-success/10 border border-success/15">
                      <span className="text-[10px] font-bold uppercase tracking-wider text-success">Optimized replacement text:</span>
                      <p className="text-xs text-foreground font-mono leading-relaxed select-text">
                        "{activeSuggestion.suggested}"
                      </p>
                    </div>

                    <div className="mt-auto glass-panel p-4 flex flex-col gap-2">
                      <h4 className="text-xs font-bold text-foreground">Why this change?</h4>
                      <p className="text-xs text-muted-foreground leading-relaxed">{activeSuggestion.explanation}</p>
                    </div>
                  </motion.div>
                ) : (
                  <div className="flex flex-col items-center justify-center h-full text-center text-muted-foreground gap-2">
                    <Sparkles className="h-8 w-8 text-primary/40 animate-pulse" />
                    <p className="text-xs">Select a suggestion card from the left panel to compare.</p>
                  </div>
                )}
              </AnimatePresence>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
