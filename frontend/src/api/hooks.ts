import { useQuery } from "@tanstack/react-query";
import { useTranslation } from "react-i18next";

import { apiGet } from "./client";
import type { Plan, Question, Review, SiteSettings, Teacher } from "./types";

// Language is part of the cache key — switching it reloads the data.
function useLangKey() {
  const { i18n } = useTranslation();
  return i18n.language;
}

export function useSiteSettings() {
  const lang = useLangKey();
  return useQuery({
    queryKey: ["site-settings", lang],
    queryFn: () => apiGet<SiteSettings>("/site-settings/"),
  });
}

export function useTeachers() {
  const lang = useLangKey();
  return useQuery({
    queryKey: ["teachers", lang],
    queryFn: () => apiGet<Teacher[]>("/teachers/"),
  });
}

export function useReviews() {
  const lang = useLangKey();
  return useQuery({
    queryKey: ["reviews", lang],
    queryFn: () => apiGet<Review[]>("/reviews/"),
  });
}

export function usePlans() {
  const lang = useLangKey();
  return useQuery({
    queryKey: ["plans", lang],
    queryFn: () => apiGet<Plan[]>("/plans/"),
  });
}

export function useQuestions() {
  const lang = useLangKey();
  return useQuery({
    queryKey: ["questions", lang],
    queryFn: () => apiGet<Question[]>("/test/questions/"),
  });
}
