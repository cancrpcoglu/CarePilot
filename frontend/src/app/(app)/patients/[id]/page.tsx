"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { AssessmentView } from "@/components/assessment";
import { QrCode } from "@/components/qr";
import {
  Alert,
  Badge,
  Button,
  Card,
  Input,
  Label,
  Spinner,
  Textarea,
} from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import type { Patient, TriageRunResponse } from "@/lib/types";

const languages = [
  { value: "en", label: "İngilizce" },
  { value: "tr", label: "Türkçe" },
  { value: "ar", label: "Arapça" },
  { value: "de", label: "Almanca" },
  { value: "ru", label: "Rusça" },
  { value: "fr", label: "Fransızca" },
];

function ChatLinkCard({ accessToken }: { accessToken: string }) {
  const [link, setLink] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    setLink(`${window.location.origin}/chat/${accessToken}`);
  }, [accessToken]);

  const copy = async () => {
    try {
      await navigator.clipboard.writeText(link);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch {
      // pano erişimi yoksa sessizce geç
    }
  };

  return (
    <Card>
      <h2 className="text-base font-semibold text-slate-900">
        Hasta sohbet linki
      </h2>
      <p className="mt-1 text-sm text-slate-500">
        Bu linki hastaya gönderin; hasta yapay zeka asistanıyla kendi dilinde
        sohbet edip ön değerlendirmesini oluşturur.
      </p>
      <div className="mt-4 flex gap-2">
        <Input readOnly value={link} onFocus={(e) => e.target.select()} />
        <Button variant="outline" onClick={copy} className="shrink-0">
          {copied ? "Kopyalandı" : "Kopyala"}
        </Button>
      </div>
      {link && (
        <div className="mt-4 flex flex-wrap items-center gap-5">
          <QrCode value={link} />
          <a
            href={`https://wa.me/?text=${encodeURIComponent(
              `CarePilot ön değerlendirme sohbetiniz: ${link}`,
            )}`}
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center rounded-lg border border-slate-300 px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
          >
            WhatsApp ile gönder
          </a>
        </div>
      )}
    </Card>
  );
}

function PatientManageCard({ patient }: { patient: Patient }) {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [form, setForm] = useState({
    full_name: patient.full_name,
    language: patient.language,
    country: patient.country ?? "",
    notes: patient.notes ?? "",
  });
  const [saved, setSaved] = useState(false);
  const [confirmDelete, setConfirmDelete] = useState(false);

  const update = useMutation({
    mutationFn: () =>
      api.updatePatient(patient.id, {
        full_name: form.full_name,
        language: form.language,
        country: form.country || undefined,
        notes: form.notes,
      }),
    onSuccess: async () => {
      setSaved(true);
      setTimeout(() => setSaved(false), 2000);
      await queryClient.invalidateQueries({ queryKey: ["patient", patient.id] });
      await queryClient.invalidateQueries({ queryKey: ["patients"] });
    },
  });

  const remove = useMutation({
    mutationFn: () => api.deletePatient(patient.id),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["patients"] });
      router.replace("/patients");
    },
  });

  return (
    <Card>
      <h2 className="text-base font-semibold text-slate-900">Hasta bilgileri</h2>
      <div className="mt-4 grid gap-4 sm:grid-cols-3">
        <div>
          <Label htmlFor="edit_name">Ad soyad</Label>
          <Input
            id="edit_name"
            value={form.full_name}
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
          />
        </div>
        <div>
          <Label htmlFor="edit_lang">Dil</Label>
          <select
            id="edit_lang"
            value={form.language}
            onChange={(e) => setForm({ ...form, language: e.target.value })}
            className="w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 outline-none transition focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
          >
            {languages.map((lang) => (
              <option key={lang.value} value={lang.value}>
                {lang.label}
              </option>
            ))}
          </select>
        </div>
        <div>
          <Label htmlFor="edit_country">Ülke</Label>
          <Input
            id="edit_country"
            value={form.country}
            onChange={(e) => setForm({ ...form, country: e.target.value })}
          />
        </div>
      </div>

      <div className="mt-4">
        <Label htmlFor="edit_notes">Notlar (kliniğe özel, hasta görmez)</Label>
        <Textarea
          id="edit_notes"
          rows={3}
          value={form.notes}
          onChange={(e) => setForm({ ...form, notes: e.target.value })}
          placeholder="Bu hastaya dair notlarınız…"
        />
      </div>

      <div className="mt-4 flex items-center gap-3">
        <Button onClick={() => update.mutate()} disabled={update.isPending}>
          {update.isPending ? "Kaydediliyor…" : "Kaydet"}
        </Button>
        {saved && <span className="text-sm text-teal-600">Kaydedildi ✓</span>}
      </div>

      <div className="mt-6 border-t border-slate-100 pt-4">
        {!confirmDelete ? (
          <Button variant="danger" onClick={() => setConfirmDelete(true)}>
            Hastayı sil
          </Button>
        ) : (
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-sm text-slate-600">
              Emin misiniz? Bu işlem geri alınamaz.
            </span>
            <Button
              variant="danger"
              onClick={() => remove.mutate()}
              disabled={remove.isPending}
            >
              {remove.isPending ? "Siliniyor…" : "Evet, sil"}
            </Button>
            <Button variant="outline" onClick={() => setConfirmDelete(false)}>
              Vazgeç
            </Button>
          </div>
        )}
      </div>
    </Card>
  );
}

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

      <PatientManageCard patient={p} />

      <ChatLinkCard accessToken={p.access_token} />

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
