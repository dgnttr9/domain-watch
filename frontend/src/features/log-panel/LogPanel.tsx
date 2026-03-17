import { Card } from "../../components/ui/Card";
import { EmptyState } from "../../components/ui/EmptyState";
import { Input } from "../../components/ui/Input";
import { Select } from "../../components/ui/Select";
import { formatDate } from "../../lib/format";
import type { LogRecord } from "../../types/log";

interface LogPanelProps {
  logs: LogRecord[];
  levelFilter: string;
  createdFrom: string;
  createdTo: string;
  onLevelFilterChange: (value: string) => void;
  onCreatedFromChange: (value: string) => void;
  onCreatedToChange: (value: string) => void;
  onClearFilters: () => void;
}

export function LogPanel({
  logs,
  levelFilter,
  createdFrom,
  createdTo,
  onLevelFilterChange,
  onCreatedFromChange,
  onCreatedToChange,
  onClearFilters,
}: LogPanelProps) {
  return (
    <Card
      title="Log output"
      subtitle="Filter log severity and inspect provider attempt traces."
      actions={
        <div className="text-xs text-slate-500">
          Filters update the backend query directly.
        </div>
      }
    >
      <div className="mb-4 grid gap-3 md:grid-cols-[1fr_1fr_1fr_auto]">
        <Select label="Level" value={levelFilter} onChange={(event) => onLevelFilterChange(event.target.value)}>
          <option value="">All</option>
          <option value="INFO">Info</option>
          <option value="WARNING">Warning</option>
          <option value="ERROR">Error</option>
        </Select>
        <Input
          label="Created from"
          type="datetime-local"
          value={createdFrom}
          onChange={(event) => onCreatedFromChange(event.target.value)}
        />
        <Input
          label="Created to"
          type="datetime-local"
          value={createdTo}
          onChange={(event) => onCreatedToChange(event.target.value)}
        />
        <button
          className="mt-7 rounded-xl bg-slate-100 px-4 py-3 text-sm font-medium text-ink-950 transition hover:bg-slate-200"
          onClick={onClearFilters}
          type="button"
        >
          Clear
        </button>
      </div>
      {logs.length === 0 ? (
        <EmptyState title="No logs available" message="Run a domain action to populate operational logs." />
      ) : (
        <div className="space-y-3">
          {logs.map((log) => (
            <article key={log.id} className="rounded-2xl border border-slate-200 bg-slate-50 px-4 py-3">
              <div className="flex flex-wrap items-center justify-between gap-2">
                <div className="text-sm font-semibold text-ink-950">{log.message}</div>
                <div className="text-xs uppercase tracking-wide text-slate-500">{log.level}</div>
              </div>
              <div className="mt-2 text-xs text-slate-500">{formatDate(log.created_at)}</div>
              {log.metadata_json?.provider_attempts?.length ? (
                <ul className="mt-3 space-y-2 text-xs text-slate-600">
                  {log.metadata_json.provider_attempts.map((attempt, index) => (
                    <li key={`${log.id}-${attempt.provider}-${index}`} className="rounded-xl bg-white px-3 py-2">
                      {attempt.provider}: {attempt.status}
                      {attempt.error_code ? ` (${attempt.error_code})` : ""}
                    </li>
                  ))}
                </ul>
              ) : null}
            </article>
          ))}
        </div>
      )}
    </Card>
  );
}
