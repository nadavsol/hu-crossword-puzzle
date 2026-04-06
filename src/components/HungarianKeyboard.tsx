"use client";

interface HungarianKeyboardProps {
  onKeyPress: (key: string) => void;
}

export function HungarianKeyboard({ onKeyPress }: HungarianKeyboardProps) {
  const rows = [
    ["Q", "W", "E", "R", "T", "Z", "U", "I", "O", "P", "Ö", "Ü", "Ó"],
    ["A", "S", "D", "F", "G", "H", "J", "K", "L", "É", "Á", "Ű"],
    ["Í", "Y", "X", "C", "V", "B", "N", "M", "⌫"],
  ];

  return (
    <div
      className="bg-slate-200 border-t-2 border-slate-300 select-none"
      style={{ padding: "4px 4px env(safe-area-inset-bottom, 6px)" }}
    >
      {rows.map((row, i) => (
        <div key={i} className="flex justify-center gap-[3px] mb-[3px]">
          {row.map((key) => {
            const isBackspace = key === "⌫";
            return (
              <button
                key={key}
                onPointerDown={(e) => {
                  e.preventDefault(); // prevent focus steal / native keyboard
                  onKeyPress(isBackspace ? "BACKSPACE" : key);
                }}
                className={[
                  "rounded-lg font-bold shadow-md",
                  "flex items-center justify-center",
                  "active:scale-95 transition-transform duration-75",
                  "touch-manipulation",
                  isBackspace
                    ? "bg-slate-500 text-white"
                    : "bg-white text-[#1e3a5f]",
                ].join(" ")}
                style={
                  isBackspace
                    ? {
                        fontSize: "18px",
                        minWidth: "56px",
                        height: "44px",
                        paddingLeft: "8px",
                        paddingRight: "8px",
                      }
                    : {
                        fontSize: "16px",
                        minWidth: "28px",
                        flex: "1 1 0",
                        maxWidth: "48px",
                        height: "44px",
                      }
                }
                aria-label={isBackspace ? "Törlés" : key}
              >
                {key}
              </button>
            );
          })}
        </div>
      ))}
    </div>
  );
}
