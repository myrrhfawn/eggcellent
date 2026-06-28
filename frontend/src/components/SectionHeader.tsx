import Reveal from "./Reveal";
import Squiggle from "./Squiggle";

export default function SectionHeader({
  title,
  subtitle,
}: {
  title: string;
  subtitle?: string;
}) {
  return (
    <Reveal className="mb-12 text-center">
      <h2 className="section-title">{title}</h2>
      <Squiggle variant="c" draw className="mx-auto mt-3 w-40" />
      {subtitle && <p className="mt-3 text-lg text-ink/60">{subtitle}</p>}
    </Reveal>
  );
}
