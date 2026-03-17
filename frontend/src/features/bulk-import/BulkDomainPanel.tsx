import { useState } from "react";

import { Button } from "../../components/ui/Button";
import { Card } from "../../components/ui/Card";
import { TextArea } from "../../components/ui/TextArea";

interface BulkDomainPanelProps {
  onCheckDomains: (domains: string[]) => Promise<void>;
  onImportText: (content: string) => Promise<void>;
  onImportFile: (file: File) => Promise<void>;
  submitting: boolean;
}

export function BulkDomainPanel({
  onCheckDomains,
  onImportText,
  onImportFile,
  submitting,
}: BulkDomainPanelProps) {
  const [content, setContent] = useState("");

  const parsedDomains = content
    .split(/\r?\n/)
    .map((item) => item.trim())
    .filter(Boolean);

  async function handleFileChange(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    await onImportFile(file);
    event.target.value = "";
  }

  return (
    <Card title="Bulk actions" subtitle="Paste a list or upload txt/csv for validation, import, and checking.">
      <div className="grid gap-4">
        <TextArea
          label="Bulk domain list"
          placeholder={"openai.com\nexample.org"}
          value={content}
          onChange={(event) => setContent(event.target.value)}
        />
        <div className="grid gap-3 sm:grid-cols-3">
          <Button disabled={submitting || parsedDomains.length === 0} onClick={() => void onCheckDomains(parsedDomains)} type="button">
            {submitting ? "Running..." : "Check list"}
          </Button>
          <Button
            disabled={submitting || !content.trim()}
            onClick={() => void onImportText(content)}
            type="button"
            variant="secondary"
          >
            Import text
          </Button>
          <label className="inline-flex cursor-pointer items-center justify-center rounded-xl bg-white px-4 py-2.5 text-sm font-medium text-ink-950 ring-1 ring-slate-200 transition hover:bg-slate-50">
            Upload txt/csv
            <input accept=".txt,.csv" className="hidden" onChange={handleFileChange} type="file" />
          </label>
        </div>
      </div>
    </Card>
  );
}
