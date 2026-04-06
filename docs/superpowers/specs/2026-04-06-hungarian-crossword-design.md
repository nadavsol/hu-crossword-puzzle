# Hungarian Crossword Puzzle — iPad PWA

## Overview

A Progressive Web App for solving Hungarian-language crossword puzzles on iPad. Designed for elderly users (90+), optimized for offline use, with Hungarian and Hebrew UI language support.

## Tech Stack

- **Framework:** Next.js with static export (`output: 'export'`)
- **Styling:** Tailwind CSS
- **Offline:** PWA with Service Worker (via `serwist` — actively maintained `next-pwa` successor)
- **State:** localStorage for player progress and preferences
- **Hosting:** Static hosting (Vercel, Netlify, or GitHub Pages — free tier)
- **No backend required**

## Screens

Three screens total. Maximum 2 taps from home to playing.

### 1. Home Screen

- **Daily puzzle card** — prominent, one-tap start. Shows title, category, difficulty, grid size. Deterministic selection based on current date (index into puzzle manifest).
- **Resume in-progress puzzle** — shown only when the player has an unfinished puzzle. Displays title and completion percentage.
- **Browse all puzzles** button — navigates to the puzzle browser.
- **Language toggle** (HU / HE) in the top bar.
- **Settings gear** in the top bar (for future use — currently only language).

### 2. Puzzle Browser

- **Difficulty filter pills** at top: Mind (All), Könnyű (Easy), Közepes (Medium), Nehéz (Hard).
- **Categories** listed vertically, each with horizontally scrollable puzzle cards.
- Each card shows: title, grid size, difficulty, completion status (not started / percentage / completed checkmark).
- Tapping a card navigates to the puzzle screen.

### 3. Puzzle Screen

**Landscape (primary orientation):**
- Grid on the left (~60% width), clue list on the right (~40% width).
- Top bar: app title, hints button, settings.

**Portrait:**
- Grid on top, active clue highlight bar below the grid, full clue list at the bottom.
- Clues shown in two columns to save vertical space.

**Grid interaction:**
- Tap a cell to select it. Selected cell has blue background.
- The entire word (across or down) for the selected cell is lightly highlighted.
- Tap the same cell again to toggle between across/down direction.
- Native iPad on-screen keyboard appears for letter input.
- After typing a letter, cursor advances to the next cell in the current direction.
- Black cells are not selectable.
- Cell numbers displayed in top-left corner of numbered cells.

**Clue panel:**
- Split into "Vízszintes" (Across) and "Függőleges" (Down) sections.
- Active clue is highlighted with blue background.
- Tapping a clue selects the first cell of that word in the grid.

## Hints System

Accessed via a button in the top bar. Opens a bottom sheet with three options:

- **Betű felfedése** (Reveal letter) — fills the correct letter in the currently selected cell, visually marked so the player knows it was revealed.
- **Szó felfedése** (Reveal word) — reveals all letters of the current word.
- **Ellenőrzés** (Check) — highlights incorrect letters in red. Correct letters remain unchanged. The player can then fix the red cells.

No usage limits — the app is for enjoyment, not competition.

## Puzzle Data Format

Puzzles are pre-generated and bundled as static JSON files.

### File structure

```
public/puzzles/
  manifest.json          # Index of all puzzles
  nature/
    spring-flowers-easy-001.json
    forest-animals-easy-002.json
  history/
    hungarian-kings-medium-001.json
  food/
    hungarian-cuisine-easy-001.json
  ...
```

### Manifest (`manifest.json`)

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

### Puzzle file

```json
{
  "id": "nature-spring-flowers-easy-001",
  "title": { "hu": "Tavaszi virágok", "he": "פרחי אביב" },
  "category": "nature",
  "difficulty": "easy",
  "gridSize": { "rows": 5, "cols": 5 },
  "grid": [
    ["K", "E", "R", "T", "#"],
    ["Ö", "#", "Ó", "U", "L"],
    ["R", "Ó", "#", "L", "I"],
    ["T", "Z", "S", "I", "P"],
    ["#", "S", "A", "P", "#"]
  ],
  "clues": {
    "across": [
      {
        "number": 1,
        "clue": { "hu": "Virágoskert része", "he": "חלק מגינת פרחים" },
        "row": 0,
        "col": 0,
        "length": 4
      }
    ],
    "down": [
      {
        "number": 1,
        "clue": { "hu": "Évszak", "he": "עונה" },
        "row": 0,
        "col": 0,
        "length": 4
      }
    ]
  }
}
```

- `#` = black/blocked cell
- `grid` stores the solution (never sent to the client as-is in a real scenario, but since there's no server and the data is local, this is acceptable — the app simply doesn't display it until reveal/check)
- All user-facing strings have `hu` and `he` translations

### Puzzle categories and topics

Suitable for elderly users — no tech/computing topics:

| Category | Example topics |
|----------|---------------|
| Természet (Nature) | Flowers, trees, animals, seasons, rivers |
| Történelem (History) | Hungarian kings, historical events, famous figures |
| Ételek (Food) | Hungarian cuisine, spices, fruits, vegetables |
| Földrajz (Geography) | Hungarian cities, European capitals, rivers, mountains |
| Kultúra (Culture) | Literature, music, folk traditions, holidays |
| Hétköznapi élet (Everyday) | Household items, family, clothing, professions |

### Puzzle sizing by difficulty

| Difficulty | Grid size | Target audience |
|-----------|-----------|-----------------|
| Könnyű (Easy) | 5×5 to 6×6 | Quick, approachable |
| Közepes (Medium) | 7×7 to 8×8 | Moderate challenge |
| Nehéz (Hard) | 9×9 to 10×10 | Experienced solvers |

### Puzzle generation

Puzzles are generated during development using an LLM (Claude). The generation process:

1. Provide the LLM with a category, difficulty, and grid size.
2. LLM generates a valid crossword grid with Hungarian words and clues.
3. LLM also provides Hebrew translations for the title and all clues.
4. Output is validated (grid consistency, all words cross correctly, no orphan cells).
5. Validated puzzles are saved as JSON files.

Target: 100-200 puzzles across all categories and difficulties for the initial release. More can be added as app updates.

## Player State (localStorage)

```json
{
  "language": "hu",
  "puzzleProgress": {
    "nature-spring-flowers-easy-001": {
      "userGrid": [["K", "E", "", "T", "#"], ["", "#", "", "", ""], ...],
      "revealedCells": [[0, 2]],
      "completed": false,
      "completedAt": null,
      "lastPlayed": "2026-04-06T14:30:00Z"
    }
  },
  "completedPuzzles": ["nature-forest-animals-easy-002"],
  "dailyHistory": ["2026-04-05", "2026-04-04"]
}
```

- `userGrid` mirrors the puzzle grid dimensions, storing the player's entered letters (empty string for unfilled cells, `#` for black cells).
- `revealedCells` tracks which cells were revealed via hints (displayed with a subtle indicator).
- `completedPuzzles` is a list of puzzle IDs for quick lookup in the browser.
- `dailyHistory` tracks which daily puzzles were completed.

## Daily Puzzle Logic

The daily puzzle is selected deterministically:

```
dailyIndex = daysSinceEpoch(today) % totalPuzzleCount
dailyPuzzle = manifest.puzzles[dailyIndex]
```

This means each day maps to a specific puzzle. When the puzzle library grows, the cycle extends. No server or date API needed.

## Accessibility (Elderly-Focused)

- **Touch targets:** Minimum 44×44px for all interactive elements (Apple HIG).
- **Font sizes:** 18px+ for grid letters, 14px+ for clues, 16px+ for buttons.
- **Contrast:** WCAG AA minimum. Dark text on white/light backgrounds. Navy (#1e3a5f) for dark elements.
- **No gestures:** No pinch, swipe, or drag. Everything is tap-based.
- **Native keyboard:** Uses iPad's on-screen keyboard — familiar to users.
- **Clear feedback:** Selected cell has blue background, active word is highlighted, active clue is highlighted in the clue panel.
- **Error indication:** Incorrect letters shown in red during check — clear and unmistakable.
- **Simple navigation:** Back button always visible, maximum 2 taps to any screen.
- **No time pressure:** No timer, no scoring, no penalties.

## Internationalization (i18n)

### Translation files

```
src/locales/
  hu.json
  he.json
```

Example `hu.json`:
```json
{
  "app.title": "Keresztrejtvény",
  "home.dailyPuzzle": "Mai rejtvény",
  "home.startGame": "Játék indítása",
  "home.resume": "Félbehagyott rejtvény",
  "home.browseAll": "Összes rejtvény",
  "browse.all": "Mind",
  "browse.easy": "Könnyű",
  "browse.medium": "Közepes",
  "browse.hard": "Nehéz",
  "puzzle.across": "Vízszintes",
  "puzzle.down": "Függőleges",
  "hints.revealLetter": "Betű felfedése",
  "hints.revealWord": "Szó felfedése",
  "hints.check": "Ellenőrzés",
  "puzzle.completed": "Gratulálunk!",
  "puzzle.completedMessage": "Sikeresen megoldottad a rejtvényt!",
  "status.complete": "Kész",
  "status.inProgress": "Folyamatban"
}
```

### RTL support

- Hebrew mode sets `dir="rtl"` on the root element.
- UI text and clue panel flow right-to-left.
- The crossword grid does NOT flip — grid coordinates remain the same regardless of language.
- Tailwind's RTL utilities (`rtl:` prefix) handle layout adjustments.

## PWA Configuration

### Web App Manifest (`public/manifest.json`)

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

### Service Worker strategy

- **Precache** on install: all HTML pages, JS/CSS bundles, puzzle manifest, all puzzle JSON files, icons, fonts.
- **Cache-first** strategy for all assets — serve from cache, never hit network once installed.
- Puzzle JSONs are part of the precache since the full library is bundled.
- Cache versioning tied to build — new deployment triggers cache update on next online visit.

## Project Structure

```
hu-crossword-puzzle/
  public/
    manifest.json              # PWA manifest
    icons/                     # App icons (192, 512)
    puzzles/
      manifest.json            # Puzzle index
      nature/                  # Puzzle JSONs by category
      history/
      food/
      geography/
      culture/
      everyday/
  src/
    app/
      layout.tsx               # Root layout, i18n provider, PWA meta
      page.tsx                 # Home screen
      browse/
        page.tsx               # Puzzle browser
      puzzle/
        [id]/
          page.tsx             # Puzzle solving screen
    components/
      CrosswordGrid.tsx        # The interactive grid
      CluePanel.tsx            # Clue list with highlighting
      HintsSheet.tsx           # Bottom sheet with hint options
      DailyPuzzleCard.tsx      # Home screen daily puzzle card
      PuzzleCard.tsx           # Browse screen puzzle card
      DifficultyFilter.tsx     # Filter pills
      LanguageToggle.tsx       # HU/HE switcher
      TopBar.tsx               # App header
      CompletionModal.tsx      # Congratulations overlay
    hooks/
      usePuzzle.ts             # Load puzzle, manage grid state
      useProgress.ts           # localStorage read/write
      useTranslation.ts        # i18n hook
    locales/
      hu.json
      he.json
    lib/
      puzzleUtils.ts           # Grid validation, daily puzzle selection
      storage.ts               # localStorage wrapper
    types/
      puzzle.ts                # TypeScript types for puzzle data
  next.config.js               # Static export + PWA config
  tailwind.config.js
  package.json
```
