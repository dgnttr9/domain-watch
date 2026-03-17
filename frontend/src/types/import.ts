export interface ImportJob {
  id: number;
  source_type: string;
  file_name: string | null;
  total_rows: number;
  valid_rows: number;
  invalid_rows: number;
  status: string;
  error_summary: string | null;
}
