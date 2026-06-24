export type UserRole = "clinic_admin" | "patient";

export interface User {
  id: string;
  email: string;
  full_name: string | null;
  role: UserRole;
  is_active: boolean;
  clinic_id: string | null;
  created_at: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Clinic {
  id: string;
  name: string;
  country: string | null;
  contact_email: string | null;
  contact_phone: string | null;
  created_at: string;
}

export interface Patient {
  id: string;
  clinic_id: string;
  user_id: string | null;
  full_name: string;
  language: string;
  country: string | null;
  created_at: string;
}

export type JourneyStepStatus = "pending" | "completed" | "skipped";

export interface JourneyStep {
  id: string;
  patient_id: string;
  step_type: string;
  status: JourneyStepStatus;
  scheduled_at: string | null;
  completed_at: string | null;
  created_at: string;
}
