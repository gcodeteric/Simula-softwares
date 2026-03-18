// ---- API Response Envelope ----
export interface ApiResponse<T> {
  success: true;
  data: T;
}

export interface ApiErrorResponse {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, string[]>;
  };
}

export interface PaginatedResponse<T> {
  success: true;
  data: T[];
  pagination: {
    page: number;
    pageSize: number;
    total: number;
    totalPages: number;
  };
}

// ---- Comparison ----
export interface ComparisonResult {
  categories: ComparisonCategory[];
  summary: {
    totalParams: number;
    changedParams: number;
    categoriesAffected: string[];
  };
}

export interface ComparisonCategory {
  name: string;
  parameters: ComparisonParameter[];
  hasChanges: boolean;
}

export interface ComparisonParameter {
  key: string;
  label: string;
  unit: string | null;
  category: string;
  valueA: unknown;
  valueB: unknown;
  changed: boolean;
  delta: number | null;
  deltaPercent: number | null;
}

// ---- Query Parameters ----
export interface LibraryQueryParams {
  page?: number;
  pageSize?: number;
  carId?: string;
  trackId?: string;
  sim?: string;
  tags?: string[];
  search?: string;
  folder?: string;
  isFavorite?: boolean;
  sortBy?: "name" | "createdAt" | "updatedAt";
  sortOrder?: "asc" | "desc";
}
