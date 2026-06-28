import useEmblaCarousel from "embla-carousel-react";
import { useCallback, useEffect, useState, type ReactNode } from "react";

interface Props {
  children: ReactNode[];
  /** CSS classes for each slide (control width/responsive behavior) */
  slideClassName?: string;
  /** dark section (black background) — light carousel controls */
  dark?: boolean;
}

// Slide width accounts for gap-10 (2.5rem) so the viewport fits a WHOLE
// number of cards: 1 (mobile) / 2 (tablet) / 3 (desktop).
// The larger gap also hides the overflowing badges of neighboring cards past the edge.
const DEFAULT_SLIDE =
  "min-w-0 shrink-0 grow-0 basis-full sm:basis-[calc(50%-1.25rem)] lg:basis-[calc(33.333%-1.667rem)]";

export default function Carousel({
  children,
  slideClassName = DEFAULT_SLIDE,
  dark = false,
}: Props) {
  const [emblaRef, emblaApi] = useEmblaCarousel({
    loop: false,
    align: "start",
    containScroll: "trimSnaps",
    slidesToScroll: "auto",
  });
  const [selected, setSelected] = useState(0);
  const [snaps, setSnaps] = useState<number[]>([]);

  const onSelect = useCallback(() => {
    if (emblaApi) setSelected(emblaApi.selectedScrollSnap());
  }, [emblaApi]);

  useEffect(() => {
    if (!emblaApi) return;
    setSnaps(emblaApi.scrollSnapList());
    emblaApi.on("select", onSelect);
    emblaApi.on("reInit", () => {
      setSnaps(emblaApi.scrollSnapList());
      onSelect();
    });
    onSelect();
  }, [emblaApi, onSelect]);

  const btn = dark
    ? "bg-cream text-ink hover:bg-white"
    : "bg-ink text-cream hover:opacity-90";
  const dotIdle = dark ? "bg-cream/40" : "bg-ink/30";

  return (
    <div className="relative">
      {/* px/py — spacing so the overflowing discount badges and card shadows
          are not clipped by the viewport edges */}
      <div className="overflow-hidden px-4 py-10" ref={emblaRef}>
        <div className="flex gap-10">
          {children.map((child, i) => (
            <div className={slideClassName} key={i}>
              {child}
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6 flex items-center justify-center gap-4">
        <button
          type="button"
          onClick={() => emblaApi?.scrollPrev()}
          aria-label="prev"
          className={`flex h-11 w-11 items-center justify-center rounded-full text-xl font-bold transition ${btn}`}
        >
          ‹
        </button>
        <div className="flex items-center gap-2">
          {snaps.map((_, i) => (
            <button
              key={i}
              type="button"
              aria-label={`slide ${i + 1}`}
              onClick={() => emblaApi?.scrollTo(i)}
              className={`h-2.5 rounded-full transition-all ${
                i === selected ? "w-7 bg-brand" : `w-2.5 ${dotIdle}`
              }`}
            />
          ))}
        </div>
        <button
          type="button"
          onClick={() => emblaApi?.scrollNext()}
          aria-label="next"
          className={`flex h-11 w-11 items-center justify-center rounded-full text-xl font-bold transition ${btn}`}
        >
          ›
        </button>
      </div>
    </div>
  );
}
