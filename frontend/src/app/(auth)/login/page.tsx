"use client";

import { useMutation } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";

import { Alert, Button, Card, Input, Label } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import { setToken } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: async () => {
      const token = await api.login(form.email, form.password);
      setToken(token.access_token);
    },
    onSuccess: () => router.replace("/dashboard"),
    onError: (err) =>
      setError(err instanceof ApiError ? err.message : "Giriş başarısız."),
  });

  return (
    <div className="flex min-h-screen items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        <Link href="/" className="mb-6 block text-center text-lg font-semibold">
          Care<span className="text-teal-600">Pilot</span>
        </Link>
        <Card>
          <h1 className="text-xl font-semibold text-slate-900">Giriş yap</h1>
          <p className="mt-1 text-sm text-slate-500">
            Klinik yönetici hesabınızla devam edin.
          </p>

          <form
            className="mt-6 space-y-4"
            onSubmit={(e) => {
              e.preventDefault();
              setError(null);
              mutation.mutate();
            }}
          >
            <div>
              <Label htmlFor="email">E-posta</Label>
              <Input
                id="email"
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
                placeholder="klinik@ornek.com"
              />
            </div>
            <div>
              <Label htmlFor="password">Parola</Label>
              <Input
                id="password"
                type="password"
                value={form.password}
                onChange={(e) => setForm({ ...form, password: e.target.value })}
                placeholder="Parolanız"
              />
            </div>

            {error && <Alert message={error} />}

            <Button type="submit" className="w-full" disabled={mutation.isPending}>
              {mutation.isPending ? "Giriş yapılıyor…" : "Giriş yap"}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-slate-500">
            Kliniğiniz yok mu?{" "}
            <Link
              href="/register"
              className="font-medium text-teal-600 hover:underline"
            >
              Klinik kaydı oluştur
            </Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
