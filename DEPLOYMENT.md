# 🚀 CarePilot — Canlıya Alma (Deployment) Rehberi

CarePilot tamamen **ücretsiz** bir yığınla canlıya alınabilir (kredi kartı gerekmez):

- **Veritabanı:** [Neon](https://neon.tech) — ücretsiz PostgreSQL, **pgvector destekli**, süresiz
- **Backend + Frontend:** [Render](https://render.com) — ücretsiz web servisleri (Blueprint ile)

> Not: Proje daha önce Railway'de canlıydı; Railway ücretsiz trial'ı dolduğu için
> aşağıdaki ücretsiz ve sürdürülebilir yığına geçiş belgelenmiştir. Kod tarafı
> platformdan bağımsızdır (`config.py`, `DATABASE_URL`'i otomatik asyncpg'ye çevirir).

---

## 1) Veritabanı — Neon (~3 dk)

1. [neon.tech](https://neon.tech) → ücretsiz hesap aç (GitHub ile giriş yapılabilir).
2. **Create project** → bir isim ver (örn. `carepilot`), bölge Frankfurt.
3. Oluşan **connection string**'i kopyala (biçim: `postgresql://user:pass@...neon.tech/db?sslmode=require`).
4. pgvector Neon'da hazırdır; migration ilk deploy'da `CREATE EXTENSION vector` çalıştırır.

## 2) Backend + Frontend — Render (~10 dk)

1. [render.com](https://render.com) → ücretsiz hesap aç, GitHub'ı bağla.
2. **New > Blueprint** → CarePilot repo'sunu seç. Render kökteki [`render.yaml`](./render.yaml)'i okur ve iki servis oluşturur.
3. Aşağıdaki ortam değişkenlerini gir (`sync: false` olanlar):

   **carepilot-backend:**
   | Değişken | Değer |
   |---|---|
   | `DATABASE_URL` | Neon connection string (1. adım) |
   | `GEMINI_API_KEY` | [Google AI Studio](https://aistudio.google.com/apikey) key'i |
   | `BACKEND_CORS_ORIGINS` | Frontend URL'i, JSON dizi (aşağıya bak) |

   **carepilot-frontend:**
   | Değişken | Değer |
   |---|---|
   | `NEXT_PUBLIC_API_URL` | Backend URL'i (örn. `https://carepilot-backend.onrender.com`) |

4. **İlk deploy sırası (URL'ler birbirine bağlı):**
   - Backend'i deploy et → URL'ini al (örn. `https://carepilot-backend.onrender.com`).
   - Frontend'in `NEXT_PUBLIC_API_URL`'ini bu backend URL'i yap → frontend'i deploy et → URL'ini al.
   - Backend'in `BACKEND_CORS_ORIGINS`'ini `["https://<frontend-url>"]` yap → backend'i **yeniden deploy** et.

5. Backend başlangıçta otomatik `alembic upgrade head` çalıştırır (tüm tablolar + pgvector).

## 3) Doğrulama

- Backend: `https://<backend-url>/api/v1/health` → `{"status":"ok"}`
- Swagger: `https://<backend-url>/docs`
- Frontend: `https://<frontend-url>` → kayıt ol, hasta ekle, davet linki / chat / arama dene.

---

## Notlar & İpuçları

- **Render ücretsiz tier:** servisler 15 dk hareketsizlikte uykuya geçer; ilk istek ~1 dk soğuk başlangıç ister. Demo öncesi bir kez uyandırın.
- **Frontend build belleği:** Render free tier'da Next.js build bellek sınırına takılırsa, frontend'i [Cloudflare Pages](https://pages.cloudflare.com) ile de yayınlayabilirsiniz (alternatif).
- **Gizli anahtarlar** yalnızca Render/Neon panolarında tutulur; repoda `.env` yoktur (`.gitignore`).
- **Yerel çalıştırma** için [README.md](./README.md#-kurulum) kurulum bölümüne bakın.
