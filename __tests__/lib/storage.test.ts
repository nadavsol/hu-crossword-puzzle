import { loadState, saveState, getDefaultState } from "@/lib/storage";
import type { PlayerState } from "@/types/puzzle";

beforeEach(() => {
  localStorage.clear();
});

describe("storage", () => {
  test("getDefaultState returns valid initial state", () => {
    const state = getDefaultState();
    expect(state.language).toBe("hu");
    expect(state.puzzleProgress).toEqual({});
    expect(state.completedPuzzles).toEqual([]);
    expect(state.dailyHistory).toEqual([]);
  });

  test("loadState returns default state when localStorage is empty", () => {
    const state = loadState();
    expect(state).toEqual(getDefaultState());
  });

  test("saveState and loadState round-trip", () => {
    const state: PlayerState = {
      language: "hu",
      puzzleProgress: {
        "test-001": {
          userGrid: [["A", "", "#"]],
          revealedCells: [[0, 0]],
          completed: false,
          completedAt: null,
          lastPlayed: "2026-04-06T10:00:00Z",
        },
      },
      completedPuzzles: [],
      dailyHistory: ["2026-04-05"],
    };
    saveState(state);
    expect(loadState()).toEqual(state);
  });

  test("loadState returns default state on corrupt data", () => {
    localStorage.setItem("crossword-state", "not json");
    expect(loadState()).toEqual(getDefaultState());
  });

  test("loadState merges partial/legacy state with defaults", () => {
    localStorage.setItem("crossword-state", JSON.stringify({ language: "hu" }));
    const state = loadState();
    expect(state.language).toBe("hu");
    expect(state.puzzleProgress).toEqual({});
    expect(state.completedPuzzles).toEqual([]);
    expect(state.dailyHistory).toEqual([]);
  });

  test("loadState resets invalid fields to defaults", () => {
    localStorage.setItem("crossword-state", JSON.stringify({
      language: "hu",
      puzzleProgress: "not-an-object",
      completedPuzzles: "not-an-array",
      dailyHistory: 123,
    }));
    const state = loadState();
    expect(state.puzzleProgress).toEqual({});
    expect(state.completedPuzzles).toEqual([]);
    expect(state.dailyHistory).toEqual([]);
  });
});
