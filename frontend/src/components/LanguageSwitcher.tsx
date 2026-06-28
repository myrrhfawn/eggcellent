import { useTranslation } from "react-i18next";

import { LANGS } from "../i18n";

export default function LanguageSwitcher({ dark }: { dark?: boolean }) {
  const { i18n } = useTranslation();
  const base = dark ? "text-cream/60" : "text-ink/50";
  const active = dark ? "text-cream" : "text-ink";

  return (
    <div className="flex items-center gap-1 font-display text-sm font-bold uppercase">
      {LANGS.map((lng, i) => (
        <span key={lng} className="flex items-center gap-1">
          {i > 0 && <span className={base}>/</span>}
          <button
            type="button"
            onClick={() => i18n.changeLanguage(lng)}
            className={`transition-colors hover:opacity-80 ${
              i18n.language === lng ? active : base
            }`}
          >
            {lng}
          </button>
        </span>
      ))}
    </div>
  );
}
