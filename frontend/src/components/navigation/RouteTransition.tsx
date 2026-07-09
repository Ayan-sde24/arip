import { motion } from "framer-motion";
import { pageTransition } from "../../animations/variants";

export function RouteTransition({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={pageTransition.initial}
      animate={pageTransition.animate}
      exit={pageTransition.exit}
      className="flex-1 w-full"
    >
      {children}
    </motion.div>
  );
}
