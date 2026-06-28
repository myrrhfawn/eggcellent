import LogoTextSvg from "../assets/logo_text.svg?react";

/**
 * Text variant of the logo (the "EGGCELLENT" wordmark without the plate) — for the header.
 * Inlined into the DOM so that <text> can see the page's @font-face fonts.
 */
export default function LogoText({ className }: { className?: string }) {
  // overflow-visible — the glyphs slightly extend beyond the viewBox (font size > height),
  // otherwise the inline SVG clips them at the edges.
  return (
    <LogoTextSvg
      className={`overflow-visible ${className ?? ""}`}
      role="img"
      aria-label="EGGCELLENT"
    />
  );
}
