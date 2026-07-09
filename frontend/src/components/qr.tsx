"use client";

import { QRCodeSVG } from "qrcode.react";

export function QrCode({ value, size = 148 }: { value: string; size?: number }) {
  if (!value) return null;
  return (
    <div className="inline-block rounded-lg border border-slate-200 bg-white p-3">
      <QRCodeSVG value={value} size={size} level="M" />
    </div>
  );
}
