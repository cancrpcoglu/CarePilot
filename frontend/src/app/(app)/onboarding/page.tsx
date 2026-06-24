"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Alert, Button, Card, Input, Label } from "@/components/ui";
import { api, ApiError } from "@/lib/api";

export default function OnboardingPage() {
  const router = useRouter();
  const queryClient = useQueryClient();
  const [form, setForm] = useState({ name: "", country: "" });
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: () =>
      api.createClinic({
        name: form.name,
        country: form.country || undefined,
      }),
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["me"] });
      router.replace("/dashboard");
    },
    onError: (err) =>
      setError(err instanceof ApiError ? err.message : "Klinik oluşturulamadı."),
  });

  return (
    <div className="mx-auto max-w-md py-8">
      <Card>
        <h1 className="text-xl font-semibold text-slate-900">
          Kliniğinizi oluşturun
        </h1>
        <p className="mt-1 text-sm text-slate-500">
          Başlamadan önce klinik profilinizi tanımlayın.
        </p>

        <form
          className="mt-6 space-y-4"
          onSubmit={(e) => {
            e.preventDefault();
            setError(null);
            if (form.name.trim().length < 2) {
              setError("Lütfen geçerli bir klinik adı girin.");
              return;
            }
            mutation.mutate();
          }}
        >
          <div>
            <Label htmlFor="name">Klinik adı</Label>
            <Input
              id="name"
              value={form.name}
              onChange={(e) => setForm({ ...form, name: e.target.value })}
              placeholder="Estetik & Saç Ekim Merkezi"
            />
          </div>
          <div>
            <Label htmlFor="country">Ülke (opsiyonel)</Label>
            <Input
              id="country"
              value={form.country}
              onChange={(e) => setForm({ ...form, country: e.target.value })}
              placeholder="Türkiye"
            />
          </div>

          {error && <Alert message={error} />}

          <Button type="submit" className="w-full" disabled={mutation.isPending}>
            {mutation.isPending ? "Oluşturuluyor…" : "Kliniği oluştur"}
          </Button>
        </form>
      </Card>
    </div>
  );
}
