import { Badge } from "@/components/ui";
import { treatmentAreaLabels } from "@/lib/triage";
import type { TriageAssessment } from "@/lib/types";

function ListField({ label, items }: { label: string; items: string[] }) {
  if (items.length === 0) return null;
  return (
    <div>
      <p className="font-medium text-slate-700">{label}</p>
      <ul className="ml-4 mt-1 list-disc space-y-0.5 text-slate-600">
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

export function AssessmentView({ assessment }: { assessment: TriageAssessment }) {
  return (
    <div className="space-y-3 text-sm">
      <div className="flex flex-wrap gap-2">
        <Badge tone="info">{treatmentAreaLabels[assessment.treatment_area]}</Badge>
        <Badge tone="neutral">Dil: {assessment.detected_language}</Badge>
        {assessment.recommended_specialty && (
          <Badge tone="neutral">{assessment.recommended_specialty}</Badge>
        )}
      </div>

      <p className="text-slate-700">
        <span className="font-medium">Özet: </span>
        {assessment.summary}
      </p>

      {assessment.patient_expectations && (
        <p className="text-slate-700">
          <span className="font-medium">Beklenti: </span>
          {assessment.patient_expectations}
        </p>
      )}

      <ListField label="Ana şikayetler" items={assessment.primary_concerns} />
      <ListField label="İlgili sağlık geçmişi" items={assessment.relevant_medical_history} />
      <ListField
        label="Eksik bilgiler (hastaya sorulmalı)"
        items={assessment.missing_information}
      />
    </div>
  );
}
