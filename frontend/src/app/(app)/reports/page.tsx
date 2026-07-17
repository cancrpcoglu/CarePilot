"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import Link from "next/link";
import { useState } from "react";

import { AssessmentView } from "@/components/assessment";
import { Badge, Button, Card, Input, Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { reportStatusLabels, reportStatusTone } from "@/lib/triage";
import type { TriageReport, TriageReportStatus } from "@/lib/types";

const filters: { value: TriageReportStatus | "all"; label: string }[] = [
  { value: "all", label: "Tümü" },
  { value: "pending", label: "Bekleyen" },
  { value: "approved", label: "Onaylanan" },
  { value: "rejected", label: "Reddedilen" },
];

export default function ReportsPage() {
  const [filter, setFilter] = useState<TriageReportStatus | "all">("pending");
  const [searchInput, setSearchInput] = useState("");
  const [searchResults, setSearchResults] = useState<TriageReport[] | null>(null);
  const queryClient = useQueryClient();

  const patients = useQuery({ queryKey: ["patients"], queryFn: api.listPatients });
  const reports = useQuery({
    queryKey: ["reports", filter],
    queryFn: () => api.listReports(filter === "all" ? undefined : filter),
  });

  const review = useMutation({
    mutationFn: ({ id, action }: { id: string; action: "approve" | "reject" }) =>
      action === "approve" ? api.approveReport(id) : api.rejectReport(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reports"] });
      setSearchResults(null);
    },
  });

  const search = useMutation({
    mutationFn: () => api.searchReports(searchInput.trim()),
    onSuccess: (data) => setSearchResults(data),
  });

  const clearSearch = () => {
    setSearchResults(null);
    setSearchInput("");
  };

  const patientName = (id: string) =>
    patients.data?.find((p) => p.id === id)?.full_name ?? "Bilinmeyen hasta";

  const isSearching = searchResults !== null;
  const displayReports = searchResults ?? reports.data ?? [];

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

      <Card>
        <form
          className="flex flex-wrap gap-2"
          onSubmit={(e) => {
            e.preventDefault();
            if (searchInput.trim().length >= 2) search.mutate();
          }}
        >
          <Input
            value={searchInput}
            onChange={(e) => setSearchInput(e.target.value)}
            placeholder="Anlamsal arama — örn. “diyabetli estetik hastaları”"
            className="flex-1"
          />
          <Button type="submit" disabled={search.isPending} className="shrink-0">
            {search.isPending ? "Aranıyor…" : "Ara"}
          </Button>
          {isSearching && (
            <Button
              type="button"
              variant="outline"
              onClick={clearSearch}
              className="shrink-0"
            >
              Temizle
            </Button>
          )}
        </form>
        <p className="mt-2 text-xs text-slate-400">
          Yapay zeka, anlam benzerliğine göre en alakalı raporları getirir
          (embedding tabanlı — pgvector).
        </p>
      </Card>

      {!isSearching && (
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
      )}

      {isSearching && (
        <p className="text-sm text-slate-500">
          “{searchInput}” için {displayReports.length} sonuç (en alakalı önce)
        </p>
      )}

      {!isSearching && reports.isLoading ? (
        <Spinner label="Raporlar yükleniyor…" />
      ) : displayReports.length > 0 ? (
        <div className="space-y-4">
          {displayReports.map((report) => (
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
          {isSearching
            ? "Bu arama için sonuç bulunamadı."
            : "Bu filtrede rapor yok. Bir hastanın detay sayfasından “AI ön değerlendirme çalıştır” ile rapor oluşturabilirsiniz."}
        </div>
      )}
    </div>
  );
}
