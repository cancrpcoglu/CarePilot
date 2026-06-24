"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import { clearToken, getToken } from "@/lib/auth";

const navItems = [
  { href: "/dashboard", label: "Panel" },
  { href: "/patients", label: "Hastalar" },
];

export default function AppLayout({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname();
  const [token, setTokenState] = useState<string | null | undefined>(undefined);

  useEffect(() => {
    setTokenState(getToken());
  }, []);

  const { data: me, isLoading, isError } = useQuery({
    queryKey: ["me"],
    queryFn: api.me,
    enabled: !!token,
  });

  useEffect(() => {
    if (token === null) router.replace("/login");
  }, [token, router]);

  useEffect(() => {
    if (isError) {
      clearToken();
      router.replace("/login");
    }
  }, [isError, router]);

  useEffect(() => {
    if (!me) return;
    if (!me.clinic_id && pathname !== "/onboarding") router.replace("/onboarding");
    if (me.clinic_id && pathname === "/onboarding") router.replace("/dashboard");
  }, [me, pathname, router]);

  if (token === undefined || isLoading || !me) {
    return <Spinner label="Yükleniyor…" />;
  }

  const logout = () => {
    clearToken();
    router.replace("/login");
  };

  return (
    <div className="min-h-screen">
      <header className="border-b border-slate-200 bg-white">
        <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-3">
          <div className="flex items-center gap-8">
            <Link href="/dashboard" className="text-lg font-semibold text-slate-900">
              Care<span className="text-teal-600">Pilot</span>
            </Link>
            {me.clinic_id && (
              <nav className="flex items-center gap-1">
                {navItems.map((item) => (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={`rounded-lg px-3 py-1.5 text-sm font-medium transition ${
                      pathname === item.href
                        ? "bg-teal-50 text-teal-700"
                        : "text-slate-600 hover:bg-slate-100"
                    }`}
                  >
                    {item.label}
                  </Link>
                ))}
              </nav>
            )}
          </div>
          <div className="flex items-center gap-3">
            <span className="hidden text-sm text-slate-500 sm:inline">
              {me.email}
            </span>
            <button
              onClick={logout}
              className="rounded-lg px-3 py-1.5 text-sm font-medium text-slate-600 transition hover:bg-slate-100"
            >
              Çıkış
            </button>
          </div>
        </div>
      </header>
      <main className="mx-auto max-w-5xl px-6 py-8">{children}</main>
    </div>
  );
}
