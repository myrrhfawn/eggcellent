import MascotSvg from "../assets/mascot.svg?react";

/** Egg-headed mascot wearing glasses. */
export default function Mascot({ className }: { className?: string }) {
  return <MascotSvg className={className} role="img" aria-label="EGGCELLENT mascot" />;
}
