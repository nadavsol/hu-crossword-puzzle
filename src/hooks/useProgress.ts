"use client";

import { useState, useCallback } from "react";
import { loadState, saveState } from "@/lib/storage";
import type { PlayerState, PuzzleProgress, Language } from "@/types/puzzle";

export function useProgress() {
  const [state, setState] = useState<PlayerState>(loadState);

  const persist = useCallback((next: PlayerState) => {
    setState(next);
    saveState(next);
  }, []);

  const setLanguage = useCallback(
    (lang: Language) => {
      persist({ ...state, language: lang });
    },
    [state, persist]
  );

  const getProgress = useCallback(
    (puzzleId: string): PuzzleProgress | undefined => {
      return state.puzzleProgress[puzzleId];
    },
    [state]
  );

  const saveProgress = useCallback(
    (puzzleId: string, progress: PuzzleProgress) => {
      const next = {
        ...state,
        puzzleProgress: { ...state.puzzleProgress, [puzzleId]: progress },
      };
      if (progress.completed && !state.completedPuzzles.includes(puzzleId)) {
        next.completedPuzzles = [...state.completedPuzzles, puzzleId];
      }
      persist(next);
    },
    [state, persist]
  );

  const markDailyCompleted = useCallback(
    (date: string) => {
      if (!state.dailyHistory.includes(date)) {
        persist({ ...state, dailyHistory: [...state.dailyHistory, date] });
      }
    },
    [state, persist]
  );

  const completionPercentage = useCallback(
    (puzzleId: string, totalCells: number): number => {
      const progress = state.puzzleProgress[puzzleId];
      if (!progress) return 0;
      const filled = progress.userGrid
        .flat()
        .filter((c) => c !== "" && c !== "#").length;
      return Math.round((filled / totalCells) * 100);
    },
    [state]
  );

  return {
    state,
    setLanguage,
    getProgress,
    saveProgress,
    markDailyCompleted,
    completionPercentage,
  };
}
