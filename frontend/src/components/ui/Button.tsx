import type { ButtonHTMLAttributes, PropsWithChildren } from "react";

type ButtonVariant = "primary" | "secondary" | "ghost";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: ButtonVariant;
  fullWidth?: boolean;
}

const variantClasses: Record<ButtonVariant, string> = {
  primary: "bg-ink-950 text-white hover:bg-ink-900",
  secondary: "bg-white text-ink-950 ring-1 ring-slate-200 hover:bg-slate-50",
  ghost: "bg-transparent text-slate-600 hover:bg-slate-100",
};

export function Button({
  children,
  variant = "primary",
  fullWidth = false,
  className = "",
  ...props
}: PropsWithChildren<ButtonProps>) {
  return (
    <button
      className={[
        "inline-flex items-center justify-center rounded-xl px-4 py-2.5 text-sm font-medium transition",
        "disabled:cursor-not-allowed disabled:opacity-60",
        variantClasses[variant],
        fullWidth ? "w-full" : "",
        className,
      ].join(" ")}
      {...props}
    >
      {children}
    </button>
  );
}
