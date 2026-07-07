"use client";

import { useMutation, useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";
import { useEffect, useRef, useState } from "react";

import { Spinner } from "@/components/ui";
import { api } from "@/lib/api";
import type { ChatMessage } from "@/lib/types";

export default function PatientChatPage() {
  const params = useParams();
  const token = params.token as string;

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [seeded, setSeeded] = useState(false);
  const [input, setInput] = useState("");
  const [completed, setCompleted] = useState(false);
  const endRef = useRef<HTMLDivElement>(null);

  const session = useQuery({
    queryKey: ["chat", token],
    queryFn: () => api.getChatSession(token),
    retry: false,
  });

  useEffect(() => {
    if (session.data && !seeded) {
      setMessages(session.data.messages);
      setSeeded(true);
    }
  }, [session.data, seeded]);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, completed]);

  const send = useMutation({
    mutationFn: (text: string) => api.sendChatMessage(token, text),
    onSuccess: (data) => {
      setMessages((prev) => [
        ...prev,
        {
          role: "agent",
          content: data.reply,
          created_at: new Date().toISOString(),
        },
      ]);
      if (data.is_complete) setCompleted(true);
    },
  });

  const handleSend = () => {
    const text = input.trim();
    if (!text || send.isPending) return;
    setMessages((prev) => [
      ...prev,
      { role: "user", content: text, created_at: new Date().toISOString() },
    ]);
    setInput("");
    send.mutate(text);
  };

  if (session.isLoading) {
    return (
      <div className="flex min-h-screen items-center justify-center">
        <Spinner label="Loading…" />
      </div>
    );
  }

  if (session.isError) {
    return (
      <div className="flex min-h-screen items-center justify-center px-6">
        <div className="text-center">
          <p className="text-lg font-semibold text-slate-900">Invalid link</p>
          <p className="mt-1 text-sm text-slate-500">
            This chat link is not valid. Please contact your clinic.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="mx-auto flex min-h-screen max-w-2xl flex-col">
      <header className="border-b border-slate-200 bg-white px-5 py-4">
        <p className="text-lg font-semibold text-slate-900">
          Care<span className="text-teal-600">Pilot</span>
        </p>
        <p className="text-sm text-slate-500">
          Hi {session.data?.patient_name} — how can we help you today?
        </p>
      </header>

      <div className="flex-1 space-y-4 overflow-y-auto px-5 py-6">
        {messages.length === 0 && (
          <div className="rounded-xl border border-slate-200 bg-white p-5 text-sm text-slate-600">
            Welcome! Tell us which treatment you are interested in (for example
            hair transplant or aesthetic surgery) and describe your situation.
            You can write in your own language.
          </div>
        )}

        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex ${
              message.role === "user" ? "justify-end" : "justify-start"
            }`}
          >
            <div
              className={`max-w-[80%] whitespace-pre-wrap rounded-2xl px-4 py-2.5 text-sm ${
                message.role === "user"
                  ? "bg-teal-600 text-white"
                  : "border border-slate-200 bg-white text-slate-800"
              }`}
            >
              {message.content}
            </div>
          </div>
        ))}

        {send.isPending && (
          <div className="flex justify-start">
            <div className="rounded-2xl border border-slate-200 bg-white px-4 py-2.5 text-sm text-slate-400">
              typing…
            </div>
          </div>
        )}

        {completed && (
          <div className="rounded-xl border border-teal-200 bg-teal-50 p-4 text-sm text-teal-800">
            Thank you! Your information has been sent to the clinic team. They
            will review it and contact you soon.
          </div>
        )}

        <div ref={endRef} />
      </div>

      <div className="border-t border-slate-200 bg-white px-5 py-4">
        <div className="flex gap-2">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSend();
            }}
            placeholder="Type your message…"
            className="flex-1 rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 outline-none transition placeholder:text-slate-400 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20"
          />
          <button
            onClick={handleSend}
            disabled={send.isPending || !input.trim()}
            className="rounded-lg bg-teal-600 px-4 py-2.5 text-sm font-medium text-white transition hover:bg-teal-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
