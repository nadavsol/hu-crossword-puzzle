"use client";

interface TopBarProps {
  title: string;
  backHref?: string;
  rightContent?: React.ReactNode;
}

export function TopBar({
  title,
  backHref,
  rightContent,
}: TopBarProps) {
  return (
    <header className="bg-[#1e3a5f] text-white px-4 py-3 flex items-center justify-between">
      <div className="flex items-center gap-3">
        {backHref && (
          <a
            href={backHref}
            className="text-xl min-w-[44px] min-h-[44px] flex items-center justify-center"
            aria-label="Back"
          >
            ←
          </a>
        )}
        <h1 className="text-lg font-bold">{title}</h1>
      </div>
      <div className="flex items-center gap-3">
        {rightContent}
      </div>
    </header>
  );
}
