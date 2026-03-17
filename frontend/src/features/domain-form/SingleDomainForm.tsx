import { useState } from "react";

import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { Input } from "../../components/ui/Input";
import { Select } from "../../components/ui/Select";

type SchedulerPreset = "daily" | "weekly" | "monthly";

interface SingleDomainFormProps {
  onSubmit: (payload: {
    domain: string;
    scheduler_enabled: boolean;
    scheduler_preset?: SchedulerPreset;
  }) => Promise<void>;
  submitting: boolean;
}

export function SingleDomainForm({ onSubmit, submitting }: SingleDomainFormProps) {
  const [domain, setDomain] = useState("");
  const [schedulerEnabled, setSchedulerEnabled] = useState(false);
  const [schedulerPreset, setSchedulerPreset] = useState<SchedulerPreset>("daily");

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await onSubmit({
      domain,
      scheduler_enabled: schedulerEnabled,
      scheduler_preset: schedulerEnabled ? schedulerPreset : undefined,
    });
    setDomain("");
  }

  return (
    <Card title="Add domain" subtitle="Register one domain with an optional preset schedule.">
      <form className="grid gap-4" onSubmit={handleSubmit}>
        <Input
          label="Domain"
          placeholder="example.com"
          required
          value={domain}
          onChange={(event) => setDomain(event.target.value)}
        />
        <label className="flex items-center gap-3 rounded-2xl bg-slate-50 px-4 py-3 text-sm text-slate-700">
          <input
            checked={schedulerEnabled}
            className="h-4 w-4 rounded border-slate-300"
            onChange={(event) => setSchedulerEnabled(event.target.checked)}
            type="checkbox"
          />
          Enable scheduler preset
        </label>
        <Select
          disabled={!schedulerEnabled}
          label="Preset"
          value={schedulerPreset}
          onChange={(event) => setSchedulerPreset(event.target.value as SchedulerPreset)}
        >
          <option value="daily">Daily</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </Select>
        <Button disabled={submitting || !domain.trim()} type="submit">
          {submitting ? "Saving..." : "Add domain"}
        </Button>
      </form>
    </Card>
  );
}
