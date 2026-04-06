"use client";

import { useState, useCallback, useEffect } from "react";
import type { Puzzle, Clue, PuzzleProgress } from "@/types/puzzle";
import { isCellBlack } from "@/lib/puzzleUtils";

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
