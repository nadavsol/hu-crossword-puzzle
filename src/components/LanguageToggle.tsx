"use client";

import type { Language } from "@/types/puzzle";

interface LanguageToggleProps {
  language: Language;
  onToggle: (lang: Language) => void;
}

export function LanguageToggle({ language, onToggle }: LanguageToggleProps) {
  return (
    <button
      onClick={() => onToggle(language === "hu" ? "he" : "hu")}
      className="bg-[#2d5a8e] text-white px-3 py-1.5 rounded-lg text-sm font-medium
                 min-w-[44px] min-h-[44px] flex items-center justify-center
                 active:bg-[#1e3a5f] transition-colors"
      aria-label={language === "hu" ? "Switch to Hebrew" : "Switch to Hungarian"}
    >
      {language === "hu" ? "HU | עב" : "עב | HU"}
    </button>
  );
}
