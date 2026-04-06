import type { PlayerState } from "@/types/puzzle";

const STORAGE_KEY = "crossword-state";

export function getDefaultState(): PlayerState {
  return {
    language: "hu",
    puzzleProgress: {},
    completedPuzzles: [],
    dailyHistory: [],
  };
}

export function loadState(): PlayerState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return getDefaultState();
    const parsed = JSON.parse(raw);
    const defaults = getDefaultState();
    // Merge with defaults to handle schema drift / partial state
    return {
      language: parsed.language === "hu" ? "hu" : defaults.language,
      puzzleProgress:
        parsed.puzzleProgress && typeof parsed.puzzleProgress === "object"
          ? parsed.puzzleProgress
          : defaults.puzzleProgress,
      completedPuzzles: Array.isArray(parsed.completedPuzzles)
        ? parsed.completedPuzzles
        : defaults.completedPuzzles,
      dailyHistory: Array.isArray(parsed.dailyHistory)
        ? parsed.dailyHistory
        : defaults.dailyHistory,
    };
  } catch {
    return getDefaultState();
  }
}

export function saveState(state: PlayerState): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}
