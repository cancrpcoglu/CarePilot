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
  access_token: string;
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

export type TreatmentArea = "hair_transplant" | "aesthetic_surgery" | "other";

export interface TriageAssessment {
  detected_language: string;
  treatment_area: TreatmentArea;
  summary: string;
  primary_concerns: string[];
  patient_expectations: string | null;
  relevant_medical_history: string[];
  missing_information: string[];
  recommended_specialty: string | null;
}

export type TriageReportStatus = "pending" | "approved" | "rejected";

export interface TriageReport {
  id: string;
  patient_id: string;
  conversation_id: string;
  structured_data: TriageAssessment;
  status: TriageReportStatus;
  reviewed_by: string | null;
  created_at: string;
  updated_at: string;
}

export interface TriageRunResponse {
  report_id: string;
  conversation_id: string;
  assessment: TriageAssessment;
}

export type ChatRole = "user" | "agent";

export interface ChatMessage {
  role: ChatRole;
  content: string;
  created_at: string;
}

export interface ChatSession {
  patient_name: string;
  language: string;
  messages: ChatMessage[];
}

export interface ChatSendResponse {
  reply: string;
  is_complete: boolean;
  report_id: string | null;
}
