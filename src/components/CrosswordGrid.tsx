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
