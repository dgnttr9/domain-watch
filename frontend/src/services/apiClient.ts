import type { ApiResponse } from "../types/api";
import type {
  DomainCheckPayload,
  DomainCreatePayload,
  DomainRecord,
  SchedulerUpdatePayload,
} from "../types/domain";
import type { ImportJob } from "../types/import";
import type { LogRecord } from "../types/log";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "http://127.0.0.1:8000/api/v1";

async function parseResponse<T>(response: Response): Promise<ApiResponse<T>> {
  const payload = (await response.json()) as ApiResponse<T>;

  if (!response.ok || payload.status === "error") {
    const message = payload.errors[0]?.message ?? payload.message ?? "Unexpected API error.";
    throw new Error(message);
  }

  return payload;
}

class ApiClient {
  async getDomains(): Promise<DomainRecord[]> {
    const response = await fetch(`${API_BASE_URL}/domains`);
    const payload = await parseResponse<DomainRecord[]>(response);
    return payload.data;
  }

  async createDomain(payload: DomainCreatePayload): Promise<DomainRecord> {
    const response = await fetch(`${API_BASE_URL}/domains`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return (await parseResponse<DomainRecord>(response)).data;
  }

  async checkDomains(payload: DomainCheckPayload): Promise<DomainRecord[]> {
    const response = await fetch(`${API_BASE_URL}/domains/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return (await parseResponse<DomainRecord[]>(response)).data;
  }

  async recheckDomain(domainId: number): Promise<DomainRecord> {
    const response = await fetch(`${API_BASE_URL}/domains/${domainId}/recheck`, {
      method: "POST",
    });
    return (await parseResponse<DomainRecord>(response)).data;
  }

  async importText(content: string): Promise<ImportJob> {
    const response = await fetch(`${API_BASE_URL}/imports/text`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ content }),
    });
    return (await parseResponse<ImportJob>(response)).data;
  }

  async importFile(file: File): Promise<ImportJob> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${API_BASE_URL}/imports/file`, {
      method: "POST",
      body: formData,
    });
    return (await parseResponse<ImportJob>(response)).data;
  }

  async getLogs(filters?: {
    level?: string;
    domainId?: number | null;
    createdFrom?: string;
    createdTo?: string;
  }): Promise<LogRecord[]> {
    const params = new URLSearchParams();
    if (filters?.level) params.set("level", filters.level);
    if (filters?.domainId) params.set("domain_id", String(filters.domainId));
    if (filters?.createdFrom) params.set("created_from", filters.createdFrom);
    if (filters?.createdTo) params.set("created_to", filters.createdTo);

    const response = await fetch(
      `${API_BASE_URL}/logs${params.toString() ? `?${params.toString()}` : ""}`,
    );
    return (await parseResponse<LogRecord[]>(response)).data;
  }

  async updateScheduler(domainId: number, payload: SchedulerUpdatePayload): Promise<DomainRecord> {
    const response = await fetch(`${API_BASE_URL}/scheduler/domains/${domainId}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    return (await parseResponse<DomainRecord>(response)).data;
  }

  async dispatchScheduler(limit = 25): Promise<DomainRecord[]> {
    const response = await fetch(`${API_BASE_URL}/scheduler/dispatch?limit=${limit}`, {
      method: "POST",
    });
    return (await parseResponse<DomainRecord[]>(response)).data;
  }

  getExportUrl(format: "csv" | "json"): string {
    return `${API_BASE_URL}/exports/domains.${format}`;
  }
}

export const apiClient = new ApiClient();
