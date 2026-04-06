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
      <div
        className="fixed inset-0 bg-black/30 z-40"
        onClick={onClose}
      />
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
