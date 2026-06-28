import { createContext, useContext, useState, type ReactNode } from "react";

import type { SubmitResult } from "./api/types";

interface LeadStore {
  result: SubmitResult | null;
  setResult: (r: SubmitResult | null) => void;
}

const Ctx = createContext<LeadStore | null>(null);

export function LeadProvider({ children }: { children: ReactNode }) {
  const [result, setResult] = useState<SubmitResult | null>(null);
  return <Ctx.Provider value={{ result, setResult }}>{children}</Ctx.Provider>;
}

export function useLeadStore() {
  const ctx = useContext(Ctx);
  if (!ctx) throw new Error("useLeadStore must be used within LeadProvider");
  return ctx;
}
