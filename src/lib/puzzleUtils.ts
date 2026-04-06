export function isCellBlack(value: string): boolean {
  return value === "#";
}

export function countFillableCells(grid: string[][]): number {
  return grid.flat().filter((c) => !isCellBlack(c)).length;
}

export function completionPercentage(
  userGrid: string[][],
  totalFillable: number
): number {
  if (totalFillable === 0) return 0;
  const filled = userGrid.flat().filter((c) => c !== "" && !isCellBlack(c)).length;
  return Math.round((filled / totalFillable) * 100);
}

export function getDailyPuzzleIndex(
  dateString: string,
  totalPuzzles: number
): number {
  const epoch = new Date("2026-01-01").getTime();
  const current = new Date(dateString).getTime();
  const daysSinceEpoch = Math.floor((current - epoch) / (1000 * 60 * 60 * 24));
  return ((daysSinceEpoch % totalPuzzles) + totalPuzzles) % totalPuzzles;
}
