"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Alert, Button, Card, Input, Label, Spinner } from "@/components/ui";
import { api, ApiError } from "@/lib/api";

export default function SettingsPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [confirmName, setConfirmName] = useState("");
  const [error, setError] = useState<string | null>(null);

  const clinic = useQuery({ queryKey: ["clinic"], queryFn: api.myClinic });

  const remove = useMutation({
    mutationFn: () => api.deleteClinic(),
    onSuccess: () => {
      // Klinik silindi → tüm önbelleği temizle ve onboarding'e dön
      queryClient.clear();
      router.replace("/onboarding");
    },
    onError: (err) =>
      setError(err instanceof ApiError ? err.message : "Klinik silinemedi."),
  });

  if (clinic.isLoading) return <Spinner label="Yükleniyor…" />;

  const clinicName = clinic.data?.name ?? "";
  const canDelete = confirmName.trim() === clinicName && clinicName.length > 0;

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Ayarlar</h1>
        <p className="mt-1 text-sm text-slate-500">
          Klinik hesabınızı yönetin.
        </p>
      </div>

      <Card>
        <h2 className="text-base font-semibold text-slate-900">Klinik</h2>
        <dl className="mt-3 space-y-1 text-sm">
          <div className="flex gap-2">
            <dt className="text-slate-500">Ad:</dt>
            <dd className="text-slate-900">{clinicName}</dd>
          </div>
          {clinic.data?.country && (
            <div className="flex gap-2">
              <dt className="text-slate-500">Ülke:</dt>
              <dd className="text-slate-900">{clinic.data.country}</dd>
            </div>
          )}
        </dl>
      </Card>

      <Card className="border-red-200">
        <h2 className="text-base font-semibold text-red-700">Tehlikeli bölge</h2>
        <p className="mt-1 text-sm text-slate-600">
          Kliniği silmek, kliniğe bağlı tüm hastaları ve ön değerlendirme
          raporlarını da erişilmez kılar. Bu işlem geri alınamaz. Devam etmek
          için klinik adını (<span className="font-medium">{clinicName}</span>)
          aşağıya yazın.
        </p>

        <div className="mt-4 max-w-sm">
          <Label htmlFor="confirm_name">Onay için klinik adı</Label>
          <Input
            id="confirm_name"
            value={confirmName}
            onChange={(e) => setConfirmName(e.target.value)}
            placeholder={clinicName}
          />
        </div>

        {error && (
          <div className="mt-3 max-w-sm">
            <Alert message={error} />
          </div>
        )}

        <div className="mt-4">
          <Button
            variant="danger"
            disabled={!canDelete || remove.isPending}
            onClick={() => {
              setError(null);
              remove.mutate();
            }}
          >
            {remove.isPending ? "Siliniyor…" : "Kliniği kalıcı olarak sil"}
          </Button>
        </div>
      </Card>
    </div>
  );
}
