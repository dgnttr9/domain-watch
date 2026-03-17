import { EmptyState } from "../../components/ui/EmptyState";
import { StatusBadge } from "../../components/ui/StatusBadge";
import { formatDate, formatRelativeDays } from "../../lib/format";
import type { DomainRecord } from "../../types/domain";

interface DomainResultsTableProps {
  domains: DomainRecord[];
  selectedDomainId: number | null;
  onSelectDomain: (domainId: number) => void;
  onRecheckDomain: (domainId: number) => Promise<void>;
  recheckingDomainId: number | null;
}

export function DomainResultsTable({
  domains,
  selectedDomainId,
  onSelectDomain,
  onRecheckDomain,
  recheckingDomainId,
}: DomainResultsTableProps) {
  if (domains.length === 0) {
    return (
      <EmptyState
        title="No domains yet"
        message="Add a single domain or run a bulk action to populate the result table."
      />
    );
  }

  return (
    <div className="overflow-hidden rounded-2xl border border-slate-200">
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-slate-200 text-left text-sm">
          <thead className="bg-slate-50 text-slate-500">
            <tr>
              <th className="px-4 py-3 font-medium">Domain</th>
              <th className="px-4 py-3 font-medium">Status</th>
              <th className="px-4 py-3 font-medium">Expiration date</th>
              <th className="px-4 py-3 font-medium">Days left</th>
              <th className="px-4 py-3 font-medium">Last checked</th>
              <th className="px-4 py-3 font-medium">Next check</th>
              <th className="px-4 py-3 font-medium">Provider</th>
              <th className="px-4 py-3 font-medium">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100 bg-white">
            {domains.map((domain) => (
              <tr
                key={domain.id}
                className={`cursor-pointer transition hover:bg-slate-50 ${
                  selectedDomainId === domain.id ? "bg-sky-100/90 ring-1 ring-inset ring-sky-200" : ""
                }`}
                onClick={() => onSelectDomain(domain.id)}
              >
                <td className="px-4 py-3 font-medium text-ink-950">{domain.domain}</td>
                <td className="px-4 py-3">
                  <StatusBadge status={domain.status} />
                </td>
                <td className="px-4 py-3 text-slate-600">{formatDate(domain.expiration_date)}</td>
                <td className="px-4 py-3 text-slate-600">{formatRelativeDays(domain.days_left)}</td>
                <td className="px-4 py-3 text-slate-600">{formatDate(domain.last_checked_at)}</td>
                <td className="px-4 py-3 text-slate-600">{formatDate(domain.next_check_at)}</td>
                <td className="px-4 py-3 text-slate-600">{domain.provider_used ?? "Not set"}</td>
                <td className="px-4 py-3">
                  <button
                    className="rounded-lg bg-slate-100 px-3 py-2 text-xs font-medium text-ink-950 transition hover:bg-slate-200 disabled:cursor-not-allowed disabled:opacity-60"
                    disabled={recheckingDomainId === domain.id}
                    onClick={(event) => {
                      event.stopPropagation();
                      void onRecheckDomain(domain.id);
                    }}
                    type="button"
                  >
                    {recheckingDomainId === domain.id ? "Rechecking..." : "Recheck"}
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
