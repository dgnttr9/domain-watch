import type { DomainRecord } from "./domain";
import type { LogRecord } from "./log";

export interface DashboardState {
  domains: DomainRecord[];
  logs: LogRecord[];
  selectedDomainId: number | null;
  selectedLogDomainId: number | null;
  loading: boolean;
  submitting: boolean;
  error: string | null;
}
