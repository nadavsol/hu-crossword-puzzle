"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { TopBar } from "@/components/TopBar";
import { CrosswordGrid } from "@/components/CrosswordGrid";
import { CluePanel } from "@/components/CluePanel";
import { HintsSheet } from "@/components/HintsSheet";
import { CompletionModal } from "@/components/CompletionModal";
import { usePuzzle } from "@/hooks/usePuzzle";
import { useProgress } from "@/hooks/useProgress";
import { useTranslation } from "@/hooks/useTranslation";
import type { Puzzle, Clue, PuzzleProgress, LocalizedString } from "@/types/puzzle";

function PuzzlePageInner() {
  const searchParams = useSearchParams();
  const id = searchParams.get("id") ?? "";
  const { state, setLanguage, getProgress, saveProgress } = useProgress();
  const { t, ls, language } = useTranslation(state.language);
  const [puzzle, setPuzzle] = useState<Puzzle | null>(null);
  const [hintsOpen, setHintsOpen] = useState(false);

  useEffect(() => {
    if (!id) return;
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
      onSaveProgress={(progress: PuzzleProgress) => saveProgress(puzzle.id, progress)}
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
  savedProgress: PuzzleProgress | undefined;
  onSaveProgress: (progress: PuzzleProgress) => void;
  onLanguageToggle: (lang: "hu" | "he") => void;
  t: (key: string) => string;
  ls: (localized: LocalizedString) => string;
  hintsOpen: boolean;
  setHintsOpen: (open: boolean) => void;
}) {
  const game = usePuzzle({
    puzzle,
    savedProgress: savedProgress ?? undefined,
    onSaveProgress,
  });

  const handleClueClick = (clue: Clue, _direction: "across" | "down") => {
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

      {/* Active clue bar */}
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

export default function PuzzlePage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen bg-slate-50 flex items-center justify-center">
          <div className="text-xl text-slate-400">...</div>
        </div>
      }
    >
      <PuzzlePageInner />
    </Suspense>
  );
}
