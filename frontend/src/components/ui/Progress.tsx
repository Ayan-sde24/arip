import { motion } from "framer-motion";
import { cn } from "../../lib/utils";

// ── 1. Linear Progress ────────────────────────────────────────────────────────
export function LinearProgress({
  value,
  className,
}: {
  value: number;
  className?: string;
}) {
  const percent = Math.min(100, Math.max(0, value));

  return (
    <div className={cn("w-full bg-muted rounded-full h-2 overflow-hidden", className)}>
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: `${percent}%` }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="h-full bg-primary rounded-full"
      />
    </div>
  );
}

// ── 2. Circular Progress & Score Ring ─────────────────────────────────────────
export function ScoreRing({
  score,
  size = 80,
  strokeWidth = 6,
  className,
}: {
  score: number;
  size?: number;
  strokeWidth?: number;
  className?: string;
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div
      className={cn("relative flex items-center justify-center select-none", className)}
      style={{ width: size, height: size }}
    >
      <svg className="transform -rotate-90 w-full h-full">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          className="stroke-muted"
          strokeWidth={strokeWidth}
          fill="transparent"
        />
        <motion.circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          className="stroke-primary"
          strokeWidth={strokeWidth}
          fill="transparent"
          strokeDasharray={circumference}
          initial={{ strokeDashoffset: circumference }}
          animate={{ strokeDashoffset: offset }}
          transition={{ duration: 1, ease: "easeOut" }}
        />
      </svg>
      <div className="absolute flex flex-col items-center">
        <span className="text-sm font-bold text-foreground">{score}</span>
        <span className="text-[9px] text-muted-foreground font-medium uppercase tracking-wide">
          Score
        </span>
      </div>
    </div>
  );
}

// ── 3. Pipeline Progress ──────────────────────────────────────────────────────
export function PipelineProgress({
  steps,
  currentStep,
}: {
  steps: string[];
  currentStep: number;
}) {
  return (
    <div className="flex items-center justify-between w-full relative py-2">
      <div className="absolute top-1/2 left-0 w-full h-[2px] bg-muted transform -translate-y-1/2 -z-10" />
      {steps.map((step, idx) => {
        const active = idx <= currentStep;
        return (
          <div key={idx} className="flex flex-col items-center gap-2 bg-background px-3">
            <div
              className={cn(
                "h-6 w-6 rounded-full border flex items-center justify-center text-xs font-semibold transition-all duration-300",
                active
                  ? "bg-primary text-primary-foreground border-primary scale-110 shadow-lg shadow-primary/20"
                  : "bg-card text-muted-foreground border-border/80"
              )}
            >
              {idx + 1}
            </div>
            <span
              className={cn(
                "text-[10px] font-semibold uppercase tracking-wider",
                active ? "text-primary" : "text-muted-foreground"
              )}
            >
              {step}
            </span>
          </div>
        );
      })}
    </div>
  );
}
