interface StatusBadgeProps {
  status: string;
}

const classes: Record<string, string> = {
  active: "bg-emerald-50 text-emerald-700 ring-emerald-200",
  available: "bg-amber-50 text-amber-700 ring-amber-200",
  error: "bg-red-50 text-red-700 ring-red-200",
  unknown: "bg-slate-100 text-slate-700 ring-slate-200",
  pending: "bg-sky-50 text-sky-700 ring-sky-200",
};

export function StatusBadge({ status }: StatusBadgeProps) {
  return (
    <span
      className={`inline-flex rounded-full px-2.5 py-1 text-xs font-semibold capitalize ring-1 ${
        classes[status] ?? classes.unknown
      }`}
    >
      {status}
    </span>
  );
}
