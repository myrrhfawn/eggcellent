import { motion } from "framer-motion";
import { useState } from "react";
import { useTranslation } from "react-i18next";

import { apiPost } from "../../api/client";
import { useLeadStore } from "../../store";
import Reveal from "../Reveal";

export default function LeadForm() {
  const { t } = useTranslation();
  const { result } = useLeadStore();

  const [name, setName] = useState("");
  const [phone, setPhone] = useState("");
  const [status, setStatus] = useState<"idle" | "sending" | "ok" | "err">("idle");
  const [errors, setErrors] = useState<{ name?: string; phone?: string }>({});

  const validate = () => {
    const e: typeof errors = {};
    if (name.trim().length < 2) e.name = t("lead.name_required");
    if (phone.replace(/\D/g, "").length < 9) e.phone = t("lead.phone_required");
    setErrors(e);
    return Object.keys(e).length === 0;
  };

  // Called ONLY on an explicit user action (button click or Enter).
  // The form does not submit on its own, so errors do not appear right away.
  const submit = async () => {
    if (!validate()) return;
    setStatus("sending");
    try {
      await apiPost("/leads/", {
        name,
        phone,
        source: result ? "test" : "form",
        submission_id: result?.id ?? null,
      });
      setStatus("ok");
      setName("");
      setPhone("");
    } catch {
      setStatus("err");
    }
  };

  return (
    <section id="apply" className="mx-auto max-w-2xl px-6 py-24">
      <Reveal>
        <div className="card bg-cream p-8 sm:p-10">
          <h2 className="section-title text-center">{t("lead.title")}</h2>
          <p className="mt-3 text-center text-ink/60">{t("lead.subtitle")}</p>

          {result?.level && (
            <div className="mx-auto mt-5 w-fit rounded-pill bg-brand px-5 py-2 font-semibold text-cream">
              {t("test.result_title")} {result.level.code}
            </div>
          )}

          {status === "ok" ? (
            <motion.p
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="mt-8 rounded-2xl bg-ink p-6 text-center text-lg font-semibold text-cream"
            >
              {t("lead.success")}
            </motion.p>
          ) : (
            <form
              onSubmit={(e) => e.preventDefault()}
              className="mt-8 flex flex-col gap-4"
              noValidate
            >
              <label className="flex flex-col gap-1">
                <span className="pl-4 font-semibold text-ink/70">
                  {t("lead.name")}
                </span>
                <input
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && submit()}
                  className="rounded-2xl border-2 border-ink/20 bg-white px-4 py-3 text-lg outline-none focus:border-brand"
                  placeholder="Taras"
                />
                {errors.name && (
                  <span className="text-sm text-brand">{errors.name}</span>
                )}
              </label>

              <label className="flex flex-col gap-1">
                <span className="pl-4 font-semibold text-ink/70">
                  {t("lead.phone")}
                </span>
                <input
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && submit()}
                  inputMode="tel"
                  className="rounded-2xl border-2 border-ink/20 bg-white px-4 py-3 text-lg outline-none focus:border-brand"
                  placeholder="+380 67 123 45 67"
                />
                {errors.phone && (
                  <span className="text-sm text-brand">{errors.phone}</span>
                )}
              </label>

              <button
                type="button"
                onClick={submit}
                disabled={status === "sending"}
                className="pill-primary mt-2 disabled:opacity-50"
              >
                {status === "sending" ? t("lead.sending") : t("lead.submit")}
              </button>
              {status === "err" && (
                <p className="text-center text-brand">{t("lead.error")}</p>
              )}
            </form>
          )}
        </div>
      </Reveal>
    </section>
  );
}
