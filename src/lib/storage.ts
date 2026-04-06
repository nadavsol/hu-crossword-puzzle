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
    return JSON.parse(raw) as PlayerState;
  } catch {
    return getDefaultState();
  }
}

export function saveState(state: PlayerState): void {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}
