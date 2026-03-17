import type { PropsWithChildren, ReactNode } from "react";

interface CardProps {
  title: string;
  subtitle?: string;
  actions?: ReactNode;
  className?: string;
}

export function Card({
  title,
  subtitle,
  actions,
  className = "",
  children,
}: PropsWithChildren<CardProps>) {
  return (
    <section className={`rounded-3xl bg-white/95 p-5 shadow-panel ring-1 ring-slate-200 ${className}`}>
      <header className="mb-4 flex items-start justify-between gap-3">
        <div>
          <h2 className="text-base font-semibold text-ink-950">{title}</h2>
          {subtitle ? <p className="mt-1 text-sm text-slate-500">{subtitle}</p> : null}
        </div>
        {actions}
      </header>
      {children}
    </section>
  );
}
