import { useTranslation } from "react-i18next";

import { useSiteSettings } from "../../api/hooks";
import Logo from "../Logo";
import Mascot from "../Mascot";
import Squiggle from "../Squiggle";

export default function Hero() {
  const { t } = useTranslation();
  const { data: site } = useSiteSettings();

  return (
    <section
      id="hero"
      className="relative flex min-h-screen flex-col items-center justify-center overflow-hidden px-6 pt-24 text-center"
    >
      {/* Decorative squiggles — static (no scroll parallax so they don't jitter) */}
      <Squiggle
        variant="b"
        className="pointer-events-none absolute left-4 top-24 w-40 opacity-70 sm:w-64"
      />
      <Squiggle
        variant="c"
        className="pointer-events-none absolute bottom-28 right-4 w-44 opacity-70 sm:w-72"
      />

      {/* CSS animations (independent of JS) — critical content is always visible.
          The mascot sits BEHIND the logo card (z-0), shifted to the right edge and tilted right. */}
      <div className="relative flex w-full max-w-4xl flex-col items-center">
        <div className="absolute -top-28 right-2 z-0 w-28 rotate-[14deg] sm:-top-44 sm:right-10 sm:w-48">
          <div className="animate-float">
            <Mascot className="h-auto w-full" />
          </div>
        </div>

        <div className="relative z-10 w-full animate-pop-in rounded-[2rem] bg-ink p-6 shadow-[10px_10px_0_0_#ff0049] sm:p-12">
          <Logo className="mx-auto h-auto w-full" />
        </div>
      </div>

      <h1
        className="mt-10 max-w-3xl animate-fade-up font-display text-2xl font-extrabold uppercase leading-tight sm:text-4xl"
        style={{ animationDelay: "0.15s" }}
      >
        {site?.hero_title}
      </h1>
      <p
        className="mt-3 max-w-xl animate-fade-up text-lg text-ink/70"
        style={{ animationDelay: "0.25s" }}
      >
        {site?.hero_subtitle}
      </p>

      <div
        className="mt-8 flex animate-fade-up flex-col gap-3 sm:flex-row"
        style={{ animationDelay: "0.4s" }}
      >
        <a href="#test" className="pill-primary">
          {t("hero.cta_test")}
        </a>
        <a href="#apply" className="pill-outline">
          {t("hero.cta_apply")}
        </a>
      </div>

      <a
        href="#teachers"
        className="absolute bottom-8 animate-float text-sm uppercase tracking-widest text-ink/50"
      >
        ↓ {t("hero.scroll")}
      </a>
    </section>
  );
}
