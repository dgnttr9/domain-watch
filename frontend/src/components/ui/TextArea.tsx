import type { TextareaHTMLAttributes } from "react";

interface TextAreaProps extends TextareaHTMLAttributes<HTMLTextAreaElement> {
  label: string;
}

export function TextArea({ label, className = "", ...props }: TextAreaProps) {
  return (
    <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
      <span>{label}</span>
      <textarea
        className={`min-h-32 rounded-2xl border border-slate-200 bg-white px-4 py-3 text-sm text-ink-950 outline-none transition focus:border-slate-400 focus:ring-2 focus:ring-slate-200 ${className}`}
        {...props}
      />
    </label>
  );
}
