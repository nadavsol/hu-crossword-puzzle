export interface LocalizedString {
  hu: string;
}

export type CellValue = string | "#";

export interface Clue {
  number: number;
  clue: LocalizedString;
  row: number;
  col: number;
  length: number;
}

export interface Puzzle {
  id: string;
  title: LocalizedString;
  category: string;
  difficulty: "easy" | "medium" | "hard";
  gridSize: { rows: number; cols: number };
  grid: CellValue[][];
  clues: {
    across: Clue[];
    down: Clue[];
  };
}

export interface PuzzleManifestEntry {
  id: string;
  file: string;
  title: LocalizedString;
  category: string;
  difficulty: "easy" | "medium" | "hard";
  gridSize: { rows: number; cols: number };
}

export interface Category {
  id: string;
  label: LocalizedString;
  icon: string;
}

export interface PuzzleManifest {
  puzzles: PuzzleManifestEntry[];
  categories: Category[];
}

export type Language = "hu";

export interface PuzzleProgress {
  userGrid: string[][];
  revealedCells: [number, number][];
  completed: boolean;
  completedAt: string | null;
  lastPlayed: string;
}

export interface PlayerState {
  language: Language;
  puzzleProgress: Record<string, PuzzleProgress>;
  completedPuzzles: string[];
  dailyHistory: string[];
}
