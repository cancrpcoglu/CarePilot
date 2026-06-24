"use client";

import { useMutation } from "@tanstack/react-query";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { z } from "zod";

import { Alert, Button, Card, Input, Label } from "@/components/ui";
import { api, ApiError } from "@/lib/api";
import { setToken } from "@/lib/auth";

const schema = z.object({
  full_name: z.string().min(2, "Lütfen klinik/yetkili adını girin."),
  email: z.string().email("Geçerli bir e-posta girin."),
  password: z.string().min(8, "Parola en az 8 karakter olmalı."),
});

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ full_name: "", email: "", password: "" });
  const [error, setError] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: async () => {
      const parsed = schema.safeParse(form);
      if (!parsed.success) {
        throw new Error(parsed.error.issues[0].message);
      }
      await api.register(parsed.data);
      const token = await api.login(parsed.data.email, parsed.data.password);
      setToken(token.access_token);
    },
    onSuccess: () => router.replace("/onboarding"),
    onError: (err) =>
      setError(
        err instanceof ApiError || err instanceof Error
          ? err.message
          : "Kayıt başarısız.",
      ),
  });

  return (
    <div className="flex min-h-screen items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        <Link href="/" className="mb-6 block text-center text-lg font-semibold">
          Care<span className="text-teal-600">Pilot</span>
        </Link>
        <Card>
          <h1 className="text-xl font-semibold text-slate-900">Klinik kaydı</h1>
          <p className="mt-1 text-sm text-slate-500">
            Kliniğiniz için bir yönetici hesabı oluşturun.
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
              <Label htmlFor="full_name">Yetkili / klinik adı</Label>
              <Input
                id="full_name"
                value={form.full_name}
                onChange={(e) => setForm({ ...form, full_name: e.target.value })}
                placeholder="Dr. Ayşe Yılmaz"
              />
            </div>
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
                placeholder="En az 8 karakter"
              />
            </div>

            {error && <Alert message={error} />}

            <Button type="submit" className="w-full" disabled={mutation.isPending}>
              {mutation.isPending ? "Hesap oluşturuluyor…" : "Hesap oluştur"}
            </Button>
          </form>

          <p className="mt-6 text-center text-sm text-slate-500">
            Zaten hesabınız var mı?{" "}
            <Link href="/login" className="font-medium text-teal-600 hover:underline">
              Giriş yap
            </Link>
          </p>
        </Card>
      </div>
    </div>
  );
}
