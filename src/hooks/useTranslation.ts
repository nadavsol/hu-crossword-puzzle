import { useMemo } from "react";
import type { LocalizedString } from "@/types/puzzle";
import hu from "@/locales/hu.json";

export function useTranslation() {
  return useMemo(() => {
    const dict: Record<string, string> = hu;

    function t(key: string): string {
      return dict[key] ?? key;
    }

    function ls(localized: LocalizedString): string {
      return localized.hu;
    }

    return { t, ls, language: "hu" as const };
  }, []);
}
