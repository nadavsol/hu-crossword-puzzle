"use client";

import { useEffect, useState } from "react";
import { TopBar } from "@/components/TopBar";
import { DifficultyFilter } from "@/components/DifficultyFilter";
import { PuzzleCard } from "@/components/PuzzleCard";
import { useProgress } from "@/hooks/useProgress";
import { useTranslation } from "@/hooks/useTranslation";
import { completionPercentage } from "@/lib/puzzleUtils";
import type { PuzzleManifest, PuzzleManifestEntry } from "@/types/puzzle";

type Difficulty = "all" | "easy" | "medium" | "hard";

export default function BrowsePage() {
  const { state, setLanguage } = useProgress();
  const { t, ls, language } = useTranslation(state.language);
  const [manifest, setManifest] = useState<PuzzleManifest | null>(null);
  const [difficulty, setDifficulty] = useState<Difficulty>("all");

  useEffect(() => {
    fetch("/puzzles/manifest.json")
      .then((r) => r.json())
      .then(setManifest);
  }, []);

  if (!manifest) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-xl text-slate-400">...</div>
      </div>
    );
  }

  const difficultyLabels = {
    all: t("browse.all"),
    easy: t("browse.easy"),
    medium: t("browse.medium"),
    hard: t("browse.hard"),
  };

  const filtered =
    difficulty === "all"
      ? manifest.puzzles
      : manifest.puzzles.filter((p) => p.difficulty === difficulty);

  const puzzlesByCategory = manifest.categories
    .map((cat) => ({
      category: cat,
      puzzles: filtered.filter((p) => p.category === cat.id),
    }))
    .filter((g) => g.puzzles.length > 0);

  function getCompletionPercent(puzzle: PuzzleManifestEntry): number | undefined {
    if (state.completedPuzzles.includes(puzzle.id)) return 100;
    const progress = state.puzzleProgress[puzzle.id];
    if (!progress) return undefined;
    const totalCells =
      puzzle.gridSize.rows * puzzle.gridSize.cols -
      (progress.userGrid.flat().filter((c) => c === "#").length);
    return completionPercentage(progress.userGrid, totalCells);
  }

  return (
    <div className="min-h-screen bg-slate-50" dir={language === "he" ? "rtl" : "ltr"}>
      <TopBar
        title={t("browse.title")}
        language={state.language}
        onLanguageToggle={setLanguage}
        backHref="/"
      />
      <main className="p-4 max-w-2xl mx-auto">
        <DifficultyFilter
          selected={difficulty}
          onSelect={setDifficulty}
          labels={difficultyLabels}
        />

        <div className="mt-4 space-y-6">
          {puzzlesByCategory.map(({ category, puzzles }) => (
            <div key={category.id}>
              <h2 className="font-bold text-[#1e3a5f] text-base mb-2">
                {category.icon} {ls(category.label)}
              </h2>
              <div className="flex gap-3 overflow-x-auto pb-2">
                {puzzles.map((puzzle) => (
                  <PuzzleCard
                    key={puzzle.id}
                    puzzle={puzzle}
                    language={language}
                    difficultyLabel={difficultyLabels[puzzle.difficulty]}
                    completedLabel={t("status.complete")}
                    inProgressLabel={t("status.inProgress")}
                    completionPercent={getCompletionPercent(puzzle)}
                  />
                ))}
              </div>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
