import { motion, AnimatePresence } from "framer-motion";
import { Bot, Loader2 } from "lucide-react";
import { useGlobalLoaderStore } from "../../store";

// ── Full-screen Global Loader ─────────────────────────────────────────────────
export function GlobalLoader() {
  const { isLoading, message } = useGlobalLoaderStore();

  return (
    <AnimatePresence>
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          transition={{ duration: 0.2 }}
          className="fixed inset-0 z-[200] flex flex-col items-center justify-center bg-background/95 backdrop-blur-xl"
        >
          {/* Animated ring */}
          <div className="relative mb-8">
            <div className="h-20 w-20 rounded-full border-2 border-border/40 flex items-center justify-center">
              <Bot className="h-8 w-8 text-primary" />
            </div>
            <motion.div
              className="absolute inset-0 rounded-full border-2 border-primary border-t-transparent"
              animate={{ rotate: 360 }}
              transition={{ duration: 1.2, repeat: Infinity, ease: "linear" }}
            />
            <motion.div
              className="absolute inset-[-6px] rounded-full border border-primary/20 border-t-primary/40"
              animate={{ rotate: -360 }}
              transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
            />
          </div>

          <p className="text-sm font-semibold text-foreground">{message}</p>
          <p className="text-xs text-muted-foreground mt-1">AI agents are working…</p>

          {/* Animated dots */}
          <div className="flex items-center gap-1.5 mt-6">
            {[0, 1, 2].map((i) => (
              <motion.div
                key={i}
                className="h-1.5 w-1.5 rounded-full bg-primary"
                animate={{ opacity: [0.3, 1, 0.3], scale: [0.8, 1.1, 0.8] }}
                transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.2 }}
              />
            ))}
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// ── Skeleton Overlay ──────────────────────────────────────────────────────────
export function SkeletonOverlay({ isLoading }: { isLoading: boolean }) {
  return (
    <AnimatePresence>
      {isLoading && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 z-10 bg-background/50 backdrop-blur-sm rounded-xl"
        >
          <div className="p-6 flex flex-col gap-4">
            <div className="h-4 bg-muted rounded animate-pulse w-3/4" />
            <div className="h-3 bg-muted rounded animate-pulse w-full" />
            <div className="h-3 bg-muted rounded animate-pulse w-5/6" />
            <div className="h-24 bg-muted rounded-lg animate-pulse" />
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}

// ── AI Processing Overlay ─────────────────────────────────────────────────────
export function AIProcessingOverlay({
  isProcessing,
  label = "AI agents thinking…",
}: {
  isProcessing: boolean;
  label?: string;
}) {
  return (
    <AnimatePresence>
      {isProcessing && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          className="absolute inset-0 z-10 flex flex-col items-center justify-center gap-3 bg-card/80 backdrop-blur-sm rounded-xl"
        >
          <div className="relative">
            <Loader2 className="h-8 w-8 text-primary animate-spin" />
            <motion.div
              className="absolute inset-0 rounded-full bg-primary/10"
              animate={{ scale: [1, 1.5, 1], opacity: [0.5, 0, 0.5] }}
              transition={{ duration: 1.5, repeat: Infinity }}
            />
          </div>
          <p className="text-xs font-medium text-muted-foreground">{label}</p>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
