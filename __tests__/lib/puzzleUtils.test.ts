import {
  getDailyPuzzleIndex,
  countFillableCells,
  completionPercentage,
  isCellBlack,
} from "@/lib/puzzleUtils";

describe("puzzleUtils", () => {
  test("isCellBlack returns true for #", () => {
    expect(isCellBlack("#")).toBe(true);
  });

  test("isCellBlack returns false for letter", () => {
    expect(isCellBlack("A")).toBe(false);
  });

  test("isCellBlack returns false for empty string", () => {
    expect(isCellBlack("")).toBe(false);
  });

  test("countFillableCells counts non-black cells", () => {
    const grid = [
      ["A", "B", "#"],
      ["#", "C", "D"],
    ];
    expect(countFillableCells(grid)).toBe(4);
  });

  test("completionPercentage calculates correctly", () => {
    const userGrid = [
      ["A", "", "#"],
      ["#", "C", ""],
    ];
    expect(completionPercentage(userGrid, 4)).toBe(50);
  });

  test("completionPercentage returns 0 for empty grid", () => {
    const userGrid = [
      ["", "", "#"],
      ["#", "", ""],
    ];
    expect(completionPercentage(userGrid, 4)).toBe(0);
  });

  test("getDailyPuzzleIndex is deterministic for same date", () => {
    const idx1 = getDailyPuzzleIndex("2026-04-06", 100);
    const idx2 = getDailyPuzzleIndex("2026-04-06", 100);
    expect(idx1).toBe(idx2);
  });

  test("getDailyPuzzleIndex differs for different dates", () => {
    const idx1 = getDailyPuzzleIndex("2026-04-06", 100);
    const idx2 = getDailyPuzzleIndex("2026-04-07", 100);
    expect(idx1).not.toBe(idx2);
  });

  test("getDailyPuzzleIndex stays within bounds", () => {
    const idx = getDailyPuzzleIndex("2026-04-06", 5);
    expect(idx).toBeGreaterThanOrEqual(0);
    expect(idx).toBeLessThan(5);
  });
});
