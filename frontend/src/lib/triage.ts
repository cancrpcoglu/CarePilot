import type { TreatmentArea, TriageReportStatus } from "@/lib/types";

export const treatmentAreaLabels: Record<TreatmentArea, string> = {
  hair_transplant: "Saç Ekimi",
  aesthetic_surgery: "Estetik Cerrahi",
  other: "Diğer",
};

export const reportStatusLabels: Record<TriageReportStatus, string> = {
  pending: "Bekliyor",
  approved: "Onaylandı",
  rejected: "Reddedildi",
};

export const reportStatusTone: Record<
  TriageReportStatus,
  "warning" | "success" | "danger"
> = {
  pending: "warning",
  approved: "success",
  rejected: "danger",
};
