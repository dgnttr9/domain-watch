import { Card } from "../../components/ui/Card";

interface ExportActionsProps {
  onExport: (format: "csv" | "json") => void;
  onDispatchScheduler: () => Promise<void>;
  submitting: boolean;
}

export function ExportActions({
  onExport,
  onDispatchScheduler,
  submitting,
}: ExportActionsProps) {
  return (
    <Card title="Exports and dispatch" subtitle="Download data snapshots or run preset scheduler dispatch.">
      <div className="grid gap-3 sm:grid-cols-3">
        <button
          className="rounded-xl bg-ink-950 px-4 py-3 text-center text-sm font-medium text-white transition hover:bg-ink-900"
          onClick={() => onExport("csv")}
          type="button"
        >
          Download CSV
        </button>
        <button
          className="rounded-xl bg-white px-4 py-3 text-center text-sm font-medium text-ink-950 ring-1 ring-slate-200 transition hover:bg-slate-50"
          onClick={() => onExport("json")}
          type="button"
        >
          Download JSON
        </button>
        <button
          className="rounded-xl bg-slate-100 px-4 py-3 text-sm font-medium text-ink-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
          disabled={submitting}
          onClick={() => void onDispatchScheduler()}
          type="button"
        >
          {submitting ? "Dispatching..." : "Run dispatch"}
        </button>
      </div>
    </Card>
  );
}
