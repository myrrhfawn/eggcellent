import { useTranslation } from "react-i18next";

import { useReviews } from "../../api/hooks";
import Carousel from "../Carousel";

function Stars({ rating }: { rating: number }) {
  return (
    <div className="text-xl text-brand" aria-label={`${rating}/5`}>
      {"★".repeat(rating)}
      <span className="text-ink/20">{"★".repeat(5 - rating)}</span>
    </div>
  );
}

export default function Reviews() {
  const { t } = useTranslation();
  const { data: reviews, isLoading } = useReviews();

  if (isLoading || !reviews?.length) return null;

  return (
    <section id="reviews" className="bg-ink py-24 text-cream">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mb-12 text-center">
          <h2 className="section-title text-cream">{t("reviews.title")}</h2>
          <p className="mt-3 text-lg text-cream/60">{t("reviews.subtitle")}</p>
        </div>
        <Carousel dark>
          {reviews.map((r) => (
            <blockquote
              key={r.id}
              className="flex h-full flex-col rounded-3xl border-2 border-cream/20 bg-cream/5 p-6"
            >
              <Stars rating={r.rating} />
              <p className="mt-4 flex-1 text-lg leading-relaxed">“{r.text}”</p>
              <footer className="mt-4 font-display font-bold uppercase text-brand">
                {r.author_name}
              </footer>
            </blockquote>
          ))}
        </Carousel>
      </div>
    </section>
  );
}
