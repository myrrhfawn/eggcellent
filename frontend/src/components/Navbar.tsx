import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import LanguageSwitcher from "./LanguageSwitcher";
import LogoText from "./LogoText";

const LINKS = ["teachers", "reviews", "pricing", "test"] as const;

export default function Navbar() {
  const { t } = useTranslation();
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 40);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`fixed inset-x-0 top-0 z-50 transition-all ${
        scrolled ? "bg-cream/90 shadow-md backdrop-blur" : "bg-transparent"
      }`}
    >
      <nav className="mx-auto flex max-w-6xl items-center justify-between gap-4 px-6 py-3">
        <a href="#hero" className="block w-40 shrink-0 sm:w-48">
          <LogoText className="h-auto w-full" />
        </a>
        <div className="hidden items-center gap-6 font-display font-semibold uppercase md:flex">
          {LINKS.map((l) => (
            <a key={l} href={`#${l}`} className="transition-colors hover:text-brand">
              {t(`nav.${l}`)}
            </a>
          ))}
        </div>
        <div className="flex items-center gap-4">
          <LanguageSwitcher />
          <a href="#apply" className="pill-primary !px-5 !py-2 text-sm">
            {t("nav.apply")}
          </a>
        </div>
      </nav>
    </header>
  );
}
