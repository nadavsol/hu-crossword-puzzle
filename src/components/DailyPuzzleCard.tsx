"use client";

import type { PuzzleManifestEntry, Language } from "@/types/puzzle";

interface DailyPuzzleCardProps {
  puzzle: PuzzleManifestEntry;
  language: Language;
  startLabel: string;
  dailyLabel: string;
  difficultyLabel: string;
}

export function DailyPuzzleCard({
  puzzle,
  language,
  startLabel,
  dailyLabel,
  difficultyLabel,
}: DailyPuzzleCardProps) {
  return (
    <a
      href={`/puzzle?id=${puzzle.id}`}
      className="block bg-gradient-to-br from-[#1e3a5f] to-[#2d5a8e] rounded-2xl p-6 text-white shadow-lg"
    >
      <div className="text-xs uppercase tracking-wider opacity-80 mb-1">
        {dailyLabel}
      </div>
      <div className="text-2xl font-bold mb-1">
        {puzzle.title[language]}
      </div>
      <div className="text-sm opacity-80 mb-4">
        {difficultyLabel} · {puzzle.gridSize.rows}×{puzzle.gridSize.cols}
      </div>
      <div className="inline-block bg-white text-[#1e3a5f] px-6 py-3 rounded-xl font-bold text-base">
        {startLabel} ▶
      </div>
    </a>
  );
}
