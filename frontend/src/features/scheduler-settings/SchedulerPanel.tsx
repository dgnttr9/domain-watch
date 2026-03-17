import { useEffect, useState } from "react";

import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { EmptyState } from "../../components/ui/EmptyState";
import { Select } from "../../components/ui/Select";
import type { DomainRecord } from "../../types/domain";

type SchedulerPreset = "daily" | "weekly" | "monthly";

interface SchedulerPanelProps {
  domain: DomainRecord | null;
  onSave: (domainId: number, payload: { scheduler_enabled: boolean; scheduler_preset?: SchedulerPreset }) => Promise<void>;
  submitting: boolean;
}

export function SchedulerPanel({ domain, onSave, submitting }: SchedulerPanelProps) {
  const [enabled, setEnabled] = useState(false);
  const [preset, setPreset] = useState<SchedulerPreset>("daily");

  useEffect(() => {
    setEnabled(domain?.scheduler_enabled ?? false);
    setPreset((domain?.scheduler_preset as SchedulerPreset | null) ?? "daily");
  }, [domain]);

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!domain) return;

    await onSave(domain.id, {
      scheduler_enabled: enabled,
      scheduler_preset: enabled ? preset : undefined,
    });
  }

  return (
    <Card title="Scheduler settings" subtitle="Preset-based controls only for the first release.">
      {!domain ? (
        <EmptyState title="No domain selected" message="Select a domain from the table before changing scheduler settings." />
      ) : (
        <form className="grid gap-4" onSubmit={handleSubmit}>
          <label className="flex items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
            <input
              checked={enabled}
              className="h-4 w-4 rounded border-slate-300"
              onChange={(event) => setEnabled(event.target.checked)}
              type="checkbox"
            />
            Enable scheduler for {domain.domain}
          </label>
          <Select
            disabled={!enabled}
            label="Preset"
            value={preset}
            onChange={(event) => setPreset(event.target.value as SchedulerPreset)}
          >
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </Select>
          <Button disabled={submitting} type="submit">
            {submitting ? "Saving..." : "Save scheduler"}
          </Button>
        </form>
      )}
    </Card>
  );
}
