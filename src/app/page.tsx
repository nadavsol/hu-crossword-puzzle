"use client";

import { useEffect, useState } from "react";
import { TopBar } from "@/components/TopBar";
import { DailyPuzzleCard } from "@/components/DailyPuzzleCard";
import { useProgress } from "@/hooks/useProgress";
import { useTranslation } from "@/hooks/useTranslation";
import { getDailyPuzzleIndex } from "@/lib/puzzleUtils";
import type { PuzzleManifest } from "@/types/puzzle";

export default function Home() {
  const { state, setLanguage } = useProgress();
  const { t, ls, language } = useTranslation(state.language);
  const [manifest, setManifest] = useState<PuzzleManifest | null>(null);

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

  const today = new Date().toISOString().split("T")[0];
  const dailyIndex = getDailyPuzzleIndex(today, manifest.puzzles.length);
  const dailyPuzzle = manifest.puzzles[dailyIndex];

  const difficultyLabels = { easy: t("browse.easy"), medium: t("browse.medium"), hard: t("browse.hard") };

  // Find most recent in-progress puzzle
  const inProgressEntry = Object.entries(state.puzzleProgress)
    .filter(([, p]) => !p.completed)
    .sort(([, a], [, b]) => new Date(b.lastPlayed).getTime() - new Date(a.lastPlayed).getTime())[0];

  const inProgressManifest = inProgressEntry
    ? manifest.puzzles.find((p) => p.id === inProgressEntry[0])
    : undefined;

  return (
    <div className="min-h-screen bg-slate-50" dir={language === "he" ? "rtl" : "ltr"}>
      <TopBar
        title={t("app.title")}
        language={state.language}
        onLanguageToggle={setLanguage}
      />
      <main className="p-5 max-w-2xl mx-auto space-y-4">
        <DailyPuzzleCard
          puzzle={dailyPuzzle}
          language={language}
          startLabel={t("home.startGame")}
          dailyLabel={t("home.dailyPuzzle")}
          difficultyLabel={difficultyLabels[dailyPuzzle.difficulty]}
        />

        {inProgressManifest && inProgressEntry && (
          <a
            href={`/puzzle/${inProgressEntry[0]}`}
            className="flex items-center gap-4 bg-white rounded-xl p-4 border-2 border-slate-200"
          >
            <div className="bg-amber-100 rounded-xl w-12 h-12 flex items-center justify-center text-2xl shrink-0">
              📝
            </div>
            <div className="flex-1 min-w-0">
              <div className="font-bold text-[#1e3a5f]">
                {t("home.resume")}
              </div>
              <div className="text-sm text-slate-500">
                {ls(inProgressManifest.title)}
              </div>
            </div>
            <div className="text-2xl text-slate-400 shrink-0">›</div>
          </a>
        )}

        <a
          href="/browse"
          className="flex items-center gap-4 bg-white rounded-xl p-4 border-2 border-slate-200"
        >
          <div className="bg-blue-100 rounded-xl w-12 h-12 flex items-center justify-center text-2xl shrink-0">
            📚
          </div>
          <div className="flex-1 min-w-0">
            <div className="font-bold text-[#1e3a5f]">
              {t("home.browseAll")}
            </div>
          </div>
          <div className="text-2xl text-slate-400 shrink-0">›</div>
        </a>
      </main>
    </div>
  );
}
