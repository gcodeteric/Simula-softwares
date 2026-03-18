/**
 * API client with auth headers from Zustand store.
 * All requests go through Next.js rewrite → Express.
 */

class ApiClient {
  private getAuthHeaders(): Record<string, string> {
    // Read from persisted zustand store in localStorage
    if (typeof window === "undefined") return {};
    try {
      const raw = localStorage.getItem("simula-auth");
      if (!raw) return {};
      const state = JSON.parse(raw)?.state;
      if (state?.user?.id) {
        return { "X-Mock-User-Id": state.user.id };
      }
    } catch {}
    return {};
  }

  private async request<T>(path: string, options: RequestInit = {}): Promise<T> {
    const res = await fetch(path, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...this.getAuthHeaders(),
        ...options.headers,
      },
    });

    const data = await res.json();

    if (!res.ok) {
      throw new ApiError(res.status, data.error?.code || "UNKNOWN", data.error?.message || "Request failed");
    }

    return data;
  }

  async get<T = any>(path: string, params?: Record<string, string | undefined>): Promise<T> {
    const filtered: Record<string, string> = {};
    if (params) {
      for (const [k, v] of Object.entries(params)) {
        if (v !== undefined) filtered[k] = v;
      }
    }
    const search = Object.keys(filtered).length > 0 ? `?${new URLSearchParams(filtered)}` : "";
    return this.request(`${path}${search}`);
  }

  async post<T = any>(path: string, body?: unknown): Promise<T> {
    return this.request(path, {
      method: "POST",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async put<T = any>(path: string, body?: unknown): Promise<T> {
    return this.request(path, {
      method: "PUT",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async patch<T = any>(path: string, body?: unknown): Promise<T> {
    return this.request(path, {
      method: "PATCH",
      body: body ? JSON.stringify(body) : undefined,
    });
  }

  async del<T = any>(path: string): Promise<T> {
    return this.request(path, { method: "DELETE" });
  }

  /** Upload file with multipart form data */
  async upload<T = any>(path: string, file: File, data: Record<string, unknown>): Promise<T> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("data", JSON.stringify(data));

    const res = await fetch(path, {
      method: "POST",
      headers: this.getAuthHeaders(),
      body: formData,
    });

    const json = await res.json();
    if (!res.ok) {
      throw new ApiError(res.status, json.error?.code || "UNKNOWN", json.error?.message || "Upload failed");
    }
    return json;
  }
}

export class ApiError extends Error {
  constructor(public status: number, public code: string, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

export const api = new ApiClient();
