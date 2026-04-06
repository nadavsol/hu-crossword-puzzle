import { useMemo } from "react";
import type { Language, LocalizedString } from "@/types/puzzle";
import hu from "@/locales/hu.json";
import he from "@/locales/he.json";

const translations: Record<Language, Record<string, string>> = { hu, he };

export function useTranslation(language: Language) {
  return useMemo(() => {
    const dict = translations[language];

    function t(key: string): string {
      return dict[key] ?? key;
    }

    function ls(localized: LocalizedString): string {
      return localized[language];
    }

    return { t, ls, language, dir: language === "he" ? "rtl" as const : "ltr" as const };
  }, [language]);
}
