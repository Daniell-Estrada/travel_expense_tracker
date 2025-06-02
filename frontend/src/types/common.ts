export interface ApiResponse<T> {
  data: T;
  message?: string;
  status: number;
}

export interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}

export type LoadingState = "idle" | "loading" | "success" | "error";

export interface ErrorState {
  message: string;
  code?: string;
  details?: unknown;
}
