export interface LogRecord {
  id: number;
  level: string;
  scope: string;
  message: string;
  domain_id: number | null;
  run_id: number | null;
  metadata_json: {
    trigger_source?: string;
    final_provider?: string;
    provider_attempts?: Array<{
      provider: string;
      status: string;
      error_code?: string | null;
      error_message?: string | null;
    }>;
    error_code?: string | null;
    error_message?: string | null;
  } | null;
  created_at: string;
}
