"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useParams, useRouter } from "next/navigation";
import { useState } from "react";

import { Alert, Button, Card, Input, Label, Spinner } from "@/components/ui";
import { api, ApiError } from "@/lib/api";

export default function IntakePage() {
  const params = useParams();
  const router = useRouter();
  const token = params.token as string;

  const [name, setName] = useState("");
  const [error, setError] = useState<string | null>(null);

  const info = useQuery({
    queryKey: ["intake", token],
    queryFn: () => api.getIntakeInfo(token),
    retry: false,
  });

  const start = useMutation({
    mutationFn: () => api.startIntake(token, name.trim()),
    onSuccess: (data) => router.replace(`/chat/${data.access_token}`),
    onError: (err) =>
      setError(err instanceof ApiError ? err.message : "Something went wrong."),
  });

  if (info.isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner label="Loading…" />
      </div>
    );
  }

  if (info.isError) {
    return (
      <div className="flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <p className="text-lg font-semibold text-slate-900">Invalid link</p>
          <p className="mt-1 text-sm text-slate-500">
            This invitation link is not valid. Please contact the clinic.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen items-center justify-center px-6 py-12">
      <div className="w-full max-w-md">
        <p className="mb-6 text-center text-lg font-semibold text-slate-900">
          Care<span className="text-teal-600">Pilot</span>
        </p>
        <Card>
          <h1 className="text-xl font-semibold text-slate-900">
            Welcome to {info.data?.clinic_name}
          </h1>
          <p className="mt-1 text-sm text-slate-500">
            Start your free pre-assessment with our AI assistant. It only takes a
            few minutes and you can chat in your own language.
          </p>

          <form
            className="mt-6 space-y-4"
            onSubmit={(e) => {
              e.preventDefault();
              setError(null);
              if (name.trim().length < 2) {
                setError("Please enter your name.");
                return;
              }
              start.mutate();
            }}
          >
            <div>
              <Label htmlFor="name">Your name</Label>
              <Input
                id="name"
                value={name}
                onChange={(e) => setName(e.target.value)}
                placeholder="Your full name"
              />
            </div>

            {error && <Alert message={error} />}

            <Button type="submit" className="w-full" disabled={start.isPending}>
              {start.isPending ? "Starting…" : "Start assessment"}
            </Button>
          </form>
        </Card>
      </div>
    </div>
  );
}
