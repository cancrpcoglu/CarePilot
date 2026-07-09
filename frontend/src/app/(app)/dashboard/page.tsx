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
        Bu tek linki web sitenize, Instagram'a veya WhatsApp durumunuza koyun.
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

export default function DashboardPage() {
  const clinic = useQuery({ queryKey: ["clinic"], queryFn: api.myClinic });
  const patients = useQuery({ queryKey: ["patients"], queryFn: api.listPatients });
  const pendingReports = useQuery({
    queryKey: ["reports", "pending"],
    queryFn: () => api.listReports("pending"),
  });

  if (clinic.isLoading) {
    return <Spinner label="Panel yükleniyor…" />;
  }

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
        <StatCard label="Toplam hasta" value={patients.data?.length ?? "—"} />
        <StatCard label="Ülke" value={clinic.data?.country ?? "—"} />
        <Link href="/reports">
          <StatCard
            label="Bekleyen ön değerlendirme"
            value={pendingReports.data?.length ?? "—"}
            hint="Raporları görüntüle →"
          />
        </Link>
      </div>

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
