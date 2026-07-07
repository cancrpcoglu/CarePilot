"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useParams } from "next/navigation";
import { useState } from "react";

import { AssessmentView } from "@/components/assessment";
import { Alert, Badge, Button, Card, Input, Spinner, Textarea } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import type { TriageRunResponse } from "@/lib/types";

function JourneySection({ patientId }: { patientId: string }) {
  const queryClient = useQueryClient();
  const [stepType, setStepType] = useState("");
  const journey = useQuery({
    queryKey: ["journey", patientId],
    queryFn: () => api.patientJourney(patientId),
  });
  const add = useMutation({
    mutationFn: () => api.addJourneyStep(patientId, stepType),
    onSuccess: () => {
      setStepType("");
      queryClient.invalidateQueries({ queryKey: ["journey", patientId] });
    },
  });
  const complete = useMutation({
    mutationFn: (stepId: string) => api.updateJourneyStep(stepId, "completed"),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["journey", patientId] }),
  });

  return (
    <div className="mt-3 space-y-3">
      <div className="flex gap-2">
        <Input
          value={stepType}
          onChange={(e) => setStepType(e.target.value)}
          placeholder="Adım (örn: pre_op_consultation)"
        />
        <Button
          onClick={() => stepType.trim() && add.mutate()}
          disabled={add.isPending}
        >
          Ekle
        </Button>
      </div>
      {journey.data && journey.data.length > 0 ? (
        <ul className="divide-y divide-slate-100">
          {journey.data.map((step) => (
            <li key={step.id} className="flex items-center justify-between py-2 text-sm">
              <span className="text-slate-700">{step.step_type}</span>
              <div className="flex items-center gap-2">
                <Badge tone={step.status === "completed" ? "success" : "neutral"}>
                  {step.status === "completed" ? "Tamamlandı" : "Bekliyor"}
                </Badge>
                {step.status !== "completed" && (
                  <button
                    onClick={() => complete.mutate(step.id)}
                    className="text-xs font-medium text-teal-600 hover:underline"
                  >
                    Tamamla
                  </button>
                )}
              </div>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-slate-400">Henüz yolculuk adımı yok.</p>
      )}
    </div>
  );
}

export default function PatientDetailPage() {
  const params = useParams();
  const patientId = params.id as string;
  const queryClient = useQueryClient();

  const [message, setMessage] = useState("");
  const [result, setResult] = useState<TriageRunResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  const patient = useQuery({
    queryKey: ["patient", patientId],
    queryFn: () => api.getPatient(patientId),
  });

  const triage = useMutation({
    mutationFn: () => api.runTriage(patientId, message, patient.data?.language),
    onSuccess: (data) => {
      setResult(data);
      setMessage("");
      queryClient.invalidateQueries({ queryKey: ["reports"] });
    },
    onError: (err) =>
      setError(err instanceof ApiError ? err.message : "Değerlendirme oluşturulamadı."),
  });

  if (patient.isLoading) return <Spinner label="Yükleniyor…" />;
  if (patient.isError || !patient.data) {
    return (
      <div className="text-sm text-slate-500">
        Hasta bulunamadı.{" "}
        <Link href="/patients" className="text-teal-600 hover:underline">
          Hastalara dön
        </Link>
      </div>
    );
  }

  const p = patient.data;

  return (
    <div className="space-y-6">
      <Link href="/patients" className="text-sm text-teal-600 hover:underline">
        ← Hastalar
      </Link>

      <div>
        <h1 className="text-2xl font-semibold text-slate-900">{p.full_name}</h1>
        <p className="mt-1 text-sm text-slate-500">
          Dil: {p.language} · Ülke: {p.country ?? "—"}
        </p>
      </div>

      <Card>
        <h2 className="text-base font-semibold text-slate-900">
          AI ön değerlendirme çalıştır
        </h2>
        <p className="mt-1 text-sm text-slate-500">
          Hastanın mesajını girin; yapay zeka yapılandırılmış bir ön değerlendirme
          üretip onay bekleyen bir rapor oluşturur.
        </p>
        <div className="mt-4 space-y-3">
          <Textarea
            rows={4}
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Örn: Merhaba, 32 yaşındayım, saçlarım tepeden dökülüyor ve saç ekimi düşünüyorum. Genel sağlığım iyi."
          />
          {error && <Alert message={error} />}
          <Button
            onClick={() => {
              setError(null);
              if (message.trim().length < 5) {
                setError("Lütfen hastanın mesajını girin.");
                return;
              }
              triage.mutate();
            }}
            disabled={triage.isPending}
          >
            {triage.isPending ? "Yapay zeka değerlendiriyor…" : "Değerlendirme oluştur"}
          </Button>
        </div>

        {result && (
          <div className="mt-4 rounded-lg border border-teal-100 bg-teal-50/40 p-4">
            <div className="mb-3 flex items-center gap-2">
              <Badge tone="success">Rapor oluşturuldu</Badge>
              <Link href="/reports" className="text-sm text-teal-700 hover:underline">
                Raporlarda görüntüle →
              </Link>
            </div>
            <AssessmentView assessment={result.assessment} />
          </div>
        )}
      </Card>

      <Card>
        <h2 className="text-base font-semibold text-slate-900">Hasta yolculuğu</h2>
        <JourneySection patientId={patientId} />
      </Card>
    </div>
  );
}
