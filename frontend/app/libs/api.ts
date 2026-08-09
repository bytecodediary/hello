const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000";

export type HttpMethod = "GET" | "POST" | "PUT" | "PATCH" | "DELETE" | "OPTIONS";

interface ApiRequestOptions extends Omit<RequestInit, "body"> {
  method?: HttpMethod;
  query?: Record<string, string | number | boolean | undefined | null>;
  body?: Record<string, unknown> | FormData | undefined;
  authenticated?: boolean;
}

interface ApiErrorPayload {
  detail?: string;
  [key: string]: unknown;
}

export class ApiError<T = ApiErrorPayload> extends Error {
  readonly status: number;
  readonly data: T | null;

  constructor(message: string, status: number, data: T | null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.data = data;
  }
}

function buildQueryString(query: ApiRequestOptions["query"]): string {
  if (!query) {
    return "";
  }

  const params = new URLSearchParams();
  Object.entries(query).forEach(([key, value]) => {
    if (value === undefined || value === null) {
      return;
    }
    params.append(key, String(value));
  });

  const queryString = params.toString();
  return queryString ? `?${queryString}` : "";
}

function resolveBody(body: ApiRequestOptions["body"]): BodyInit | undefined {
  if (!body) {
    return undefined;
  }

  if (body instanceof FormData) {
    return body;
  }

  return JSON.stringify(body);
}

function defaultHeaders(body: ApiRequestOptions["body"]): HeadersInit {
  if (body instanceof FormData) {
    return {};
  }

  return {
    "Content-Type": "application/json",
  };
}

function getCookie(name: string): string | null {
  if (typeof document === "undefined") return null;
  const value = document.cookie.split("; ").find((cookie) => cookie.startsWith(`${name}=`));
  return value ? decodeURIComponent(value.split("=").slice(1).join("=")) : null;
}

async function ensureCsrfCookie(): Promise<void> {
  if (typeof window === "undefined" || getCookie("csrftoken")) return;
  await fetch(`${API_BASE_URL}/user/get_csrf_token/`, { credentials: "include" });
}

async function parseJson<T>(response: Response): Promise<T | null> {
  const text = await response.text();
  if (!text) {
    return null;
  }

  try {
    return JSON.parse(text) as T;
  } catch (error) {
    console.error("Failed to parse JSON response", error);
    return null;
  }
}

export async function apiFetch<TResponse>(
  endpoint: string,
  options: ApiRequestOptions = {}
): Promise<TResponse> {
  const { query, body, headers, authenticated: _authenticated = true, method = "GET", ...rest } = options;
  void _authenticated;

  if (!["GET", "HEAD", "OPTIONS"].includes(method)) {
    await ensureCsrfCookie();
  }

  const url = `${API_BASE_URL}${endpoint}${buildQueryString(query)}`;
  const baseHeaders: HeadersInit = {
    ...defaultHeaders(body),
    ...(!["GET", "HEAD", "OPTIONS"].includes(method) && getCookie("csrftoken")
      ? { "X-CSRFToken": getCookie("csrftoken") as string }
      : {}),
  };

  const response = await fetch(url, {
    method,
    headers: {
      ...baseHeaders,
      ...(headers ?? {}),
    },
    body: resolveBody(body),
    credentials: "include",
    ...rest,
  });

  if (!response.ok) {
    const errorPayload = await parseJson<ApiErrorPayload>(response);
    const message = errorPayload?.detail ?? response.statusText;
    throw new ApiError(message || "Request failed", response.status, errorPayload);
  }

  if (response.status === 204) {
    return undefined as TResponse;
  }

  const data = await parseJson<TResponse>(response);
  return (data ?? (undefined as TResponse));
}

export async function apiFetchJson<TResponse>(
  endpoint: string,
  options: ApiRequestOptions = {}
): Promise<TResponse> {
  return apiFetch<TResponse>(endpoint, options);
}

export const apiClient = {
  get: <TResponse>(endpoint: string, options: ApiRequestOptions = {}) =>
    apiFetch<TResponse>(endpoint, { ...options, method: "GET" }),
  post: <TResponse>(endpoint: string, options: ApiRequestOptions = {}) =>
    apiFetch<TResponse>(endpoint, { ...options, method: "POST" }),
  put: <TResponse>(endpoint: string, options: ApiRequestOptions = {}) =>
    apiFetch<TResponse>(endpoint, { ...options, method: "PUT" }),
  patch: <TResponse>(endpoint: string, options: ApiRequestOptions = {}) =>
    apiFetch<TResponse>(endpoint, { ...options, method: "PATCH" }),
  delete: <TResponse>(endpoint: string, options: ApiRequestOptions = {}) =>
    apiFetch<TResponse>(endpoint, { ...options, method: "DELETE" }),
};

export type { ApiRequestOptions };
