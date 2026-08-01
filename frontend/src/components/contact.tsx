import type { ReactNode } from "react";

/** wa.me yalnızca rakam ister (+, boşluk, tire olmadan). */
function toWhatsApp(phone: string): string {
  return phone.replace(/\D/g, "");
}

function ActionLink({
  href,
  external,
  children,
}: {
  href: string;
  external?: boolean;
  children: ReactNode;
}) {
  return (
    <a
      href={href}
      {...(external ? { target: "_blank", rel: "noopener noreferrer" } : {})}
      className="inline-flex items-center gap-1.5 rounded-lg border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
    >
      {children}
    </a>
  );
}

/**
 * Hasta iletişim aksiyonları: klinik tek tıkla WhatsApp / telefon / e-posta ile
 * hastaya ulaşır. Hiç bilgi yoksa hiçbir şey render etmez.
 */
export function ContactActions({
  phone,
  email,
  className,
}: {
  phone?: string | null;
  email?: string | null;
  className?: string;
}) {
  if (!phone && !email) return null;
  const digits = phone ? toWhatsApp(phone) : "";

  return (
    <div className={`flex flex-wrap gap-2 ${className ?? ""}`}>
      {digits && (
        <ActionLink href={`https://wa.me/${digits}`} external>
          <span className="text-emerald-600">●</span> WhatsApp
        </ActionLink>
      )}
      {phone && <ActionLink href={`tel:${phone}`}>Ara</ActionLink>}
      {email && <ActionLink href={`mailto:${email}`}>E-posta</ActionLink>}
    </div>
  );
}
