"use client";

import type { Language } from "@/types/puzzle";
import { LanguageToggle } from "./LanguageToggle";

interface TopBarProps {
  title: string;
  language: Language;
  onLanguageToggle: (lang: Language) => void;
  backHref?: string;
  rightContent?: React.ReactNode;
}

export function TopBar({
  title,
  language,
  onLanguageToggle,
  backHref,
  rightContent,
}: TopBarProps) {
  return (
    <header className="bg-[#1e3a5f] text-white px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        {backHref && (
          <a
            href={backHref}
            className="text-xl min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label="Back"
          >
            ←
          </a>
        )}
        <h1 className="text-lg font-bold">{title}</h1>
      </div>
      <div className="flex items-center gap-3">
        {rightContent}
        <LanguageToggle language={language} onToggle={onLanguageToggle} />
      </div>
    </header>
  );
}
