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
