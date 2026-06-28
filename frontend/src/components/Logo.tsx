import LogoSvg from "../assets/logo.svg?react";

/**
 * The logo is inlined into the DOM (not via <img>!) so that <text> inside the SVG
 * can see the page's @font-face fonts (League Spartan + Aka-AcidGR).
 */
export default function Logo({ className }: { className?: string }) {
  return <LogoSvg className={className} role="img" aria-label="EGGCELLENT" />;
}
