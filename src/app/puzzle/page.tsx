"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { TopBar } from "@/components/TopBar";
import { CrosswordGrid } from "@/components/CrosswordGrid";
import { CluePanel } from "@/components/CluePanel";
import { HintsSheet } from "@/components/HintsSheet";
import { CompletionModal } from "@/components/CompletionModal";
import { HungarianKeyboard } from "@/components/HungarianKeyboard";
import { usePuzzle } from "@/hooks/usePuzzle";
import { useProgress } from "@/hooks/useProgress";
import { useTranslation } from "@/hooks/useTranslation";
import type { Puzzle, Clue, PuzzleProgress, LocalizedString } from "@/types/puzzle";

function PuzzlePageInner() {
  const searchParams = useSearchParams();
  const id = searchParams.get("id") ?? "";
  const { getProgress, saveProgress } = useProgress();
  const { t, ls } = useTranslation();
  const [puzzle, setPuzzle] = useState<Puzzle | null>(null);
  const [hintsOpen, setHintsOpen] = useState(false);
  const [error, setError] = useState(false);

  useEffect(() => {
    if (!id) return;
    fetch("/puzzles/manifest.json")
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load manifest");
        return r.json();
      })
      .then((manifest) => {
        const entry = manifest.puzzles.find(
          (p: { id: string }) => p.id === id
        );
        if (!entry) throw new Error("Puzzle not found");
        return fetch(`/puzzles/${entry.file}`);
      })
      .then((r) => {
        if (!r.ok) throw new Error("Failed to load puzzle");
        return r.json();
      })
      .then(setPuzzle)
      .catch(() => setError(true));
  }, [id]);

  if (error) {
    return (
      <div className="min-h-screen bg-slate-50 flex items-center justify-center p-8">
        <div className="text-center">
          <p className="text-lg text-slate-600 mb-4">Nem sikerült betölteni a rejtvényt.</p>
          <div className="flex gap-3 justify-center">
            <button onClick={() => window.location.reload()} className="bg-[#1e3a5f] text-white px-6 py-3 rounded-xl font-bold text-base">
              Újrapróbálás
            </button>
            <a href="/" className="bg-slate-200 text-slate-700 px-6 py-3 rounded-xl font-bold text-base">
              Főoldal
            </a>
          </div>
        </div>
      </div>
    );
  }

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
      savedProgress={getProgress(puzzle.id)}
      onSaveProgress={(progress: PuzzleProgress) => saveProgress(puzzle.id, progress)}
      t={t}
      ls={ls}
      hintsOpen={hintsOpen}
      setHintsOpen={setHintsOpen}
    />
  );
}

function PuzzlePageContent({
  puzzle,
  savedProgress,
  onSaveProgress,
  t,
  ls,
  hintsOpen,
  setHintsOpen,
}: {
  puzzle: Puzzle;
  savedProgress: PuzzleProgress | undefined;
  onSaveProgress: (progress: PuzzleProgress) => void;
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
    <div className="bg-slate-50 flex flex-col overflow-hidden" style={{ height: "100dvh" }}>
      <TopBar
        title={ls(puzzle.title)}
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

      {/* Tip banner */}
      <div className="bg-amber-50 px-4 py-1.5 text-sm text-amber-800 border-b border-amber-200 shrink-0 text-center font-medium">
        💡 Koppintson kétszer egy cellára a vízszintes ↔ függőleges váltáshoz
      </div>

      {/* Active clue bar */}
      {game.activeClue && (
        <div className="bg-blue-100 px-4 py-2 text-sm font-semibold text-[#1e3a5f] border-b-2 border-blue-200 shrink-0">
          {game.activeClue.number} {game.direction === "across" ? t("puzzle.across").toLowerCase() : t("puzzle.down").toLowerCase()}:{" "}
          {game.activeClue.clue.hu}
        </div>
      )}

      {/* Main content: grid + clues — scrollable middle section */}
      <div className="flex-1 flex flex-col md:flex-row overflow-hidden min-h-0">
        {/* Grid */}
        <div className="flex-1 flex items-start justify-center p-2 md:p-3 md:items-center overflow-auto min-h-0">
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

        {/* Clue panel — hidden on small portrait, visible on landscape/desktop */}
        <div className="hidden md:block md:w-[38%] md:max-w-[340px] border-l-2 border-slate-200 bg-white p-3 overflow-y-auto">
          <CluePanel
            acrossClues={puzzle.clues.across}
            downClues={puzzle.clues.down}
            activeClueNumber={game.activeClue?.number ?? null}
            activeDirection={game.direction}
            language="hu"
            acrossLabel={t("puzzle.across")}
            downLabel={t("puzzle.down")}
            onClueClick={handleClueClick}
          />
        </div>
      </div>

      {/* Hungarian keyboard — always visible at bottom */}
      <div className="shrink-0">
        <HungarianKeyboard onKeyPress={game.onKeyInput} />
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
