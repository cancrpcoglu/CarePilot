"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useEffect, useState } from "react";

import { QrCode } from "@/components/qr";
import { Button, Card, Input, Spinner } from "@/components/ui";
import { api } from "@/lib/api";

function IntakeLinkCard({ intakeToken }: { intakeToken: string }) {
  const [link, setLink] = useState("");
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    setLink(`${window.location.origin}/intake/${intakeToken}`);
  }, [intakeToken]);

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
        Klinik davet linki (self-servis)
      </h2>
      <p className="mt-1 text-sm text-slate-500">
        Bu tek linki web sitenize, Instagram&apos;a veya WhatsApp durumunuza koyun.
        Yeni hastalar buradan kendileri ön kayıt olup AI ile sohbet eder; hasta
        ve ön değerlendirme raporu panelinizde otomatik belirir.
      </p>
      <div className="mt-4 flex gap-2">
        <Input readOnly value={link} onFocus={(e) => e.target.select()} />
        <Button variant="outline" onClick={copy} className="shrink-0">
          {copied ? "Kopyalandı" : "Kopyala"}
        </Button>
      </div>
      {link && (
        <div className="mt-4">
          <QrCode value={link} />
        </div>
      )}
    </Card>
  );
}

function StatCard({
  label,
  value,
  hint,
}: {
  label: string;
  value: string | number;
  hint?: string;
}) {
  return (
    <div className="rounded-xl border border-slate-200 bg-white p-5">
      <p className="text-sm text-slate-500">{label}</p>
      <p className="mt-1 text-2xl font-semibold text-slate-900">{value}</p>
      {hint && <p className="mt-1 text-xs text-slate-400">{hint}</p>}
    </div>
  );
}

function FunnelCard({
  patients,
  reports,
  approved,
}: {
  patients: number;
  reports: number;
  approved: number;
}) {
  const pct = (n: number) => (patients > 0 ? Math.round((n / patients) * 100) : 0);
  const stages = [
    { label: "Hasta (ön kayıt)", value: patients, width: 100, tone: "bg-teal-600" },
    {
      label: "Ön değerlendirme üretildi",
      value: reports,
      width: pct(reports),
      tone: "bg-teal-500",
    },
    {
      label: "Onaylandı",
      value: approved,
      width: pct(approved),
      tone: "bg-emerald-500",
    },
  ];

  return (
    <Card>
      <h2 className="text-base font-semibold text-slate-900">Dönüşüm hunisi</h2>
      <p className="mt-1 text-sm text-slate-500">
        Ön kayıttan onaylı ön değerlendirmeye kadar hasta akışı.
      </p>
      <div className="mt-4 space-y-3">
        {stages.map((s) => (
          <div key={s.label}>
            <div className="mb-1 flex items-center justify-between text-sm">
              <span className="text-slate-600">{s.label}</span>
              <span className="font-medium text-slate-900">
                {s.value}
                {s.width < 100 && (
                  <span className="ml-1 text-xs text-slate-400">
                    ({s.width}%)
                  </span>
                )}
              </span>
            </div>
            <div className="h-2.5 w-full overflow-hidden rounded-full bg-slate-100">
              <div
                className={`h-full rounded-full ${s.tone} transition-all`}
                style={{ width: `${Math.max(s.width, s.value > 0 ? 4 : 0)}%` }}
              />
            </div>
          </div>
        ))}
      </div>
    </Card>
  );
}

export default function DashboardPage() {
  const clinic = useQuery({ queryKey: ["clinic"], queryFn: api.myClinic });
  const patients = useQuery({ queryKey: ["patients"], queryFn: api.listPatients });
  const reports = useQuery({
    queryKey: ["reports", "all"],
    queryFn: () => api.listReports(),
  });

  if (clinic.isLoading) {
    return <Spinner label="Panel yükleniyor…" />;
  }

  const patientCount = patients.data?.length ?? 0;
  const reportCount = reports.data?.length ?? 0;
  const approvedCount =
    reports.data?.filter((r) => r.status === "approved").length ?? 0;
  const pendingCount =
    reports.data?.filter((r) => r.status === "pending").length ?? 0;

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">
          {clinic.data?.name ?? "Klinik paneli"}
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Klinik paneli — hasta ve ön değerlendirme yönetimi
        </p>
      </div>

      <div className="grid gap-5 sm:grid-cols-3">
        <StatCard label="Toplam hasta" value={patientCount} />
        <Link href="/reports">
          <StatCard
            label="Bekleyen ön değerlendirme"
            value={pendingCount}
            hint="Raporları görüntüle →"
          />
        </Link>
        <StatCard label="Onaylanan" value={approvedCount} />
      </div>

      <FunnelCard
        patients={patientCount}
        reports={reportCount}
        approved={approvedCount}
      />

      {clinic.data && <IntakeLinkCard intakeToken={clinic.data.intake_token} />}

      <Card>
        <h2 className="text-base font-semibold text-slate-900">Hızlı işlemler</h2>
        <p className="mt-1 text-sm text-slate-500">
          Hastalarınızı yönetin, yeni hasta ekleyin.
        </p>
        <div className="mt-4">
          <Link
            href="/patients"
            className="inline-flex items-center gap-1 rounded-lg bg-teal-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-teal-700"
          >
            Hastalara git →
          </Link>
        </div>
      </Card>
    </div>
  );
}
