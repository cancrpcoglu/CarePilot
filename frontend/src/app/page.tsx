import Link from "next/link";

const features = [
  {
    title: "Çok dilli ön değerlendirme",
    description:
      "Hasta kendi dilinde görüşür, yapay zeka yapılandırılmış bir ön değerlendirme raporu çıkarır.",
  },
  {
    title: "Hafızalı hasta yolculuğu",
    description:
      "Ameliyat öncesinden sonrasına kadar tüm süreç tek noktadan, hafızalı şekilde takip edilir.",
  },
  {
    title: "Klinik onay akışı",
    description:
      "Klinikler gelen ön değerlendirmeleri görüntüler, onaylar ve hastayı yönlendirir.",
  },
];

export default function LandingPage() {
  return (
    <div className="min-h-screen">
      <header className="mx-auto flex max-w-5xl items-center justify-between px-6 py-5">
        <span className="text-lg font-semibold text-slate-900">
          Care<span className="text-teal-600">Pilot</span>
        </span>
        <div className="flex items-center gap-3">
          <Link
            href="/login"
            className="rounded-lg px-4 py-2 text-sm font-medium text-slate-600 transition hover:bg-slate-100"
          >
            Giriş yap
          </Link>
          <Link
            href="/register"
            className="rounded-lg bg-teal-600 px-4 py-2 text-sm font-medium text-white transition hover:bg-teal-700"
          >
            Klinik kaydı
          </Link>
        </div>
      </header>

      <main className="mx-auto max-w-5xl px-6">
        <section className="py-16 sm:py-24">
          <p className="mb-4 inline-block rounded-full bg-teal-50 px-3 py-1 text-sm font-medium text-teal-700">
            Sağlık turizmi için yapay zeka konsiyerji
          </p>
          <h1 className="max-w-3xl text-4xl font-semibold leading-tight tracking-tight text-slate-900 sm:text-5xl">
            Yabancı hastalarınızı, ilk görüşmeden ameliyat sonrasına kadar tek
            platformda yönetin.
          </h1>
          <p className="mt-6 max-w-2xl text-lg text-slate-600">
            CarePilot; saç ekimi ve estetik cerrahi klinikleri için çok dilli,
            hafızalı bir yapay zeka hasta konsiyerj platformudur. Dil bariyerini
            kaldırır, ön değerlendirmeyi standartlaştırır, takibi otomatikleştirir.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link
              href="/register"
              className="rounded-lg bg-teal-600 px-5 py-3 text-sm font-medium text-white transition hover:bg-teal-700"
            >
              Kliniğinizi kaydedin
            </Link>
            <Link
              href="/login"
              className="rounded-lg border border-slate-300 px-5 py-3 text-sm font-medium text-slate-700 transition hover:bg-slate-50"
            >
              Giriş yap
            </Link>
          </div>
        </section>

        <section className="grid gap-5 pb-24 sm:grid-cols-3">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="rounded-xl border border-slate-200 bg-white p-6"
            >
              <h3 className="text-base font-semibold text-slate-900">
                {feature.title}
              </h3>
              <p className="mt-2 text-sm leading-relaxed text-slate-600">
                {feature.description}
              </p>
            </div>
          ))}
        </section>
      </main>
    </div>
  );
}
