import i18n from "../i18n";

const API_BASE = import.meta.env.VITE_API_BASE ?? "/api";

function withLang(path: string): string {
  const sep = path.includes("?") ? "&" : "?";
  return `${API_BASE}${path}${sep}lang=${i18n.language}`;
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(withLang(path));
  if (!res.ok) throw new Error(`GET ${path} -> ${res.status}`);
  return res.json();
}

export async function apiPost<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(withLang(path), {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`POST ${path} -> ${res.status}: ${detail}`);
  }
  return res.json();
}
