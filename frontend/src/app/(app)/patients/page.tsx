"use client";

import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useState } from "react";

import { Alert, Button, Card, Input, Label, Spinner } from "@/components/ui";
import { api, ApiError } from "@/lib/api";

const languages = [
  { value: "en", label: "İngilizce" },
  { value: "tr", label: "Türkçe" },
  { value: "ar", label: "Arapça" },
  { value: "de", label: "Almanca" },
  { value: "ru", label: "Rusça" },
  { value: "fr", label: "Fransızca" },
];

const languageLabel = (value: string) =>
  languages.find((l) => l.value === value)?.label ?? value;

export default function PatientsPage() {
  const queryClient = useQueryClient();
  const [form, setForm] = useState({ full_name: "", language: "en", country: "" });
  const [error, setError] = useState<string | null>(null);

  const patients = useQuery({ queryKey: ["patients"], queryFn: api.listPatients });

  const mutation = useMutation({
    mutationFn: () =>
      api.createPatient({
        full_name: form.full_name,
        language: form.language,
        country: form.country || undefined,
      }),
    onSuccess: async () => {
      setForm({ full_name: "", language: "en", country: "" });
      await queryClient.invalidateQueries({ queryKey: ["patients"] });
    },
    onError: (err) =>
      setError(err instanceof ApiError ? err.message : "Hasta eklenemedi."),
  });

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-2xl font-semibold text-slate-900">Hastalar</h1>
        <p className="mt-1 text-sm text-slate-500">
          Kliniğinize ait hastaları görüntüleyin ve yeni hasta ekleyin.
        </p>
      </div>

      <Card>
        <h2 className="text-base font-semibold text-slate-900">Yeni hasta ekle</h2>
        <form
          className="mt-4 grid gap-4 sm:grid-cols-3"
          onSubmit={(e) => {
            e.preventDefault();
            setError(null);
            if (form.full_name.trim().length < 2) {
              setError("Lütfen geçerli bir ad girin.");
              return;
            }
            mutation.mutate();
          }}
        >
          <div className="sm:col-span-1">
            <Label htmlFor="full_name">Ad soyad</Label>
            <Input
              id="full_name"
              value={form.full_name}
              onChange={(e) => setForm({ ...form, full_name: e.target.value })}
              placeholder="John Smith"
            />
          </div>
          <div>
            <Label htmlFor="language">Dil</Label>
            <select
              id="language"
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
            <Label htmlFor="country">Ülke (opsiyonel)</Label>
            <Input
              id="country"
              value={form.country}
              onChange={(e) => setForm({ ...form, country: e.target.value })}
              placeholder="Germany"
            />
          </div>

          {error && (
            <div className="sm:col-span-3">
              <Alert message={error} />
            </div>
          )}

          <div className="sm:col-span-3">
            <Button type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? "Ekleniyor…" : "Hasta ekle"}
            </Button>
          </div>
        </form>
      </Card>

      <div>
        <h2 className="mb-3 text-base font-semibold text-slate-900">
          Hasta listesi
        </h2>
        {patients.isLoading ? (
          <Spinner label="Hastalar yükleniyor…" />
        ) : patients.data && patients.data.length > 0 ? (
          <div className="overflow-hidden rounded-xl border border-slate-200 bg-white">
            <table className="w-full text-sm">
              <thead className="border-b border-slate-200 bg-slate-50 text-left text-slate-500">
                <tr>
                  <th className="px-5 py-3 font-medium">Ad soyad</th>
                  <th className="px-5 py-3 font-medium">Dil</th>
                  <th className="px-5 py-3 font-medium">Ülke</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {patients.data.map((patient) => (
                  <tr key={patient.id} className="text-slate-900">
                    <td className="px-5 py-3 font-medium">{patient.full_name}</td>
                    <td className="px-5 py-3 text-slate-600">
                      {languageLabel(patient.language)}
                    </td>
                    <td className="px-5 py-3 text-slate-600">
                      {patient.country ?? "—"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="rounded-xl border border-dashed border-slate-300 bg-white px-6 py-12 text-center text-sm text-slate-500">
            Henüz hasta eklenmedi. Yukarıdaki formdan ilk hastanızı ekleyin.
          </div>
        )}
      </div>
    </div>
  );
}
