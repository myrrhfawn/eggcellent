import { AnimatePresence, motion } from "framer-motion";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { apiPost } from "../../api/client";
import { useQuestions } from "../../api/hooks";
import type { SubmitResult } from "../../api/types";
import { useLeadStore } from "../../store";

type Phase = "intro" | "running" | "result";

export default function TestWizard() {
  const { t } = useTranslation();
  const { data: questions } = useQuestions();
  const { setResult } = useLeadStore();

  const [phase, setPhase] = useState<Phase>("intro");
  const [current, setCurrent] = useState(0);
  // {questionId: answerId}
  const [answers, setAnswers] = useState<Record<number, number>>({});
  const [result, setLocalResult] = useState<SubmitResult | null>(null);
  const [submitting, setSubmitting] = useState(false);

  if (!questions?.length) return null;

  const total = questions.length;
  // Approximate time: ~30 sec per question.
  const estMinutes = Math.max(1, Math.round(total * 0.5));
  const q = questions[current];
  const progress = Math.round(((current + (phase === "result" ? 1 : 0)) / total) * 100);

  const pick = (answerId: number) => {
    setAnswers((prev) => ({ ...prev, [q.id]: answerId }));
  };

  const next = async () => {
    if (current < total - 1) {
      setCurrent((c) => c + 1);
      return;
    }
    // last one — submit
    setSubmitting(true);
    try {
      const res = await apiPost<SubmitResult>("/test/submit/", {
        answers: Object.fromEntries(
          Object.entries(answers).map(([k, v]) => [k, v]),
        ),
      });
      setLocalResult(res);
      setResult(res);
      setPhase("result");
    } finally {
      setSubmitting(false);
    }
  };

  const restart = () => {
    setAnswers({});
    setCurrent(0);
    setLocalResult(null);
    setResult(null);
    setPhase("intro");
  };

  return (
    <section id="test" className="bg-brand py-24 text-cream">
      <div className="mx-auto max-w-3xl px-6">
        <div className="mb-12 text-center">
          <h2 className="section-title text-cream">{t("test.title")}</h2>
          <p className="mt-3 text-lg text-cream/80">{t("test.subtitle")}</p>
        </div>

        <div className="card bg-cream p-6 text-ink sm:p-10">
          <AnimatePresence mode="wait">
            {phase === "intro" && (
              <motion.div
                key="intro"
                initial={false}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center text-center"
              >
                <p className="max-w-xl text-lg leading-relaxed text-ink/80">
                  {t("test.intro_desc")}
                </p>
                <div className="mt-6 flex flex-wrap justify-center gap-3">
                  <span className="rounded-pill border-2 border-ink/15 bg-ink/5 px-4 py-2 text-sm font-semibold">
                    📝 {t("test.info_questions", { count: total })}
                  </span>
                  <span className="rounded-pill border-2 border-ink/15 bg-ink/5 px-4 py-2 text-sm font-semibold">
                    ⏱ {t("test.info_time", { min: estMinutes })}
                  </span>
                  <span className="rounded-pill border-2 border-ink/15 bg-ink/5 px-4 py-2 text-sm font-semibold">
                    🎓 {t("test.info_cert")}
                  </span>
                </div>
                <button
                  className="pill-primary mt-8"
                  onClick={() => setPhase("running")}
                >
                  {t("test.start")}
                </button>
              </motion.div>
            )}

            {phase === "running" && (
              <motion.div
                key="running"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
              >
                {/* progress */}
                <div className="mb-2 flex justify-between text-sm font-semibold uppercase text-ink/60">
                  <span>
                    {t("test.question")} {current + 1} {t("test.of")} {total}
                  </span>
                  <span>{progress}%</span>
                </div>
                <div className="mb-8 h-2 w-full overflow-hidden rounded-full bg-ink/10">
                  <motion.div
                    className="h-full rounded-full bg-brand"
                    animate={{ width: `${((current + 1) / total) * 100}%` }}
                    transition={{ ease: "easeOut" }}
                  />
                </div>

                <AnimatePresence mode="wait">
                  <motion.div
                    key={q.id}
                    initial={{ opacity: 0, x: 40 }}
                    animate={{ opacity: 1, x: 0 }}
                    exit={{ opacity: 0, x: -40 }}
                    transition={{ duration: 0.3 }}
                  >
                    <h3 className="mb-6 font-display text-2xl font-bold">
                      {q.text}
                    </h3>
                    <div className="flex flex-col gap-3">
                      {q.answers.map((a) => {
                        const active = answers[q.id] === a.id;
                        return (
                          <button
                            key={a.id}
                            onClick={() => pick(a.id)}
                            className={`rounded-2xl border-2 px-5 py-4 text-left text-lg transition-all ${
                              active
                                ? "border-brand bg-brand text-cream"
                                : "border-ink/20 hover:border-ink"
                            }`}
                          >
                            {a.text}
                          </button>
                        );
                      })}
                    </div>
                  </motion.div>
                </AnimatePresence>

                <div className="mt-8 flex justify-between">
                  <button
                    className="pill-outline disabled:opacity-30"
                    onClick={() => setCurrent((c) => Math.max(0, c - 1))}
                    disabled={current === 0}
                  >
                    {t("test.back")}
                  </button>
                  <button
                    className="pill-primary disabled:opacity-40"
                    onClick={next}
                    disabled={answers[q.id] === undefined || submitting}
                  >
                    {current === total - 1 ? t("test.finish") : t("test.next")}
                  </button>
                </div>
              </motion.div>
            )}

            {phase === "result" && result && (
              <motion.div
                key="result"
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                className="text-center"
              >
                <p className="text-lg uppercase tracking-wide text-ink/60">
                  {t("test.result_title")}
                </p>
                <div className="my-2 font-display text-7xl font-extrabold text-brand">
                  {result.level?.code ?? "—"}
                </div>
                <p className="text-xl font-semibold">{result.level?.title}</p>
                <p className="mt-2 text-ink/70">{result.level?.description}</p>
                <p className="mt-4 text-sm uppercase text-ink/50">
                  {t("test.result_score")}: {result.score} / {result.max_score}
                </p>
                <div className="mt-8 flex flex-col justify-center gap-3 sm:flex-row">
                  <a href="#apply" className="pill-primary">
                    {t("test.result_cta")}
                  </a>
                  <button className="pill-outline" onClick={restart}>
                    {t("test.retry")}
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}
