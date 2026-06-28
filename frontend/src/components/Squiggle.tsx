import { motion } from "framer-motion";

/** Hand-drawn red squiggles from the brand style (decoration). */
const PATHS: Record<string, string> = {
  a: "M2 30 C 40 5, 70 55, 110 25 S 180 5, 220 35",
  b: "M2 20 C 30 60, 80 -10, 120 30 S 200 60, 250 15",
  c: "M5 40 Q 60 0 120 40 T 240 30",
};

interface Props {
  variant?: keyof typeof PATHS;
  className?: string;
  /** The line "draws itself" on appearance */
  draw?: boolean;
}

export default function Squiggle({ variant = "a", className, draw }: Props) {
  return (
    <svg
      className={className}
      viewBox="0 0 252 70"
      fill="none"
      aria-hidden="true"
    >
      <motion.path
        d={PATHS[variant]}
        stroke="#ff0049"
        strokeWidth={5}
        strokeLinecap="round"
        initial={draw ? { pathLength: 0 } : undefined}
        whileInView={draw ? { pathLength: 1 } : undefined}
        viewport={{ once: true }}
        transition={{ duration: 1.1, ease: "easeInOut" }}
      />
    </svg>
  );
}
