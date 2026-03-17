export interface DomainRecord {
  id: number;
  domain: string;
  status: string;
  provider_used: string | null;
  expiration_date: string | null;
  days_left: number | null;
  last_checked_at: string | null;
  next_check_at: string | null;
  scheduler_enabled: boolean;
  scheduler_preset: string | null;
  last_error_message: string | null;
}

export interface DomainCreatePayload {
  domain: string;
  scheduler_enabled: boolean;
  scheduler_preset?: "daily" | "weekly" | "monthly";
}

export interface DomainCheckPayload {
  domains: string[];
}

export interface SchedulerUpdatePayload {
  scheduler_enabled: boolean;
  scheduler_preset?: "daily" | "weekly" | "monthly";
}
