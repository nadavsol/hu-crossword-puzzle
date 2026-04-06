"use client";

import type { Clue, Language } from "@/types/puzzle";

interface CluePanelProps {
  acrossClues: Clue[];
  downClues: Clue[];
  activeClueNumber: number | null;
  activeDirection: "across" | "down";
  language: Language;
  acrossLabel: string;
  downLabel: string;
  onClueClick: (clue: Clue, direction: "across" | "down") => void;
}

export function CluePanel({
  acrossClues,
  downClues,
  activeClueNumber,
  activeDirection,
  language,
  acrossLabel,
  downLabel,
  onClueClick,
}: CluePanelProps) {
  const renderClue = (clue: Clue, direction: "across" | "down") => {
    const isActive =
      clue.number === activeClueNumber && direction === activeDirection;
    return (
      <button
        key={`${direction}-${clue.number}`}
        onClick={() => onClueClick(clue, direction)}
        className={`block w-full text-left px-2 py-1.5 rounded text-sm min-h-[44px]
                   flex items-start gap-2 transition-colors
                   ${isActive ? "bg-blue-100" : "hover:bg-slate-50"}`}
      >
        <span className="font-bold text-blue-600 shrink-0">{clue.number}.</span>
        <span className="text-slate-700">{clue.clue[language]}</span>
      </button>
    );
  };

  return (
    <div className="overflow-y-auto">
      <h3 className="font-bold text-[#1e3a5f] text-sm border-b-2 border-blue-100 pb-1 mb-2 px-2">
        {acrossLabel} ➡️
      </h3>
      <div className="space-y-0.5 mb-4">
        {acrossClues.map((c) => renderClue(c, "across"))}
      </div>

      <h3 className="font-bold text-[#1e3a5f] text-sm border-b-2 border-blue-100 pb-1 mb-2 px-2">
        {downLabel} ⬇️
      </h3>
      <div className="space-y-0.5">
        {downClues.map((c) => renderClue(c, "down"))}
      </div>
    </div>
  );
}
