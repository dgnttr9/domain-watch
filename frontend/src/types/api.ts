export interface ErrorDetail {
  code: string;
  message: string;
  field?: string | null;
}

export interface ApiResponse<T> {
  status: "success" | "error";
  message: string;
  data: T;
  errors: ErrorDetail[];
}
