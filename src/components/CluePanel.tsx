"use client";

import { useRef, useState, useEffect, useCallback } from "react";
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
  const scrollRef = useRef<HTMLDivElement>(null);
  const [canScrollUp, setCanScrollUp] = useState(false);
  const [canScrollDown, setCanScrollDown] = useState(false);

  const checkScroll = useCallback(() => {
    const el = scrollRef.current;
    if (!el) return;
    setCanScrollUp(el.scrollTop > 4);
    setCanScrollDown(el.scrollTop + el.clientHeight < el.scrollHeight - 4);
  }, []);

  useEffect(() => {
    checkScroll();
    const el = scrollRef.current;
    if (!el) return;
    el.addEventListener("scroll", checkScroll, { passive: true });
    const observer = new ResizeObserver(checkScroll);
    observer.observe(el);
    return () => {
      el.removeEventListener("scroll", checkScroll);
      observer.disconnect();
    };
  }, [checkScroll]);

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
    <div className="relative h-full">
      {/* Scroll up indicator */}
      {canScrollUp && (
        <div className="absolute top-0 left-0 right-0 z-10 flex justify-center pointer-events-none">
          <div className="bg-gradient-to-b from-white to-transparent h-8 w-full absolute top-0" />
          <div className="text-slate-400 text-lg mt-1 animate-bounce relative">▲</div>
        </div>
      )}

      <div ref={scrollRef} className="overflow-y-auto h-full">
        <h3 className="font-bold text-[#1e3a5f] text-sm border-b-2 border-blue-100 pb-1 mb-2 px-2">
          {acrossLabel} ➡️
        </h3>
        <div className="space-y-0.5 mb-4">
          {acrossClues.map((c) => renderClue(c, "across"))}
        </div>

        <h3 className="font-bold text-[#1e3a5f] text-sm border-b-2 border-blue-100 pb-1 mb-2 px-2">
          {downLabel} ⬇️
        </h3>
        <div className="space-y-0.5 pb-2">
          {downClues.map((c) => renderClue(c, "down"))}
        </div>
      </div>

      {/* Scroll down indicator */}
      {canScrollDown && (
        <div className="absolute bottom-0 left-0 right-0 z-10 flex justify-center pointer-events-none">
          <div className="bg-gradient-to-t from-white to-transparent h-8 w-full absolute bottom-0" />
          <div className="text-slate-400 text-lg mb-1 animate-bounce relative">▼</div>
        </div>
      )}
    </div>
  );
}
