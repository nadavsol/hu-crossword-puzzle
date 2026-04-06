"use client";

import type { PuzzleManifestEntry, Language } from "@/types/puzzle";

interface PuzzleCardProps {
  puzzle: PuzzleManifestEntry;
  language: Language;
  difficultyLabel: string;
  completedLabel: string;
  inProgressLabel?: string;
  completionPercent?: number;
}

export function PuzzleCard({
  puzzle,
  language,
  difficultyLabel,
  completedLabel,
  inProgressLabel,
  completionPercent,
}: PuzzleCardProps) {
  const isCompleted = completionPercent === 100;
  const isStarted = completionPercent !== undefined && completionPercent > 0;

  return (
    <a
      href={`/puzzle/${puzzle.id}`}
      className="min-w-[160px] bg-white rounded-xl p-3 border-2 border-slate-200 block shrink-0"
    >
      <div className="font-bold text-sm text-[#1e3a5f]">
        {puzzle.title[language]}
      </div>
      <div className="text-xs text-slate-500 mt-1">
        {puzzle.gridSize.rows}×{puzzle.gridSize.cols} · {difficultyLabel}
      </div>
      {isCompleted && (
        <div className="text-xs text-green-500 mt-1 font-semibold">
          ✓ {completedLabel}
        </div>
      )}
      {isStarted && !isCompleted && (
        <div className="text-xs text-amber-500 mt-1 font-semibold">
          ◐ {completionPercent}% {inProgressLabel}
        </div>
      )}
    </a>
  );
}
