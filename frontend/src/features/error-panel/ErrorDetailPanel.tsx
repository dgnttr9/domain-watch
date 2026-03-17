import { Card } from "../../components/ui/Card";
import { EmptyState } from "../../components/ui/EmptyState";
import { formatDate, formatRelativeDays } from "../../lib/format";
import type { DomainRecord } from "../../types/domain";

interface ErrorDetailPanelProps {
  domain: DomainRecord | null;
}

export function ErrorDetailPanel({ domain }: ErrorDetailPanelProps) {
  return (
    <Card title="Error detail" subtitle="Review the selected domain, its current dates, and the latest error message.">
      {!domain ? (
        <EmptyState title="No domain selected" message="Choose a row from the results table to inspect details." />
      ) : (
        <dl className="grid gap-3 text-sm">
          <div className="rounded-2xl bg-slate-50 px-4 py-3">
            <dt className="text-slate-500">Domain</dt>
            <dd className="mt-1 font-medium text-ink-950">{domain.domain}</dd>
          </div>
          <div className="grid gap-3 sm:grid-cols-2">
            <div className="rounded-2xl bg-slate-50 px-4 py-3">
              <dt className="text-slate-500">Expiration date</dt>
              <dd className="mt-1 text-ink-950">{formatDate(domain.expiration_date)}</dd>
            </div>
            <div className="rounded-2xl bg-slate-50 px-4 py-3">
              <dt className="text-slate-500">Days left</dt>
              <dd className="mt-1 text-ink-950">{formatRelativeDays(domain.days_left)}</dd>
            </div>
          </div>
          <div className="rounded-2xl bg-slate-50 px-4 py-3">
            <dt className="text-slate-500">Error message</dt>
            <dd className="mt-1 text-ink-950">{domain.last_error_message ?? "No provider error recorded."}</dd>
          </div>
        </dl>
      )}
    </Card>
  );
}
