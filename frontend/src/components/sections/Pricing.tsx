import { useTranslation } from "react-i18next";

import { usePlans } from "../../api/hooks";
import type { Plan } from "../../api/types";
import Carousel from "../Carousel";
import SectionHeader from "../SectionHeader";

function PlanCard({ plan }: { plan: Plan }) {
  const { t } = useTranslation();
  const highlighted = plan.is_highlighted;

  return (
    <div
      className={`relative flex h-full flex-col rounded-3xl border-2 p-6 ${
        highlighted
          ? "border-brand bg-ink text-cream shadow-[8px_8px_0_0_#ff0049] lg:-translate-y-3"
          : "border-ink bg-cream shadow-[6px_6px_0_0_#252422]"
      }`}
    >
      {plan.discount_percent > 0 && (
        <span className="absolute -right-3 -top-3 rotate-6 rounded-pill bg-brand px-3 py-1 text-sm font-bold text-cream shadow">
          −{plan.discount_percent}% {t("pricing.discount")}
        </span>
      )}
      {highlighted && !plan.discount_percent && (
        <span className="absolute -right-3 -top-3 rounded-pill bg-brand px-3 py-1 text-sm font-bold text-cream">
          {t("pricing.popular")}
        </span>
      )}

      <h3 className="font-display text-2xl font-extrabold uppercase">
        {plan.title}
      </h3>

      {plan.is_speaking_club ? (
        <>
          <div className="mt-4 font-display text-5xl font-extrabold text-brand">
            {plan.total_price} <span className="text-2xl">грн</span>
            <span className="text-base font-normal opacity-60">
              {t("pricing.month")}
            </span>
          </div>
          <ul className="mt-5 flex-1 space-y-2 text-left">
            {plan.features?.map((f, i) => (
              <li key={i} className="flex gap-2">
                <span className="text-brand">✓</span>
                <span className="opacity-80">{f}</span>
              </li>
            ))}
          </ul>
        </>
      ) : (
        <>
          <div className="mt-4 font-display text-5xl font-extrabold text-brand">
            {plan.price_per_lesson}
            <span className="ml-1 text-base font-normal opacity-60">
              {t("pricing.per_lesson")}
            </span>
          </div>
          <p className="mt-2 opacity-70">
            {plan.lessons_count} {t("pricing.lessons")} · {plan.total_price} грн{" "}
            {t("pricing.total")}
          </p>
          <div className="flex-1" />
        </>
      )}

      {plan.note && <p className="mt-4 text-sm opacity-60">{plan.note}</p>}

      <a
        href="#apply"
        className={`mt-6 ${highlighted ? "pill-primary" : "pill-ink"}`}
      >
        {t("pricing.choose")}
      </a>
    </div>
  );
}

export default function Pricing() {
  const { t } = useTranslation();
  const { data: plans, isLoading } = usePlans();

  if (isLoading || !plans?.length) return null;

  return (
    <section id="pricing" className="mx-auto max-w-6xl px-6 py-24">
      <SectionHeader title={t("pricing.title")} subtitle={t("pricing.subtitle")} />
      <Carousel>
        {plans.map((p) => (
          <PlanCard key={p.id} plan={p} />
        ))}
      </Carousel>
    </section>
  );
}
