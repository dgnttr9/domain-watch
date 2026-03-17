import type { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
}

export function Input({ label, className = "", ...props }: InputProps) {
  return (
    <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
      <span>{label}</span>
      <input
        className={`rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-ink-950 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 ${className}`}
        {...props}
      />
    </label>
  );
}
