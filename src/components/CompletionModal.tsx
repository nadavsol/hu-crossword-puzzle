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
