"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useState } from "react";

import { AssessmentView } from "@/components/assessment";
import { Badge, Button, Card, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { reportStatusLabels, reportStatusTone } from "@/lib/triage";
import type { TriageReportStatus } from "@/lib/types";

const filters: { value: TriageReportStatus | "all"; label: string }[] = [
  { value: "all", label: "Tümü" },
  { value: "pending", label: "Bekleyen" },
  { value: "approved", label: "Onaylanan" },
  { value: "rejected", label: "Reddedilen" },
];

export default function ReportsPage() {
  const [filter, setFilter] = useState<TriageReportStatus | "all">("pending");
  const queryClient = useQueryClient();

  const patients = useQuery({ queryKey: ["patients"], queryFn: api.listPatients });
  const reports = useQuery({
    queryKey: ["reports", filter],
    queryFn: () => api.listReports(filter === "all" ? undefined : filter),
  });

  const review = useMutation({
    mutationFn: ({ id, action }: { id: string; action: "approve" | "reject" }) =>
      action === "approve" ? api.approveReport(id) : api.rejectReport(id),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["reports"] }),
  });

  const patientName = (id: string) =>
    patients.data?.find((p) => p.id === id)?.full_name ?? "Bilinmeyen hasta";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">
          Ön Değerlendirme Raporları
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Yapay zekanın ürettiği raporları inceleyin, onaylayın veya reddedin.
        </p>
      </div>

      <div className="flex flex-wrap gap-2">
        {filters.map((f) => (
          <button
            key={f.value}
            onClick={() => setFilter(f.value)}
            className={`rounded-lg px-3 py-1.5 text-sm font-medium transition ${
              filter === f.value
                ? "bg-teal-600 text-white"
                : "border border-slate-300 text-slate-600 hover:bg-slate-50"
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {reports.isLoading ? (
        <Spinner label="Raporlar yükleniyor…" />
      ) : reports.data && reports.data.length > 0 ? (
        <div className="space-y-4">
          {reports.data.map((report) => (
            <Card key={report.id}>
              <div className="flex items-start justify-between gap-4">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <Link
                      href={`/patients/${report.patient_id}`}
                      className="font-medium text-slate-900 hover:text-teal-700"
                    >
                      {patientName(report.patient_id)}
                    </Link>
                    <Badge tone={reportStatusTone[report.status]}>
                      {reportStatusLabels[report.status]}
                    </Badge>
                  </div>
                  <p className="mt-1 text-xs text-slate-400">
                    {new Date(report.created_at).toLocaleString("tr-TR")}
                  </p>
                </div>
                {report.status === "pending" && (
                  <div className="flex shrink-0 gap-2">
                    <Button
                      onClick={() => review.mutate({ id: report.id, action: "approve" })}
                      disabled={review.isPending}
                    >
                      Onayla
                    </Button>
                    <Button
                      variant="danger"
                      onClick={() => review.mutate({ id: report.id, action: "reject" })}
                      disabled={review.isPending}
                    >
                      Reddet
                    </Button>
                  </div>
                )}
              </div>
              <div className="mt-4 border-t border-slate-100 pt-4">
                <AssessmentView assessment={report.structured_data} />
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <div className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-12 text-center text-sm text-slate-500">
          Bu filtrede rapor yok. Bir hastanın detay sayfasından
          <span className="font-medium"> “AI ön değerlendirme çalıştır” </span>
          ile rapor oluşturabilirsiniz.
        </div>
      )}
    </div>
  );
}
