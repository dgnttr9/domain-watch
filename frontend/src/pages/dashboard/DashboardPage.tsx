import { useEffect, useMemo, useState } from "react";

import { AppShell } from "../../components/layout/AppShell";
import { Header } from "../../components/layout/Header";
import { Card } from "../../components/ui/Card";
import { EmptyState } from "../../components/ui/EmptyState";
import { LoadingState } from "../../components/ui/LoadingState";
import { BulkDomainPanel } from "../../features/bulk-import/BulkDomainPanel";
import { DomainResultsTable } from "../../features/domain-table/DomainResultsTable";
import { SingleDomainForm } from "../../features/domain-form/SingleDomainForm";
import { ErrorDetailPanel } from "../../features/error-panel/ErrorDetailPanel";
import { ExportActions } from "../../features/exports/ExportActions";
import { LogPanel } from "../../features/log-panel/LogPanel";
import { SchedulerPanel } from "../../features/scheduler-settings/SchedulerPanel";
import { apiClient } from "../../services/apiClient";
import type { ImportJob } from "../../types/import";
import type { DomainRecord, SchedulerUpdatePayload } from "../../types/domain";
import type { LogRecord } from "../../types/log";

interface FeedbackState {
  tone: "info" | "success" | "error";
  message: string;
}

export function DashboardPage() {
  const [domains, setDomains] = useState<DomainRecord[]>([]);
  const [logs, setLogs] = useState<LogRecord[]>([]);
  const [selectedDomainId, setSelectedDomainId] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [logLevelFilter, setLogLevelFilter] = useState("");
  const [createdFrom, setCreatedFrom] = useState("");
  const [createdTo, setCreatedTo] = useState("");
  const [feedback, setFeedback] = useState<FeedbackState | null>(null);
  const [lastImportJob, setLastImportJob] = useState<ImportJob | null>(null);
  const [recheckingDomainId, setRecheckingDomainId] = useState<number | null>(null);

  const selectedDomain = useMemo(
    () => domains.find((domain) => domain.id === selectedDomainId) ?? null,
    [domains, selectedDomainId],
  );

  async function loadDashboard() {
    setLoading(true);
    setError(null);
    try {
      const [domainData, logData] = await Promise.all([
        apiClient.getDomains(),
        apiClient.getLogs({
          level: logLevelFilter || undefined,
          createdFrom: createdFrom ? new Date(createdFrom).toISOString() : undefined,
          createdTo: createdTo ? new Date(createdTo).toISOString() : undefined,
        }),
      ]);
      setDomains(domainData);
      setLogs(logData);
      if (!selectedDomainId && domainData[0]) {
        setSelectedDomainId(domainData[0].id);
      }
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Failed to load dashboard.");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void loadDashboard();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [logLevelFilter, createdFrom, createdTo]);

  async function runAction(action: () => Promise<void>, successMessage?: string) {
    setSubmitting(true);
    setError(null);
    try {
      await action();
      if (successMessage) {
        setFeedback({ tone: "success", message: successMessage });
      }
      await loadDashboard();
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Action failed.");
      setFeedback(null);
    } finally {
      setSubmitting(false);
    }
  }

  async function handleRecheckDomain(domainId: number) {
    setRecheckingDomainId(domainId);
    setError(null);
    try {
      const updated = await apiClient.recheckDomain(domainId);
      setFeedback({ tone: "success", message: `${updated.domain} was rechecked successfully.` });
      await loadDashboard();
    } catch (requestError) {
      setError(requestError instanceof Error ? requestError.message : "Recheck failed.");
    } finally {
      setRecheckingDomainId(null);
    }
  }

  function handleExport(format: "csv" | "json") {
    window.open(apiClient.getExportUrl(format), "_blank", "noopener,noreferrer");
    setFeedback({
      tone: "info",
      message: `${format.toUpperCase()} export download started.`,
    });
  }

  function clearLogFilters() {
    setLogLevelFilter("");
    setCreatedFrom("");
    setCreatedTo("");
  }

  return (
    <AppShell>
      <Header />

      {loading ? <LoadingState /> : null}
      {error ? (
        <div className="mb-6 rounded-2xl border border-red-300 bg-red-50 px-4 py-3 text-sm font-medium text-red-700 shadow-sm">
          {error}
        </div>
      ) : null}
      {feedback ? (
        <div
          className={`mb-6 rounded-2xl px-4 py-3 text-sm font-medium shadow-sm ${
            feedback.tone === "success"
              ? "border border-emerald-200 bg-emerald-50 text-emerald-700"
              : feedback.tone === "error"
                ? "border border-red-300 bg-red-50 text-red-700"
                : "border border-sky-200 bg-sky-50 text-sky-700"
          }`}
        >
          {feedback.message}
        </div>
      ) : null}

      <div className="grid gap-6 xl:grid-cols-[1.15fr_0.85fr]">
        <div className="grid gap-6">
          <div className="grid gap-6 lg:grid-cols-2">
            <SingleDomainForm
              onSubmit={(payload) => runAction(async () => {
                await apiClient.createDomain(payload);
              }, "Domain created successfully.")}
              submitting={submitting}
            />
            <BulkDomainPanel
              onCheckDomains={(domainList) => runAction(async () => {
                const checked = await apiClient.checkDomains({ domains: domainList });
                setFeedback({
                  tone: "success",
                  message: `${checked.length} domain(s) checked successfully.`,
                });
              })}
              onImportText={(content) => runAction(async () => {
                const result = await apiClient.importText(content);
                setLastImportJob(result);
                setFeedback({
                  tone: "success",
                  message: `Text import completed. Valid rows: ${result.valid_rows}, invalid rows: ${result.invalid_rows}.`,
                });
              })}
              onImportFile={(file) => runAction(async () => {
                const result = await apiClient.importFile(file);
                setLastImportJob(result);
                setFeedback({
                  tone: "success",
                  message: `File import completed. Valid rows: ${result.valid_rows}, invalid rows: ${result.invalid_rows}.`,
                });
              })}
              submitting={submitting}
            />
          </div>

          {lastImportJob ? (
            <Card
              title="Last import summary"
              subtitle="The latest text or file import result."
            >
              <div className="grid gap-3 sm:grid-cols-4">
                <div className="rounded-2xl bg-slate-50 px-4 py-3">
                  <div className="text-xs uppercase tracking-wide text-slate-500">Source</div>
                  <div className="mt-1 text-sm font-semibold text-ink-950">{lastImportJob.source_type.toUpperCase()}</div>
                </div>
                <div className="rounded-2xl bg-slate-50 px-4 py-3">
                  <div className="text-xs uppercase tracking-wide text-slate-500">Valid rows</div>
                  <div className="mt-1 text-sm font-semibold text-ink-950">{lastImportJob.valid_rows}</div>
                </div>
                <div className="rounded-2xl bg-slate-50 px-4 py-3">
                  <div className="text-xs uppercase tracking-wide text-slate-500">Invalid rows</div>
                  <div className="mt-1 text-sm font-semibold text-ink-950">{lastImportJob.invalid_rows}</div>
                </div>
                <div className="rounded-2xl bg-slate-50 px-4 py-3">
                  <div className="text-xs uppercase tracking-wide text-slate-500">Status</div>
                  <div className="mt-1 text-sm font-semibold text-ink-950">{lastImportJob.status}</div>
                </div>
              </div>
            </Card>
          ) : null}

          <Card title="Results" subtitle="Domain list, provider status, scheduling and last check metadata.">
            {!loading && domains.length === 0 ? (
              <EmptyState title="No domains loaded" message="Use the forms above to add domains and populate the table." />
            ) : (
              <DomainResultsTable
                domains={domains}
                selectedDomainId={selectedDomainId}
                onSelectDomain={setSelectedDomainId}
                onRecheckDomain={handleRecheckDomain}
                recheckingDomainId={recheckingDomainId}
              />
            )}
          </Card>

          <ExportActions
            onExport={handleExport}
            onDispatchScheduler={() => runAction(async () => {
              const processed = await apiClient.dispatchScheduler();
              setFeedback({
                tone: "success",
                message: `Scheduler dispatch completed. ${processed.length} domain(s) processed.`,
              });
            })}
            submitting={submitting}
          />
        </div>

        <div className="grid gap-6">
          <ErrorDetailPanel domain={selectedDomain} />
          <SchedulerPanel
            domain={selectedDomain}
            onSave={(domainId, payload: SchedulerUpdatePayload) => runAction(async () => {
              await apiClient.updateScheduler(domainId, payload);
            }, "Scheduler settings saved.")}
            submitting={submitting}
          />
          <LogPanel
            logs={logs}
            levelFilter={logLevelFilter}
            createdFrom={createdFrom}
            createdTo={createdTo}
            onLevelFilterChange={setLogLevelFilter}
            onCreatedFromChange={setCreatedFrom}
            onCreatedToChange={setCreatedTo}
            onClearFilters={clearLogFilters}
          />
        </div>
      </div>
    </AppShell>
  );
}
