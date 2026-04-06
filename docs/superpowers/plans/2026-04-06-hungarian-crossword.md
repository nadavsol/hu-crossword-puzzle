# Hungarian Crossword Puzzle Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an offline-capable iPad PWA for solving Hungarian crossword puzzles, designed for elderly users with Hungarian and Hebrew UI support.

**Architecture:** Next.js static export with Tailwind CSS, served as a PWA via Serwist service worker. Puzzles are pre-generated JSON files bundled at build time. Player state persisted to localStorage. Three screens: Home, Browse, Puzzle.

**Tech Stack:** Next.js 15 (App Router, static export), TypeScript, Tailwind CSS 4, Serwist (PWA/Service Worker)

---

## File Structure

```
hu-crossword-puzzle/
  public/
    manifest.json                    # PWA web app manifest
    icons/
      icon-192.png                   # App icon 192x192
      icon-512.png                   # App icon 512x512
    puzzles/
      manifest.json                  # Puzzle index (all puzzles metadata)
      nature/
        spring-flowers-easy-001.json # Individual puzzle files
      history/
      food/
      geography/
      culture/
      everyday/
  src/
    app/
      layout.tsx                     # Root layout: html dir, lang, i18n provider, PWA meta tags
      page.tsx                       # Home screen
      browse/
        page.tsx                     # Puzzle browser with filters
      puzzle/
        [id]/
          page.tsx                   # Puzzle solving screen
      sw.ts                          # Serwist service worker entry
    components/
      CrosswordGrid.tsx              # Interactive crossword grid (tap cells, show letters)
      CluePanel.tsx                  # Across/Down clue lists with active highlighting
      HintsSheet.tsx                 # Bottom sheet: reveal letter, reveal word, check
      DailyPuzzleCard.tsx            # Home: daily puzzle hero card
      PuzzleCard.tsx                 # Browse: individual puzzle card with status
      DifficultyFilter.tsx           # Browse: filter pills (All/Easy/Medium/Hard)
      LanguageToggle.tsx             # HU/HE language switcher
      TopBar.tsx                     # Shared app header bar
      CompletionModal.tsx            # Congratulations overlay on puzzle completion
    hooks/
      usePuzzle.ts                   # Load puzzle JSON, manage grid state, check/reveal logic
      useProgress.ts                 # Read/write player progress from localStorage
      useTranslation.ts              # i18n hook: returns t() function and current language
    locales/
      hu.json                        # Hungarian UI translations
      he.json                        # Hebrew UI translations
    lib/
      puzzleUtils.ts                 # Daily puzzle selection, completion percentage calc
      storage.ts                     # Type-safe localStorage wrapper
    types/
      puzzle.ts                      # Puzzle, Clue, Manifest, PlayerState types
  next.config.ts                     # Static export config
  tailwind.config.ts                 # Tailwind config (font sizes, colors)
  tsconfig.json
  package.json
```

---

### Task 1: Project Scaffolding

**Files:**
- Create: `package.json`
- Create: `next.config.ts`
- Create: `tailwind.config.ts`
- Create: `tsconfig.json`
- Create: `src/app/layout.tsx`
- Create: `src/app/page.tsx`
- Create: `.gitignore`

- [ ] **Step 1: Initialize Next.js project**

Run:
```bash
cd /Users/nadavsolomon/Code/hu-crossword-puzzle
npx create-next-app@latest . --typescript --tailwind --eslint --app --src-dir --no-import-alias --use-npm
```

Expected: Project scaffolded with Next.js, TypeScript, Tailwind CSS, App Router, src directory.

- [ ] **Step 2: Configure static export in next.config.ts**

Replace `next.config.ts` contents:

```ts
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  output: "export",
};

export default nextConfig;
```

- [ ] **Step 3: Add .superpowers to .gitignore**

Append to `.gitignore`:
```
.superpowers/
```

- [ ] **Step 4: Clean up default page**

Replace `src/app/page.tsx` with:

```tsx
export default function Home() {
  return (
    <main className="min-h-screen bg-slate-50 flex items-center justify-center">
      <h1 className="text-3xl font-bold text-navy">Keresztrejtvény</h1>
    </main>
  );
}
```

- [ ] **Step 5: Update root layout**

Replace `src/app/layout.tsx` with:

```tsx
import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Keresztrejtvény",
  description: "Magyar keresztrejtvény iPad-ra",
};

export const viewport: Viewport = {
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
  userScalable: false,
  themeColor: "#1e3a5f",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="hu" dir="ltr">
      <head>
        <link rel="manifest" href="/manifest.json" />
        <link rel="apple-touch-icon" href="/icons/icon-192.png" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
      </head>
      <body className="antialiased bg-slate-50">{children}</body>
    </html>
  );
}
```

- [ ] **Step 6: Verify dev server starts**

Run: `npm run dev`
Expected: App loads at localhost:3000 showing "Keresztrejtvény" heading.

- [ ] **Step 7: Verify static build works**

Run: `npm run build`
Expected: Static export to `out/` directory with no errors.

- [ ] **Step 8: Commit**

```bash
git init
git add .
git commit -m "feat: scaffold Next.js project with static export"
```

---

### Task 2: TypeScript Types

**Files:**
- Create: `src/types/puzzle.ts`

- [ ] **Step 1: Define all types**

Create `src/types/puzzle.ts`:

```ts
export interface LocalizedString {
  hu: string;
  he: string;
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

export type Language = "hu" | "he";

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
```

- [ ] **Step 2: Commit**

```bash
git add src/types/puzzle.ts
git commit -m "feat: add TypeScript types for puzzle data and player state"
```

---

### Task 3: localStorage Wrapper & Progress Hook

**Files:**
- Create: `src/lib/storage.ts`
- Create: `src/hooks/useProgress.ts`
- Create: `__tests__/lib/storage.test.ts`

- [ ] **Step 1: Install testing dependencies**

Run:
```bash
npm install --save-dev jest @types/jest ts-jest @testing-library/react @testing-library/jest-dom jest-environment-jsdom
```

- [ ] **Step 2: Create Jest config**

Create `jest.config.ts`:

```ts
import type { Config } from "jest";

const config: Config = {
  testEnvironment: "jsdom",
  transform: {
    "^.+\\.tsx?$": ["ts-jest", { tsconfig: "tsconfig.json" }],
  },
  moduleNameMapper: {
    "^@/(.*)$": "<rootDir>/src/$1",
  },
};

export default config;
```

Add to `tsconfig.json` under `compilerOptions`:
```json
"baseUrl": ".",
"paths": { "@/*": ["./src/*"] }
```

- [ ] **Step 3: Write failing test for storage**

Create `__tests__/lib/storage.test.ts`:

```ts
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
      language: "he",
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
});
```

- [ ] **Step 4: Run test to verify it fails**

Run: `npx jest __tests__/lib/storage.test.ts --verbose`
Expected: FAIL — module not found.

- [ ] **Step 5: Implement storage**

Create `src/lib/storage.ts`:

```ts
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
```

- [ ] **Step 6: Run test to verify it passes**

Run: `npx jest __tests__/lib/storage.test.ts --verbose`
Expected: All 4 tests PASS.

- [ ] **Step 7: Implement useProgress hook**

Create `src/hooks/useProgress.ts`:

```ts
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
```

- [ ] **Step 8: Commit**

```bash
git add src/lib/storage.ts src/hooks/useProgress.ts src/types/puzzle.ts __tests__/lib/storage.test.ts jest.config.ts
git commit -m "feat: add localStorage wrapper and useProgress hook"
```

---

### Task 4: Internationalization (i18n)

**Files:**
- Create: `src/locales/hu.json`
- Create: `src/locales/he.json`
- Create: `src/hooks/useTranslation.ts`
- Create: `__tests__/hooks/useTranslation.test.ts`

- [ ] **Step 1: Create Hungarian translations**

Create `src/locales/hu.json`:

```json
{
  "app.title": "Keresztrejtvény",
  "home.dailyPuzzle": "Mai rejtvény",
  "home.startGame": "Játék indítása",
  "home.resume": "Félbehagyott rejtvény",
  "home.browseAll": "Összes rejtvény",
  "home.complete": "Kész",
  "browse.title": "Összes rejtvény",
  "browse.all": "Mind",
  "browse.easy": "Könnyű",
  "browse.medium": "Közepes",
  "browse.hard": "Nehéz",
  "browse.back": "Vissza",
  "puzzle.across": "Vízszintes",
  "puzzle.down": "Függőleges",
  "puzzle.back": "Vissza",
  "hints.title": "Segítség",
  "hints.revealLetter": "Betű felfedése",
  "hints.revealWord": "Szó felfedése",
  "hints.check": "Ellenőrzés",
  "puzzle.completed": "Gratulálunk!",
  "puzzle.completedMessage": "Sikeresen megoldottad a rejtvényt!",
  "puzzle.backToHome": "Vissza a főoldalra",
  "status.complete": "Kész",
  "status.inProgress": "Folyamatban"
}
```

- [ ] **Step 2: Create Hebrew translations**

Create `src/locales/he.json`:

```json
{
  "app.title": "תשבץ",
  "home.dailyPuzzle": "התשבץ של היום",
  "home.startGame": "התחל משחק",
  "home.resume": "המשך משחק",
  "home.browseAll": "כל התשבצים",
  "home.complete": "הושלם",
  "browse.title": "כל התשבצים",
  "browse.all": "הכל",
  "browse.easy": "קל",
  "browse.medium": "בינוני",
  "browse.hard": "קשה",
  "browse.back": "חזרה",
  "puzzle.across": "מאוזן",
  "puzzle.down": "מאונך",
  "puzzle.back": "חזרה",
  "hints.title": "עזרה",
  "hints.revealLetter": "גלה אות",
  "hints.revealWord": "גלה מילה",
  "hints.check": "בדיקה",
  "puzzle.completed": "כל הכבוד!",
  "puzzle.completedMessage": "פתרת את התשבץ בהצלחה!",
  "puzzle.backToHome": "חזרה לדף הבית",
  "status.complete": "הושלם",
  "status.inProgress": "בתהליך"
}
```

- [ ] **Step 3: Write failing test for useTranslation**

Create `__tests__/hooks/useTranslation.test.ts`:

```ts
import { renderHook } from "@testing-library/react";
import { useTranslation } from "@/hooks/useTranslation";

describe("useTranslation", () => {
  test("returns Hungarian translation by default", () => {
    const { result } = renderHook(() => useTranslation("hu"));
    expect(result.current.t("app.title")).toBe("Keresztrejtvény");
  });

  test("returns Hebrew translation", () => {
    const { result } = renderHook(() => useTranslation("he"));
    expect(result.current.t("app.title")).toBe("תשבץ");
  });

  test("returns key when translation is missing", () => {
    const { result } = renderHook(() => useTranslation("hu"));
    expect(result.current.t("nonexistent.key")).toBe("nonexistent.key");
  });

  test("localizedString extracts correct language", () => {
    const { result } = renderHook(() => useTranslation("hu"));
    expect(
      result.current.ls({ hu: "Magyar", he: "הונגרית" })
    ).toBe("Magyar");
  });

  test("localizedString extracts Hebrew", () => {
    const { result } = renderHook(() => useTranslation("he"));
    expect(
      result.current.ls({ hu: "Magyar", he: "הונגרית" })
    ).toBe("הונגרית");
  });
});
```

- [ ] **Step 4: Run test to verify it fails**

Run: `npx jest __tests__/hooks/useTranslation.test.ts --verbose`
Expected: FAIL — module not found.

- [ ] **Step 5: Implement useTranslation**

Create `src/hooks/useTranslation.ts`:

```ts
import { useMemo } from "react";
import type { Language, LocalizedString } from "@/types/puzzle";
import hu from "@/locales/hu.json";
import he from "@/locales/he.json";

const translations: Record<Language, Record<string, string>> = { hu, he };

export function useTranslation(language: Language) {
  return useMemo(() => {
    const dict = translations[language];

    function t(key: string): string {
      return dict[key] ?? key;
    }

    function ls(localized: LocalizedString): string {
      return localized[language];
    }

    return { t, ls, language, dir: language === "he" ? "rtl" as const : "ltr" as const };
  }, [language]);
}
```

- [ ] **Step 6: Run test to verify it passes**

Run: `npx jest __tests__/hooks/useTranslation.test.ts --verbose`
Expected: All 5 tests PASS.

- [ ] **Step 7: Commit**

```bash
git add src/locales/ src/hooks/useTranslation.ts __tests__/hooks/useTranslation.test.ts
git commit -m "feat: add i18n with Hungarian and Hebrew translations"
```

---

### Task 5: Puzzle Utility Functions

**Files:**
- Create: `src/lib/puzzleUtils.ts`
- Create: `__tests__/lib/puzzleUtils.test.ts`

- [ ] **Step 1: Write failing tests**

Create `__tests__/lib/puzzleUtils.test.ts`:

```ts
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
    // 2 filled out of 4 fillable = 50%
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
```

- [ ] **Step 2: Run test to verify it fails**

Run: `npx jest __tests__/lib/puzzleUtils.test.ts --verbose`
Expected: FAIL — module not found.

- [ ] **Step 3: Implement puzzleUtils**

Create `src/lib/puzzleUtils.ts`:

```ts
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
```

- [ ] **Step 4: Run test to verify it passes**

Run: `npx jest __tests__/lib/puzzleUtils.test.ts --verbose`
Expected: All 9 tests PASS.

- [ ] **Step 5: Commit**

```bash
git add src/lib/puzzleUtils.ts __tests__/lib/puzzleUtils.test.ts
git commit -m "feat: add puzzle utility functions"
```

---

### Task 6: Sample Puzzle Data

**Files:**
- Create: `public/puzzles/manifest.json`
- Create: `public/puzzles/nature/spring-flowers-easy-001.json`
- Create: `public/puzzles/food/hungarian-cuisine-easy-001.json`
- Create: `public/puzzles/history/hungarian-kings-medium-001.json`

- [ ] **Step 1: Create puzzle manifest**

Create `public/puzzles/manifest.json`:

```json
{
  "puzzles": [
    {
      "id": "nature-spring-flowers-easy-001",
      "file": "nature/spring-flowers-easy-001.json",
      "title": { "hu": "Tavaszi virágok", "he": "פרחי אביב" },
      "category": "nature",
      "difficulty": "easy",
      "gridSize": { "rows": 5, "cols": 5 }
    },
    {
      "id": "food-hungarian-cuisine-easy-001",
      "file": "food/hungarian-cuisine-easy-001.json",
      "title": { "hu": "Magyar konyha", "he": "מטבח הונגרי" },
      "category": "food",
      "difficulty": "easy",
      "gridSize": { "rows": 5, "cols": 5 }
    },
    {
      "id": "history-hungarian-kings-medium-001",
      "file": "history/hungarian-kings-medium-001.json",
      "title": { "hu": "Magyar királyok", "he": "מלכי הונגריה" },
      "category": "history",
      "difficulty": "medium",
      "gridSize": { "rows": 7, "cols": 7 }
    }
  ],
  "categories": [
    { "id": "nature", "label": { "hu": "Természet", "he": "טבע" }, "icon": "🌿" },
    { "id": "history", "label": { "hu": "Történelem", "he": "היסטוריה" }, "icon": "🏛️" },
    { "id": "food", "label": { "hu": "Ételek és italok", "he": "אוכל ושתייה" }, "icon": "🍲" },
    { "id": "geography", "label": { "hu": "Földrajz", "he": "גאוגרפיה" }, "icon": "🗺️" },
    { "id": "culture", "label": { "hu": "Kultúra", "he": "תרבות" }, "icon": "🎭" },
    { "id": "everyday", "label": { "hu": "Hétköznapi élet", "he": "חיי יומיום" }, "icon": "🏠" }
  ]
}
```

- [ ] **Step 2: Create nature puzzle**

Create directories and `public/puzzles/nature/spring-flowers-easy-001.json`:

```bash
mkdir -p public/puzzles/nature public/puzzles/food public/puzzles/history public/puzzles/geography public/puzzles/culture public/puzzles/everyday
```

```json
{
  "id": "nature-spring-flowers-easy-001",
  "title": { "hu": "Tavaszi virágok", "he": "פרחי אביב" },
  "category": "nature",
  "difficulty": "easy",
  "gridSize": { "rows": 5, "cols": 5 },
  "grid": [
    ["R", "Ó", "Z", "S", "A"],
    ["Ö", "#", "Ö", "#", "S"],
    ["Z", "S", "L", "D", "Z"],
    ["S", "#", "É", "#", "T"],
    ["A", "S", "T", "E", "R"]
  ],
  "clues": {
    "across": [
      { "number": 1, "clue": { "hu": "Tüskés szárú kerti virág", "he": "פרח גינה עם גבעול קוצני" }, "row": 0, "col": 0, "length": 5 },
      { "number": 3, "clue": { "hu": "Zöld növény a kertben", "he": "צמח ירוק בגינה" }, "row": 2, "col": 0, "length": 5 },
      { "number": 5, "clue": { "hu": "Őszi virág, csillag alakú", "he": "פרח סתווי בצורת כוכב" }, "row": 4, "col": 0, "length": 5 }
    ],
    "down": [
      { "number": 1, "clue": { "hu": "Tavasz hónapja előtti virág", "he": "פרח שלפני חודש האביב" }, "row": 0, "col": 0, "length": 5 },
      { "number": 2, "clue": { "hu": "Lila kerti virág", "he": "פרח גינה סגול" }, "row": 0, "col": 2, "length": 5 },
      { "number": 4, "clue": { "hu": "Illatos tavaszi virág", "he": "פרח אביבי ריחני" }, "row": 0, "col": 4, "length": 5 }
    ]
  }
}
```

- [ ] **Step 3: Create food puzzle**

Create `public/puzzles/food/hungarian-cuisine-easy-001.json`:

```json
{
  "id": "food-hungarian-cuisine-easy-001",
  "title": { "hu": "Magyar konyha", "he": "מטבח הונגרי" },
  "category": "food",
  "difficulty": "easy",
  "gridSize": { "rows": 5, "cols": 5 },
  "grid": [
    ["G", "U", "L", "Y", "Á"],
    ["Ő", "#", "E", "#", "L"],
    ["Z", "E", "V", "E", "S"],
    ["E", "#", "E", "#", "#"],
    ["S", "A", "S", "A", "S"]
  ],
  "clues": {
    "across": [
      { "number": 1, "clue": { "hu": "Híres magyar húsétel", "he": "תבשיל בשר הונגרי מפורסם" }, "row": 0, "col": 0, "length": 5 },
      { "number": 3, "clue": { "hu": "Forró folyadék étel", "he": "מאכל נוזלי חם" }, "row": 2, "col": 0, "length": 5 },
      { "number": 5, "clue": { "hu": "Fűszer, szárított növény", "he": "תבלין, צמח מיובש" }, "row": 4, "col": 0, "length": 5 }
    ],
    "down": [
      { "number": 1, "clue": { "hu": "Főzés helye", "he": "מקום הבישול" }, "row": 0, "col": 0, "length": 5 },
      { "number": 2, "clue": { "hu": "Csípős vagy édes, piros", "he": "חריף או מתוק, אדום" }, "row": 0, "col": 2, "length": 5 },
      { "number": 4, "clue": { "hu": "Gyümölcs, zöld vagy piros", "he": "פרי, ירוק או אדום" }, "row": 0, "col": 4, "length": 3 }
    ]
  }
}
```

- [ ] **Step 4: Create history puzzle**

Create `public/puzzles/history/hungarian-kings-medium-001.json`:

```json
{
  "id": "history-hungarian-kings-medium-001",
  "title": { "hu": "Magyar királyok", "he": "מלכי הונגריה" },
  "category": "history",
  "difficulty": "medium",
  "gridSize": { "rows": 7, "cols": 7 },
  "grid": [
    ["I", "S", "T", "V", "Á", "N", "#"],
    ["#", "Z", "#", "#", "#", "A", "G"],
    ["B", "É", "L", "A", "#", "G", "Y"],
    ["#", "C", "#", "N", "O", "Y", "#"],
    ["#", "H", "U", "D", "#", "#", "#"],
    ["K", "E", "R", "E", "S", "Z", "T"],
    ["#", "N", "#", "#", "#", "#", "#"]
  ],
  "clues": {
    "across": [
      { "number": 1, "clue": { "hu": "Az első magyar király", "he": "המלך הראשון של הונגריה" }, "row": 0, "col": 0, "length": 6 },
      { "number": 3, "clue": { "hu": "Több magyar király neve, három betűs", "he": "שם של כמה מלכים הונגרים, שלוש אותיות" }, "row": 2, "col": 0, "length": 4 },
      { "number": 5, "clue": { "hu": "Mátyás király mellék...", "he": "הכינוי של המלך מאטיאש" }, "row": 4, "col": 1, "length": 3 },
      { "number": 6, "clue": { "hu": "Vallási szertartás, István király kapta", "he": "טקס דתי, שקיבל המלך אישטוון" }, "row": 5, "col": 0, "length": 7 }
    ],
    "down": [
      { "number": 1, "clue": { "hu": "István apja, fejdelem", "he": "אביו של אישטוון, נסיך" }, "row": 0, "col": 1, "length": 7 },
      { "number": 2, "clue": { "hu": "Király felsége, magyar város", "he": "בעל המלכה, עיר הונגרית" }, "row": 1, "col": 5, "length": 4 },
      { "number": 4, "clue": { "hu": "Anonymus nyelve", "he": "השפה של אנונימוס" }, "row": 1, "col": 6, "length": 2 }
    ]
  }
}
```

- [ ] **Step 5: Commit**

```bash
git add public/puzzles/
git commit -m "feat: add sample puzzle data with 3 puzzles"
```

---

### Task 7: PWA Manifest & Icons

**Files:**
- Create: `public/manifest.json`
- Create: `public/icons/icon-192.png`
- Create: `public/icons/icon-512.png`

- [ ] **Step 1: Create PWA manifest**

Create `public/manifest.json`:

```json
{
  "name": "Keresztrejtvény",
  "short_name": "Rejtvény",
  "description": "Magyar keresztrejtvény iPad-ra",
  "start_url": "/",
  "display": "standalone",
  "orientation": "any",
  "background_color": "#f0f4f8",
  "theme_color": "#1e3a5f",
  "icons": [
    { "src": "/icons/icon-192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/icons/icon-512.png", "sizes": "512x512", "type": "image/png" }
  ]
}
```

- [ ] **Step 2: Generate placeholder icons**

Create `public/icons/` directory and generate simple placeholder icons using an HTML canvas approach or any image tool. The icons should be a navy (#1e3a5f) square with a white puzzle piece emoji or the letter "K" centered.

Run:
```bash
mkdir -p public/icons
# Generate simple placeholder SVG icons (will be replaced with designed icons later)
cat > public/icons/icon.svg << 'SVG'
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
  <rect width="512" height="512" rx="64" fill="#1e3a5f"/>
  <text x="256" y="300" text-anchor="middle" font-size="240" font-family="system-ui" font-weight="bold" fill="white">K</text>
</svg>
SVG
```

Convert SVG to PNG using the `sharp` package or equivalent tool during build, or use the SVG directly for development. For production, create proper 192x192 and 512x512 PNG files.

- [ ] **Step 3: Commit**

```bash
git add public/manifest.json public/icons/
git commit -m "feat: add PWA manifest and placeholder icons"
```

---

### Task 8: Service Worker with Serwist

**Files:**
- Modify: `next.config.ts`
- Create: `src/app/sw.ts`
- Modify: `src/app/layout.tsx`

- [ ] **Step 1: Install Serwist**

Run:
```bash
npm install @serwist/next
npm install --save-dev serwist
```

- [ ] **Step 2: Update next.config.ts**

Replace `next.config.ts`:

```ts
import withSerwistInit from "@serwist/next";

const withSerwist = withSerwistInit({
  swSrc: "src/app/sw.ts",
  swDest: "public/sw.js",
});

export default withSerwist({
  output: "export",
});
```

- [ ] **Step 3: Create service worker entry**

Create `src/app/sw.ts`:

```ts
import { defaultCache } from "@serwist/next/worker";
import type { PrecacheEntry, SerwistGlobalConfig } from "serwist";
import { Serwist } from "serwist";

declare global {
  interface WorkerGlobalScope extends SerwistGlobalConfig {
    __SW_MANIFEST: (PrecacheEntry | string)[] | undefined;
  }
}

declare const self: ServiceWorkerGlobalScope & typeof globalThis;

const serwist = new Serwist({
  precacheEntries: self.__SW_MANIFEST,
  skipWaiting: true,
  clientsClaim: true,
  navigationPreload: false,
  runtimeCaching: defaultCache,
});

serwist.addEventListeners();
```

- [ ] **Step 4: Register service worker in layout**

Add a service worker registration component. Create `src/components/ServiceWorkerRegistrar.tsx`:

```tsx
"use client";

import { useEffect } from "react";

export function ServiceWorkerRegistrar() {
  useEffect(() => {
    if ("serviceWorker" in navigator) {
      navigator.serviceWorker.register("/sw.js");
    }
  }, []);
  return null;
}
```

Add `<ServiceWorkerRegistrar />` to `src/app/layout.tsx` inside the `<body>` tag, before `{children}`.

- [ ] **Step 5: Verify build still works**

Run: `npm run build`
Expected: Builds successfully with service worker generated.

- [ ] **Step 6: Commit**

```bash
git add next.config.ts src/app/sw.ts src/components/ServiceWorkerRegistrar.tsx src/app/layout.tsx
git commit -m "feat: add Serwist service worker for offline PWA support"
```

---

### Task 9: TopBar and LanguageToggle Components

**Files:**
- Create: `src/components/TopBar.tsx`
- Create: `src/components/LanguageToggle.tsx`

- [ ] **Step 1: Implement LanguageToggle**

Create `src/components/LanguageToggle.tsx`:

```tsx
"use client";

import type { Language } from "@/types/puzzle";

interface LanguageToggleProps {
  language: Language;
  onToggle: (lang: Language) => void;
}

export function LanguageToggle({ language, onToggle }: LanguageToggleProps) {
  return (
    <button
      onClick={() => onToggle(language === "hu" ? "he" : "hu")}
      className="bg-[#2d5a8e] text-white px-3 py-1.5 rounded-lg text-sm font-medium
                 min-w-[44px] min-h-[44px] flex items-center justify-center
                 active:bg-[#1e3a5f] transition-colors"
      aria-label={language === "hu" ? "Switch to Hebrew" : "Switch to Hungarian"}
    >
      {language === "hu" ? "HU | עב" : "עב | HU"}
    </button>
  );
}
```

- [ ] **Step 2: Implement TopBar**

Create `src/components/TopBar.tsx`:

```tsx
"use client";

import type { Language } from "@/types/puzzle";
import { LanguageToggle } from "./LanguageToggle";

interface TopBarProps {
  title: string;
  language: Language;
  onLanguageToggle: (lang: Language) => void;
  backHref?: string;
  rightContent?: React.ReactNode;
}

export function TopBar({
  title,
  language,
  onLanguageToggle,
  backHref,
  rightContent,
}: TopBarProps) {
  return (
    <header className="bg-[#1e3a5f] text-white px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        {backHref && (
          <a
            href={backHref}
            className="text-xl min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label="Back"
          >
            ←
          </a>
        )}
        <h1 className="text-lg font-bold">{title}</h1>
      </div>
      <div className="flex items-center gap-3">
        {rightContent}
        <LanguageToggle language={language} onToggle={onLanguageToggle} />
      </div>
    </header>
  );
}
```

- [ ] **Step 3: Commit**

```bash
git add src/components/TopBar.tsx src/components/LanguageToggle.tsx
git commit -m "feat: add TopBar and LanguageToggle components"
```

---

### Task 10: Home Screen

**Files:**
- Create: `src/components/DailyPuzzleCard.tsx`
- Modify: `src/app/page.tsx`
- Modify: `src/app/layout.tsx`

- [ ] **Step 1: Implement DailyPuzzleCard**

Create `src/components/DailyPuzzleCard.tsx`:

```tsx
"use client";

import type { PuzzleManifestEntry, Language } from "@/types/puzzle";

interface DailyPuzzleCardProps {
  puzzle: PuzzleManifestEntry;
  language: Language;
  startLabel: string;
  dailyLabel: string;
  difficultyLabel: string;
}

export function DailyPuzzleCard({
  puzzle,
  language,
  startLabel,
  dailyLabel,
  difficultyLabel,
}: DailyPuzzleCardProps) {
  return (
    <a
      href={`/puzzle/${puzzle.id}`}
      className="block bg-gradient-to-br from-[#1e3a5f] to-[#2d5a8e] rounded-2xl p-6 text-white shadow-lg"
    >
      <div className="text-xs uppercase tracking-wider opacity-80 mb-1">
        {dailyLabel}
      </div>
      <div className="text-2xl font-bold mb-1">
        {puzzle.title[language]}
      </div>
      <div className="text-sm opacity-80 mb-4">
        {difficultyLabel} · {puzzle.gridSize.rows}×{puzzle.gridSize.cols}
      </div>
      <div className="inline-block bg-white text-[#1e3a5f] px-6 py-3 rounded-xl font-bold text-base">
        {startLabel} ▶
      </div>
    </a>
  );
}
```

- [ ] **Step 2: Implement Home screen**

Replace `src/app/page.tsx`:

```tsx
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
```

- [ ] **Step 3: Update layout.tsx to include dir support**

Update `src/app/layout.tsx` — change the `<html>` tag to remove the hardcoded `dir` since it will be controlled per-page:

```tsx
<html lang="hu">
```

(Remove `dir="ltr"` from the html tag — each page sets its own `dir`.)

- [ ] **Step 4: Verify in dev server**

Run: `npm run dev`
Expected: Home screen shows with daily puzzle card, browse button. Language toggle switches between HU/HE.

- [ ] **Step 5: Commit**

```bash
git add src/app/page.tsx src/components/DailyPuzzleCard.tsx src/app/layout.tsx
git commit -m "feat: implement home screen with daily puzzle and navigation"
```

---

### Task 11: Puzzle Browser Screen

**Files:**
- Create: `src/components/DifficultyFilter.tsx`
- Create: `src/components/PuzzleCard.tsx`
- Create: `src/app/browse/page.tsx`

- [ ] **Step 1: Implement DifficultyFilter**

Create `src/components/DifficultyFilter.tsx`:

```tsx
"use client";

type Difficulty = "all" | "easy" | "medium" | "hard";

interface DifficultyFilterProps {
  selected: Difficulty;
  onSelect: (d: Difficulty) => void;
  labels: Record<Difficulty, string>;
}

export function DifficultyFilter({ selected, onSelect, labels }: DifficultyFilterProps) {
  const options: Difficulty[] = ["all", "easy", "medium", "hard"];

  return (
    <div className="flex gap-2 overflow-x-auto pb-2">
      {options.map((d) => (
        <button
          key={d}
          onClick={() => onSelect(d)}
          className={`px-4 py-2 rounded-full text-sm font-semibold whitespace-nowrap
                     min-h-[44px] transition-colors
                     ${
                       selected === d
                         ? "bg-[#1e3a5f] text-white"
                         : "bg-white text-[#1e3a5f] border-2 border-slate-200"
                     }`}
        >
          {labels[d]}
        </button>
      ))}
    </div>
  );
}
```

- [ ] **Step 2: Implement PuzzleCard**

Create `src/components/PuzzleCard.tsx`:

```tsx
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
```

- [ ] **Step 3: Implement Browse page**

Create `src/app/browse/page.tsx`:

```tsx
"use client";

import { useEffect, useState } from "react";
import { TopBar } from "@/components/TopBar";
import { DifficultyFilter } from "@/components/DifficultyFilter";
import { PuzzleCard } from "@/components/PuzzleCard";
import { useProgress } from "@/hooks/useProgress";
import { useTranslation } from "@/hooks/useTranslation";
import { countFillableCells, completionPercentage } from "@/lib/puzzleUtils";
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
```

- [ ] **Step 4: Verify in dev server**

Run: `npm run dev`, navigate to `/browse`
Expected: Shows difficulty filters and puzzle cards grouped by category.

- [ ] **Step 5: Commit**

```bash
git add src/app/browse/ src/components/DifficultyFilter.tsx src/components/PuzzleCard.tsx
git commit -m "feat: implement puzzle browser with filters and categories"
```

---

### Task 12: Crossword Grid Component

**Files:**
- Create: `src/components/CrosswordGrid.tsx`

This is the core interactive component. It handles cell selection, direction toggling, keyboard input, and visual highlighting.

- [ ] **Step 1: Implement CrosswordGrid**

Create `src/components/CrosswordGrid.tsx`:

```tsx
"use client";

import { useCallback } from "react";
import type { Clue } from "@/types/puzzle";

interface CrosswordGridProps {
  solutionGrid: string[][];
  userGrid: string[][];
  selectedCell: [number, number] | null;
  direction: "across" | "down";
  activeClue: Clue | null;
  revealedCells: [number, number][];
  incorrectCells: [number, number][];
  onCellClick: (row: number, col: number) => void;
  onKeyInput: (key: string) => void;
}

export function CrosswordGrid({
  solutionGrid,
  userGrid,
  selectedCell,
  direction,
  activeClue,
  revealedCells,
  incorrectCells,
  onCellClick,
  onKeyInput,
}: CrosswordGridProps) {
  const rows = solutionGrid.length;
  const cols = solutionGrid[0].length;

  // Calculate cell numbers
  const cellNumbers: Record<string, number> = {};
  let num = 1;
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      if (solutionGrid[r][c] === "#") continue;
      const startsAcross = (c === 0 || solutionGrid[r][c - 1] === "#") &&
        c + 1 < cols && solutionGrid[r][c + 1] !== "#";
      const startsDown = (r === 0 || solutionGrid[r - 1][c] === "#") &&
        r + 1 < rows && solutionGrid[r + 1][c] !== "#";
      if (startsAcross || startsDown) {
        cellNumbers[`${r}-${c}`] = num++;
      }
    }
  }

  // Determine which cells are part of the active word
  const activeCells = new Set<string>();
  if (activeClue) {
    for (let i = 0; i < activeClue.length; i++) {
      const r = direction === "across" ? activeClue.row : activeClue.row + i;
      const c = direction === "across" ? activeClue.col + i : activeClue.col;
      activeCells.add(`${r}-${c}`);
    }
  }

  const isRevealed = (r: number, c: number) =>
    revealedCells.some(([rr, cc]) => rr === r && cc === c);

  const isIncorrect = (r: number, c: number) =>
    incorrectCells.some(([rr, cc]) => rr === r && cc === c);

  // Hidden input for keyboard capture
  const handleInputChange = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const val = e.target.value;
      if (val) {
        onKeyInput(val.toUpperCase().slice(-1));
        e.target.value = "";
      }
    },
    [onKeyInput]
  );

  const handleInputKeyDown = useCallback(
    (e: React.KeyboardEvent<HTMLInputElement>) => {
      if (e.key === "Backspace") {
        e.preventDefault();
        onKeyInput("BACKSPACE");
      }
    },
    [onKeyInput]
  );

  return (
    <div className="relative">
      {/* Hidden input for keyboard */}
      <input
        id="grid-input"
        type="text"
        autoComplete="off"
        autoCorrect="off"
        autoCapitalize="characters"
        spellCheck={false}
        className="absolute opacity-0 w-0 h-0"
        onChange={handleInputChange}
        onKeyDown={handleInputKeyDown}
        inputMode="text"
      />

      <div
        className="grid gap-[2px] w-full max-w-[500px] mx-auto"
        style={{ gridTemplateColumns: `repeat(${cols}, 1fr)` }}
      >
        {solutionGrid.map((row, r) =>
          row.map((cell, c) => {
            if (cell === "#") {
              return (
                <div
                  key={`${r}-${c}`}
                  className="aspect-square bg-slate-800 rounded-sm"
                />
              );
            }

            const isSelected =
              selectedCell?.[0] === r && selectedCell?.[1] === c;
            const isActive = activeCells.has(`${r}-${c}`);
            const cellNum = cellNumbers[`${r}-${c}`];
            const userValue = userGrid[r]?.[c] ?? "";
            const revealed = isRevealed(r, c);
            const incorrect = isIncorrect(r, c);

            return (
              <button
                key={`${r}-${c}`}
                onClick={() => {
                  onCellClick(r, c);
                  document.getElementById("grid-input")?.focus();
                }}
                className={`aspect-square border-2 rounded-sm relative flex items-center justify-center
                           text-lg font-bold min-w-[44px] min-h-[44px] transition-colors
                           ${isSelected
                             ? "bg-blue-200 border-blue-500"
                             : isActive
                               ? "bg-blue-50 border-slate-400"
                               : "bg-white border-slate-300"
                           }
                           ${incorrect ? "text-red-600" : revealed ? "text-blue-600" : "text-[#1e3a5f]"}
                           `}
                aria-label={`Row ${r + 1}, Column ${c + 1}${userValue ? `, letter ${userValue}` : ""}`}
              >
                {cellNum && (
                  <span className="absolute top-0.5 left-1 text-[9px] text-slate-400 font-normal">
                    {cellNum}
                  </span>
                )}
                {userValue}
              </button>
            );
          })
        )}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Verify it renders**

Import and render a test grid in the dev server to visually verify. This will be fully integrated in Task 14.

- [ ] **Step 3: Commit**

```bash
git add src/components/CrosswordGrid.tsx
git commit -m "feat: implement interactive crossword grid component"
```

---

### Task 13: CluePanel and HintsSheet Components

**Files:**
- Create: `src/components/CluePanel.tsx`
- Create: `src/components/HintsSheet.tsx`
- Create: `src/components/CompletionModal.tsx`

- [ ] **Step 1: Implement CluePanel**

Create `src/components/CluePanel.tsx`:

```tsx
"use client";

import type { Clue, Language } from "@/types/puzzle";

interface CluePanelProps {
  acrossClues: Clue[];
  downClues: Clue[];
  activeClueNumber: number | null;
  activeDirection: "across" | "down";
  language: Language;
  acrossLabel: string;
  downLabel: string;
  onClueClick: (clue: Clue, direction: "across" | "down") => void;
}

export function CluePanel({
  acrossClues,
  downClues,
  activeClueNumber,
  activeDirection,
  language,
  acrossLabel,
  downLabel,
  onClueClick,
}: CluePanelProps) {
  const renderClue = (clue: Clue, direction: "across" | "down") => {
    const isActive =
      clue.number === activeClueNumber && direction === activeDirection;
    return (
      <button
        key={`${direction}-${clue.number}`}
        onClick={() => onClueClick(clue, direction)}
        className={`block w-full text-left px-2 py-1.5 rounded text-sm min-h-[44px]
                   flex items-start gap-2 transition-colors
                   ${isActive ? "bg-blue-100" : "hover:bg-slate-50"}`}
      >
        <span className="font-bold text-blue-600 shrink-0">{clue.number}.</span>
        <span className="text-slate-700">{clue.clue[language]}</span>
      </button>
    );
  };

  return (
    <div className="overflow-y-auto">
      <h3 className="font-bold text-[#1e3a5f] text-sm border-b-2 border-blue-100 pb-1 mb-2 px-2">
        {acrossLabel} ➡️
      </h3>
      <div className="space-y-0.5 mb-4">
        {acrossClues.map((c) => renderClue(c, "across"))}
      </div>

      <h3 className="font-bold text-[#1e3a5f] text-sm border-b-2 border-blue-100 pb-1 mb-2 px-2">
        {downLabel} ⬇️
      </h3>
      <div className="space-y-0.5">
        {downClues.map((c) => renderClue(c, "down"))}
      </div>
    </div>
  );
}
```

- [ ] **Step 2: Implement HintsSheet**

Create `src/components/HintsSheet.tsx`:

```tsx
"use client";

interface HintsSheetProps {
  isOpen: boolean;
  onClose: () => void;
  onRevealLetter: () => void;
  onRevealWord: () => void;
  onCheck: () => void;
  labels: {
    title: string;
    revealLetter: string;
    revealWord: string;
    check: string;
  };
}

export function HintsSheet({
  isOpen,
  onClose,
  onRevealLetter,
  onRevealWord,
  onCheck,
  labels,
}: HintsSheetProps) {
  if (!isOpen) return null;

  const buttons = [
    { label: labels.revealLetter, icon: "🔤", onClick: onRevealLetter },
    { label: labels.revealWord, icon: "📝", onClick: onRevealWord },
    { label: labels.check, icon: "✅", onClick: onCheck },
  ];

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/30 z-40"
        onClick={onClose}
      />
      {/* Sheet */}
      <div className="fixed bottom-0 left-0 right-0 bg-white rounded-t-2xl z-50 p-6 shadow-2xl">
        <h3 className="text-lg font-bold text-[#1e3a5f] mb-4 text-center">
          {labels.title}
        </h3>
        <div className="space-y-3 max-w-md mx-auto">
          {buttons.map((btn) => (
            <button
              key={btn.label}
              onClick={() => {
                btn.onClick();
                onClose();
              }}
              className="w-full flex items-center gap-4 p-4 bg-slate-50 rounded-xl
                         text-left text-base font-semibold text-[#1e3a5f]
                         min-h-[56px] active:bg-slate-100 transition-colors"
            >
              <span className="text-2xl">{btn.icon}</span>
              {btn.label}
            </button>
          ))}
        </div>
      </div>
    </>
  );
}
```

- [ ] **Step 3: Implement CompletionModal**

Create `src/components/CompletionModal.tsx`:

```tsx
"use client";

interface CompletionModalProps {
  isOpen: boolean;
  title: string;
  message: string;
  backLabel: string;
  backHref: string;
}

export function CompletionModal({
  isOpen,
  title,
  message,
  backLabel,
  backHref,
}: CompletionModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black/40 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl p-8 max-w-sm w-full text-center shadow-2xl">
        <div className="text-5xl mb-4">🎉</div>
        <h2 className="text-2xl font-bold text-[#1e3a5f] mb-2">{title}</h2>
        <p className="text-slate-600 mb-6">{message}</p>
        <a
          href={backHref}
          className="inline-block bg-[#1e3a5f] text-white px-8 py-3 rounded-xl
                     font-bold text-base min-h-[44px]"
        >
          {backLabel}
        </a>
      </div>
    </div>
  );
}
```

- [ ] **Step 4: Commit**

```bash
git add src/components/CluePanel.tsx src/components/HintsSheet.tsx src/components/CompletionModal.tsx
git commit -m "feat: add CluePanel, HintsSheet, and CompletionModal components"
```

---

### Task 14: Puzzle Game Logic Hook (usePuzzle)

**Files:**
- Create: `src/hooks/usePuzzle.ts`

- [ ] **Step 1: Implement usePuzzle hook**

Create `src/hooks/usePuzzle.ts`:

```tsx
"use client";

import { useState, useCallback, useEffect } from "react";
import type { Puzzle, Clue, PuzzleProgress } from "@/types/puzzle";
import { isCellBlack, countFillableCells } from "@/lib/puzzleUtils";

interface UsePuzzleOptions {
  puzzle: Puzzle;
  savedProgress?: PuzzleProgress;
  onSaveProgress: (progress: PuzzleProgress) => void;
}

export function usePuzzle({ puzzle, savedProgress, onSaveProgress }: UsePuzzleOptions) {
  const { grid, clues } = puzzle;
  const rows = grid.length;
  const cols = grid[0].length;

  const [userGrid, setUserGrid] = useState<string[][]>(() => {
    if (savedProgress) return savedProgress.userGrid;
    return grid.map((row) => row.map((cell) => (isCellBlack(cell) ? "#" : "")));
  });

  const [selectedCell, setSelectedCell] = useState<[number, number] | null>(null);
  const [direction, setDirection] = useState<"across" | "down">("across");
  const [revealedCells, setRevealedCells] = useState<[number, number][]>(
    savedProgress?.revealedCells ?? []
  );
  const [incorrectCells, setIncorrectCells] = useState<[number, number][]>([]);
  const [completed, setCompleted] = useState(savedProgress?.completed ?? false);

  // Find which clue a cell belongs to
  const findClue = useCallback(
    (row: number, col: number, dir: "across" | "down"): Clue | null => {
      const clueList = dir === "across" ? clues.across : clues.down;
      return (
        clueList.find((c) => {
          for (let i = 0; i < c.length; i++) {
            const r = dir === "across" ? c.row : c.row + i;
            const cc = dir === "across" ? c.col + i : c.col;
            if (r === row && cc === col) return true;
          }
          return false;
        }) ?? null
      );
    },
    [clues]
  );

  const activeClue = selectedCell ? findClue(selectedCell[0], selectedCell[1], direction) : null;

  // Cell click handler
  const onCellClick = useCallback(
    (row: number, col: number) => {
      if (isCellBlack(grid[row][col])) return;

      if (selectedCell?.[0] === row && selectedCell?.[1] === col) {
        // Toggle direction
        const newDir = direction === "across" ? "down" : "across";
        // Only toggle if there's a clue in the other direction
        if (findClue(row, col, newDir)) {
          setDirection(newDir);
        }
      } else {
        setSelectedCell([row, col]);
        setIncorrectCells([]);
      }
    },
    [selectedCell, direction, grid, findClue]
  );

  // Check if puzzle is complete
  const checkCompletion = useCallback(
    (g: string[][]) => {
      for (let r = 0; r < rows; r++) {
        for (let c = 0; c < cols; c++) {
          if (!isCellBlack(grid[r][c]) && g[r][c] !== grid[r][c]) {
            return false;
          }
        }
      }
      return true;
    },
    [grid, rows, cols]
  );

  // Key input handler
  const onKeyInput = useCallback(
    (key: string) => {
      if (!selectedCell || completed) return;
      const [row, col] = selectedCell;

      if (key === "BACKSPACE") {
        const newGrid = userGrid.map((r) => [...r]);
        newGrid[row][col] = "";
        setUserGrid(newGrid);
        setIncorrectCells([]);

        // Move backwards
        const prevR = direction === "across" ? row : row - 1;
        const prevC = direction === "across" ? col - 1 : col;
        if (prevR >= 0 && prevC >= 0 && !isCellBlack(grid[prevR][prevC])) {
          setSelectedCell([prevR, prevC]);
        }
        return;
      }

      // Place letter
      const newGrid = userGrid.map((r) => [...r]);
      newGrid[row][col] = key;
      setUserGrid(newGrid);
      setIncorrectCells([]);

      // Check completion
      if (checkCompletion(newGrid)) {
        setCompleted(true);
      }

      // Advance to next cell
      const nextR = direction === "across" ? row : row + 1;
      const nextC = direction === "across" ? col + 1 : col;
      if (nextR < rows && nextC < cols && !isCellBlack(grid[nextR][nextC])) {
        setSelectedCell([nextR, nextC]);
      }
    },
    [selectedCell, direction, userGrid, grid, rows, cols, completed, checkCompletion]
  );

  // Hint: reveal letter
  const revealLetter = useCallback(() => {
    if (!selectedCell) return;
    const [r, c] = selectedCell;
    const newGrid = userGrid.map((row) => [...row]);
    newGrid[r][c] = grid[r][c];
    setUserGrid(newGrid);
    setRevealedCells((prev) => [...prev, [r, c]]);
    if (checkCompletion(newGrid)) setCompleted(true);
  }, [selectedCell, userGrid, grid, checkCompletion]);

  // Hint: reveal word
  const revealWord = useCallback(() => {
    if (!activeClue) return;
    const newGrid = userGrid.map((row) => [...row]);
    const newRevealed = [...revealedCells];
    for (let i = 0; i < activeClue.length; i++) {
      const r = direction === "across" ? activeClue.row : activeClue.row + i;
      const c = direction === "across" ? activeClue.col + i : activeClue.col;
      newGrid[r][c] = grid[r][c];
      newRevealed.push([r, c]);
    }
    setUserGrid(newGrid);
    setRevealedCells(newRevealed);
    if (checkCompletion(newGrid)) setCompleted(true);
  }, [activeClue, direction, userGrid, grid, revealedCells, checkCompletion]);

  // Hint: check errors
  const checkErrors = useCallback(() => {
    const errors: [number, number][] = [];
    for (let r = 0; r < rows; r++) {
      for (let c = 0; c < cols; c++) {
        if (
          !isCellBlack(grid[r][c]) &&
          userGrid[r][c] !== "" &&
          userGrid[r][c] !== grid[r][c]
        ) {
          errors.push([r, c]);
        }
      }
    }
    setIncorrectCells(errors);
  }, [grid, userGrid, rows, cols]);

  // Auto-save progress
  useEffect(() => {
    const progress: PuzzleProgress = {
      userGrid,
      revealedCells,
      completed,
      completedAt: completed ? new Date().toISOString() : null,
      lastPlayed: new Date().toISOString(),
    };
    onSaveProgress(progress);
  }, [userGrid, revealedCells, completed]);

  return {
    userGrid,
    selectedCell,
    direction,
    activeClue,
    revealedCells,
    incorrectCells,
    completed,
    onCellClick,
    onKeyInput,
    revealLetter,
    revealWord,
    checkErrors,
  };
}
```

- [ ] **Step 2: Commit**

```bash
git add src/hooks/usePuzzle.ts
git commit -m "feat: implement usePuzzle hook with game logic and hints"
```

---

### Task 15: Puzzle Screen Page

**Files:**
- Create: `src/app/puzzle/[id]/page.tsx`

- [ ] **Step 1: Implement puzzle page**

Create `src/app/puzzle/[id]/page.tsx`:

```tsx
"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { TopBar } from "@/components/TopBar";
import { CrosswordGrid } from "@/components/CrosswordGrid";
import { CluePanel } from "@/components/CluePanel";
import { HintsSheet } from "@/components/HintsSheet";
import { CompletionModal } from "@/components/CompletionModal";
import { usePuzzle } from "@/hooks/usePuzzle";
import { useProgress } from "@/hooks/useProgress";
import { useTranslation } from "@/hooks/useTranslation";
import type { Puzzle, Clue } from "@/types/puzzle";

export default function PuzzlePage() {
  const { id } = useParams<{ id: string }>();
  const { state, setLanguage, getProgress, saveProgress } = useProgress();
  const { t, ls, language } = useTranslation(state.language);
  const [puzzle, setPuzzle] = useState<Puzzle | null>(null);
  const [hintsOpen, setHintsOpen] = useState(false);

  useEffect(() => {
    // Find the puzzle file from manifest
    fetch("/puzzles/manifest.json")
      .then((r) => r.json())
      .then((manifest) => {
        const entry = manifest.puzzles.find(
          (p: { id: string }) => p.id === id
        );
        if (entry) {
          return fetch(`/puzzles/${entry.file}`);
        }
        throw new Error("Puzzle not found");
      })
      .then((r) => r.json())
      .then(setPuzzle);
  }, [id]);

  if (!puzzle) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center">
        <div className="text-xl text-slate-400">...</div>
      </div>
    );
  }

  return (
    <PuzzlePageContent
      puzzle={puzzle}
      language={state.language}
      savedProgress={getProgress(puzzle.id)}
      onSaveProgress={(progress) => saveProgress(puzzle.id, progress)}
      onLanguageToggle={setLanguage}
      t={t}
      ls={ls}
      hintsOpen={hintsOpen}
      setHintsOpen={setHintsOpen}
    />
  );
}

function PuzzlePageContent({
  puzzle,
  language,
  savedProgress,
  onSaveProgress,
  onLanguageToggle,
  t,
  ls,
  hintsOpen,
  setHintsOpen,
}: {
  puzzle: Puzzle;
  language: "hu" | "he";
  savedProgress: ReturnType<ReturnType<typeof import("@/hooks/useProgress").useProgress>["getProgress"]>;
  onSaveProgress: (progress: import("@/types/puzzle").PuzzleProgress) => void;
  onLanguageToggle: (lang: "hu" | "he") => void;
  t: (key: string) => string;
  ls: (localized: import("@/types/puzzle").LocalizedString) => string;
  hintsOpen: boolean;
  setHintsOpen: (open: boolean) => void;
}) {
  const game = usePuzzle({
    puzzle,
    savedProgress: savedProgress ?? undefined,
    onSaveProgress,
  });

  const handleClueClick = (clue: Clue, direction: "across" | "down") => {
    game.onCellClick(clue.row, clue.col);
  };

  return (
    <div
      className="min-h-screen bg-slate-50 flex flex-col"
      dir={language === "he" ? "rtl" : "ltr"}
    >
      <TopBar
        title={ls(puzzle.title)}
        language={language}
        onLanguageToggle={onLanguageToggle}
        backHref="/"
        rightContent={
          <button
            onClick={() => setHintsOpen(true)}
            className="bg-[#2d5a8e] text-white px-3 py-1.5 rounded-lg text-sm font-medium
                       min-w-[44px] min-h-[44px] flex items-center justify-center"
          >
            💡 {t("hints.title")}
          </button>
        }
      />

      {/* Active clue bar (visible in both orientations) */}
      {game.activeClue && (
        <div className="bg-blue-100 px-4 py-2 text-sm font-semibold text-[#1e3a5f] border-b-2 border-blue-200">
          {game.activeClue.number} {game.direction === "across" ? t("puzzle.across").toLowerCase() : t("puzzle.down").toLowerCase()}:{" "}
          {game.activeClue.clue[language]}
        </div>
      )}

      {/* Main content: grid + clues */}
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden">
        {/* Grid */}
        <div className="flex-1 flex items-start justify-center p-4 md:items-center">
          <CrosswordGrid
            solutionGrid={puzzle.grid}
            userGrid={game.userGrid}
            selectedCell={game.selectedCell}
            direction={game.direction}
            activeClue={game.activeClue}
            revealedCells={game.revealedCells}
            incorrectCells={game.incorrectCells}
            onCellClick={game.onCellClick}
            onKeyInput={game.onKeyInput}
          />
        </div>

        {/* Clue panel */}
        <div className="md:w-[40%] md:max-w-[360px] border-t-2 md:border-t-0 md:border-l-2 border-slate-200 bg-white p-3 overflow-y-auto max-h-[40vh] md:max-h-none">
          <CluePanel
            acrossClues={puzzle.clues.across}
            downClues={puzzle.clues.down}
            activeClueNumber={game.activeClue?.number ?? null}
            activeDirection={game.direction}
            language={language}
            acrossLabel={t("puzzle.across")}
            downLabel={t("puzzle.down")}
            onClueClick={handleClueClick}
          />
        </div>
      </div>

      <HintsSheet
        isOpen={hintsOpen}
        onClose={() => setHintsOpen(false)}
        onRevealLetter={game.revealLetter}
        onRevealWord={game.revealWord}
        onCheck={game.checkErrors}
        labels={{
          title: t("hints.title"),
          revealLetter: t("hints.revealLetter"),
          revealWord: t("hints.revealWord"),
          check: t("hints.check"),
        }}
      />

      <CompletionModal
        isOpen={game.completed}
        title={t("puzzle.completed")}
        message={t("puzzle.completedMessage")}
        backLabel={t("puzzle.backToHome")}
        backHref="/"
      />
    </div>
  );
}
```

- [ ] **Step 2: Verify full puzzle flow**

Run: `npm run dev`
1. Navigate to home screen — daily puzzle card should appear
2. Click daily puzzle — puzzle screen loads with grid and clues
3. Tap a cell — cell highlights, keyboard appears
4. Type letters — letters fill cells
5. Tap hints — bottom sheet appears with 3 options
6. Test reveal letter and check
7. Switch language — UI and clues switch to Hebrew

- [ ] **Step 3: Commit**

```bash
git add src/app/puzzle/
git commit -m "feat: implement puzzle screen with grid, clues, and hints"
```

---

### Task 16: Tailwind Theme & Polish

**Files:**
- Modify: `tailwind.config.ts`
- Modify: `src/app/globals.css`

- [ ] **Step 1: Extend Tailwind config with theme colors**

Update `tailwind.config.ts` to add custom colors:

```ts
import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: "#1e3a5f",
        "navy-light": "#2d5a8e",
      },
    },
  },
  plugins: [],
};

export default config;
```

- [ ] **Step 2: Add global styles for accessibility**

Add to `src/app/globals.css` (after existing Tailwind imports):

```css
/* Prevent text selection on grid cells */
.grid button {
  -webkit-user-select: none;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}

/* Ensure focus is visible for accessibility */
button:focus-visible,
a:focus-visible {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
}

/* Smooth transitions */
* {
  -webkit-font-smoothing: antialiased;
}
```

- [ ] **Step 3: Verify static build**

Run: `npm run build`
Expected: Builds successfully to `out/` with all pages statically generated.

- [ ] **Step 4: Commit**

```bash
git add tailwind.config.ts src/app/globals.css
git commit -m "feat: add Tailwind theme colors and accessibility styles"
```

---

### Task 17: End-to-End Verification

**Files:** No new files — verification only.

- [ ] **Step 1: Run all tests**

Run: `npx jest --verbose`
Expected: All tests pass (storage, puzzleUtils, useTranslation).

- [ ] **Step 2: Run static build**

Run: `npm run build`
Expected: Builds to `out/` with no errors. Pages: `/`, `/browse`, `/puzzle/[id]`.

- [ ] **Step 3: Serve static build and test on iPad simulator or browser**

Run:
```bash
npx serve out
```

Open in browser (ideally iPad-sized viewport):
1. Home screen loads with daily puzzle
2. Navigate to browse — categories and filters work
3. Open a puzzle — grid renders, cells are tappable
4. Type letters — they appear in cells
5. Use hints — reveal and check work
6. Complete a puzzle — completion modal shows
7. Switch language to Hebrew — UI flips to RTL, clues in Hebrew
8. Reload page — progress is preserved from localStorage
9. Check PWA: manifest loads, service worker registers

- [ ] **Step 4: Commit any fixes**

If any issues found, fix and commit with descriptive message.

---

### Task 18: Generate More Puzzles

**Files:**
- Create: Additional puzzle JSON files in `public/puzzles/`
- Modify: `public/puzzles/manifest.json`

- [ ] **Step 1: Generate puzzles using Claude**

Use Claude to generate 10-20 additional puzzles across all categories and difficulties. Each puzzle must:
- Have a valid crossword grid (words intersect correctly)
- Include Hungarian clues with Hebrew translations
- Follow the JSON format defined in Task 6
- Use topics appropriate for elderly users

Categories to cover: nature, history, food, geography, culture, everyday.
Difficulties to cover: easy (5×5-6×6), medium (7×7-8×8), hard (9×9-10×10).

- [ ] **Step 2: Validate each puzzle**

For each generated puzzle, verify:
- All across/down words match the grid
- Clue positions and lengths are correct
- No orphan cells (every non-black cell is part of at least one word)
- Grid is symmetric (standard crossword convention — optional but nice)

- [ ] **Step 3: Update manifest**

Add all new puzzles to `public/puzzles/manifest.json`.

- [ ] **Step 4: Rebuild and verify**

Run: `npm run build && npx serve out`
Verify all new puzzles appear in browse and are playable.

- [ ] **Step 5: Commit**

```bash
git add public/puzzles/
git commit -m "feat: add additional puzzles across all categories"
```
