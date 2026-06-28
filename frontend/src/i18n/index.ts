import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import en from "./en.json";
import uk from "./uk.json";

export const LANGS = ["uk", "en"] as const;
export type Lang = (typeof LANGS)[number];

const saved = (localStorage.getItem("lang") as Lang) || "uk";

i18n.use(initReactI18next).init({
  resources: {
    uk: { translation: uk },
    en: { translation: en },
  },
  lng: saved,
  fallbackLng: "uk",
  interpolation: { escapeValue: false },
});

i18n.on("languageChanged", (lng) => {
  localStorage.setItem("lang", lng);
  document.documentElement.lang = lng;
});

export default i18n;
