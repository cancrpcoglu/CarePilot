import { getToken } from "@/lib/auth";
import type { Clinic, JourneyStep, Patient, Token, User } from "@/lib/types";

const API_URL =
  process.env.NEXT_PUBLIC_API_URL ??
  "https://carepilot-backend-production.up.railway.app";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

interface RequestOptions {
  method?: string;
  body?: unknown;
  form?: Record<string, string>;
  auth?: boolean;
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { method = "GET", body, form, auth = true } = options;
  const headers: Record<string, string> = {};
  let payload: BodyInit | undefined;

  if (form) {
    headers["Content-Type"] = "application/x-www-form-urlencoded";
    payload = new URLSearchParams(form).toString();
  } else if (body !== undefined) {
    headers["Content-Type"] = "application/json";
    payload = JSON.stringify(body);
  }

  if (auth) {
    const token = getToken();
    if (token) headers["Authorization"] = `Bearer ${token}`;
  }

  const response = await fetch(`${API_URL}${path}`, { method, headers, body: payload });

  if (!response.ok) {
    let detail = "Beklenmeyen bir hata oluştu. Lütfen tekrar deneyin.";
    try {
      const data = await response.json();
      if (typeof data.detail === "string") detail = data.detail;
    } catch {
      // gövde JSON değilse varsayılan mesajı kullan
    }
    throw new ApiError(detail, response.status);
  }

  if (response.status === 204) return undefined as T;
  return (await response.json()) as T;
}

export const api = {
  register: (data: { email: string; password: string; full_name?: string }) =>
    request<User>("/api/v1/auth/register", {
      method: "POST",
      body: data,
      auth: false,
    }),

  login: (email: string, password: string) =>
    request<Token>("/api/v1/auth/login", {
      method: "POST",
      form: { username: email, password },
      auth: false,
    }),

  me: () => request<User>("/api/v1/auth/me"),

  createClinic: (data: {
    name: string;
    country?: string;
    contact_email?: string;
    contact_phone?: string;
  }) => request<Clinic>("/api/v1/clinics", { method: "POST", body: data }),

  myClinic: () => request<Clinic>("/api/v1/clinics/me"),

  listPatients: () => request<Patient[]>("/api/v1/patients"),

  createPatient: (data: { full_name: string; language?: string; country?: string }) =>
    request<Patient>("/api/v1/patients", { method: "POST", body: data }),

  patientJourney: (patientId: string) =>
    request<JourneyStep[]>(`/api/v1/patients/${patientId}/journey`),
};
