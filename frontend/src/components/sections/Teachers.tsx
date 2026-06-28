import { useTranslation } from "react-i18next";

import { useTeachers } from "../../api/hooks";
import Carousel from "../Carousel";
import SectionHeader from "../SectionHeader";

export default function Teachers() {
  const { t } = useTranslation();
  const { data: teachers, isLoading } = useTeachers();

  if (isLoading || !teachers?.length) return null;

  return (
    <section id="teachers" className="mx-auto max-w-6xl px-6 py-24">
      <SectionHeader title={t("teachers.title")} subtitle={t("teachers.subtitle")} />
      <Carousel>
        {teachers.map((tch) => (
          <article key={tch.id} className="card h-full overflow-hidden p-5 text-center">
            <img
              src={tch.photo}
              alt={tch.name}
              loading="lazy"
              className="mx-auto aspect-square w-40 rounded-full border-2 border-ink object-cover"
            />
            <h3 className="mt-4 font-display text-2xl font-bold uppercase">
              {tch.name}
            </h3>
            <div className="mt-2 inline-block rounded-pill bg-brand px-4 py-1 text-sm font-semibold text-cream">
              {tch.english_level}
            </div>
            {tch.experience && (
              <p className="mt-3 text-ink/70">
                {t("teachers.experience")}: {tch.experience}
              </p>
            )}
            {tch.bio && <p className="mt-2 text-sm text-ink/60">{tch.bio}</p>}
          </article>
        ))}
      </Carousel>
    </section>
  );
}
