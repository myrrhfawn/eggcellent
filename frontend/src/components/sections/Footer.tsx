import { useTranslation } from "react-i18next";

import { useSiteSettings } from "../../api/hooks";
import LanguageSwitcher from "../LanguageSwitcher";
import Logo from "../Logo";

const SOCIALS: { key: "instagram_url" | "telegram_url" | "facebook_url"; label: string }[] =
  [
    { key: "instagram_url", label: "Instagram" },
    { key: "telegram_url", label: "Telegram" },
    { key: "facebook_url", label: "Facebook" },
  ];

export default function Footer() {
  const { t } = useTranslation();
  const { data: site } = useSiteSettings();

  return (
    <footer className="bg-ink px-6 py-14 text-cream">
      <div className="mx-auto flex max-w-6xl flex-col items-center gap-8 text-center">
        <div className="w-64">
          <Logo className="h-auto w-full" />
        </div>

        <div className="flex flex-wrap items-center justify-center gap-4">
          {SOCIALS.map(({ key, label }) => {
            const url = site?.[key];
            if (!url) return null;
            return (
              <a
                key={key}
                href={url}
                target="_blank"
                rel="noreferrer"
                className="rounded-pill border-2 border-cream/30 px-5 py-2 font-semibold uppercase transition-colors hover:border-brand hover:text-brand"
              >
                {label}
              </a>
            );
          })}
        </div>

        {site?.contact_phone && (
          <a href={`tel:${site.contact_phone}`} className="text-cream/70">
            {site.contact_phone}
          </a>
        )}

        <LanguageSwitcher dark />

        <p className="text-sm text-cream/40">
          © {new Date().getFullYear()} EGGCELLENT. {t("footer.rights")}.
        </p>
      </div>
    </footer>
  );
}
