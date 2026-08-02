# 🩺 CarePilot

**Çok dilli ve hafızalı, yapay zeka destekli sağlık turizmi hasta konsiyerj platformu.**

> YZTA (Yapay Zeka ve Teknoloji Akademisi) Bootcamp 2026 — **Grup 153**

[![Canlı Panel](https://img.shields.io/badge/Canl%C4%B1_Panel-Render-46E3B7?logo=render&logoColor=white)](https://carepilot-frontend.onrender.com)
[![Canlı API](https://img.shields.io/badge/Canl%C4%B1_API-Render-46E3B7?logo=render&logoColor=white)](https://carepilot-backend-0xxe.onrender.com/api/v1/health)
[![Swagger](https://img.shields.io/badge/API_Docs-Swagger-85EA2D?logo=swagger&logoColor=black)](https://carepilot-backend-0xxe.onrender.com/docs)
[![Demo Videosu](https://img.shields.io/badge/Demo_Videosu-YouTube-FF0000?logo=youtube&logoColor=white)](https://youtu.be/iCj_6lvJ2_Q)

- **🎬 3 dakikalık demo videosu:** https://youtu.be/iCj_6lvJ2_Q
- **Canlı Panel:** https://carepilot-frontend.onrender.com
- **Canlı API:** https://carepilot-backend-0xxe.onrender.com
- **Etkileşimli API dokümantasyonu:** https://carepilot-backend-0xxe.onrender.com/docs

> Deploy ücretsiz katmanda (Render + Neon) çalışır; servisler bir süre hareketsiz kalınca uyur, ilk istekte ~1 dk soğuk başlangıç olabilir.

---

## 👥 Takım

### Takım Üyeleri

| İsim | Rol | İletişim |
|---|---|---|
| **Can Çorapçıoğlu** | Scrum Master · Product Owner · Developer | [GitHub @cancrpcoglu](https://github.com/cancrpcoglu) |

> Akademi Danışmanı: **Hikmet Topak** · Grup: **153** · Bölüm: **Yapay Zeka ve Veri Bilimi**

---

## 🎯 Ürün

### Ürün İsmi
**CarePilot**

### Ürün Açıklaması
Türkiye, saç ekimi ve estetik cerrahide dünya lideri ülkelerden biridir; her yıl yüz binlerce yabancı hasta bu tedaviler için Türkiye'ye gelir. Ancak bu süreç hâlâ büyük ölçüde manuel ve dağınık yönetilir: dil bariyeri, WhatsApp üzerinden standart olmayan koordinasyon ve ameliyat sonrası takip kaybı.

CarePilot, hasta yolculuğunun başından sonuna kadar refakat eden **çok dilli ve hafızalı bir yapay zeka hasta konsiyerj agent'ı** sunar. Hasta kendi dilinde agent ile görüşür; agent **yapılandırılmış bir ön değerlendirme raporu** çıkarır; klinik bu raporu onaylar; agent ameliyat öncesi/sonrası süreci hafızasında tutarak hastayı yönlendirir.

### Ürün Özellikleri
- 🤖 **AI triage:** Hasta mesajından, Gemini 2.5 Flash + structured output ile yapılandırılmış ön değerlendirme (tedavi alanı, şikayetler, sağlık geçmişi, eksik bilgi, dil tespiti)
- 💬 **Hafızalı hasta sohbeti:** Hasta, kendine özel bir linkten yapay zeka asistanıyla kendi dilinde çok turlu sohbet eder (LangGraph + PostgreSQL hafıza); agent yeterli bilgiyi toplayınca otomatik olarak klinik onayına ön değerlendirme raporu üretir
- 🔗 **Self-servis davet linki + QR:** Klinik tek bir genel link/QR paylaşır; yeni hasta kendi ön kaydını yapıp AI ile sohbet eder, panelde otomatik hasta + rapor belirir (per-hasta link de mevcut)
- 📞 **İletişim yakalama + tek tık ulaşım:** Hasta ön kayıtta telefon/WhatsApp (zorunlu) ve e-posta bırakır; klinik hasta detayından ve rapor kartından **tek tıkla WhatsApp / Ara / E-posta** ile ulaşır — orphan rapor yerine iletişim bilgili nitelikli lead
- 🔒 **KVKK açık rıza:** Ön kayıtta hastadan verilerinin işlenmesi için açık rıza alınır ve zaman damgasıyla saklanır (panelde rozetle görünür)
- 🌍 **Çok dilli:** Hasta herhangi bir dilde yazar; agent dili tespit edip klinik için Türkçe özet üretir
- 🗂 **Hasta yönetimi:** Klinik hastayı düzenler, özel not tutar, siler (soft delete)
- 🔎 **Anlamsal rapor arama:** Klinik doğal dille arar (örn. "diyabetli estetik hastaları"); en alakalı raporlar Gemini embedding + pgvector kosinüs benzerliğiyle sıralanır
- 🏥 **Klinik paneli:** Hasta yönetimi, gelen ön değerlendirmeleri görüntüleme ve onaylama/reddetme
- 📊 **Dönüşüm hunisi:** Panelde ön kayıt → ön değerlendirme üretildi → onaylandı dönüşüm oranları
- ⚙️ **Hesap yönetimi:** Ayarlar sayfasından klinik bilgisi görüntüleme ve kliniği güvenli onayla silme (soft delete; hastalar da cascade silinir)
- 🧠 **Hafızalı yolculuk:** Konuşma ve yolculuk adımları PostgreSQL'de kalıcı tutulur
- 🔐 **Rol bazlı erişim:** JWT ile klinik yöneticisi ve hasta rolleri; klinikler arası veri izolasyonu

### Hedef Kitle
- **B2B:** Saç ekimi ve estetik cerrahi klinikleri (platformu white-label kullanır)
- **B2C:** Türkiye'de tedavi arayan yabancı hastalar (klinik üzerinden agent'a erişir)

### 📌 Product Backlog
Backlog ve sprint takibi bu repoda [**PRODUCT_BACKLOG.md**](./PRODUCT_BACKLOG.md) dosyasında yürütülmektedir. Toplam ~300 puanlık backlog 3 sprint'e (~100 puan/sprint) bölünmüştür.

---

## 🏗 Mimari

```mermaid
flowchart TB
    subgraph render_fe["Render (Canlı)"]
      FE["Next.js Frontend<br/>Klinik Paneli + Hasta Chat"]
    end
    subgraph render_be["Render (Canlı)"]
      BE["FastAPI Backend<br/>router → service → repository"]
    end
    subgraph neon["Neon (Canlı)"]
      DB[("PostgreSQL<br/>+ pgvector")]
    end
    AI["Gemini 2.5 Flash + embedding<br/>LangChain / LangGraph"]

    FE -->|"REST + JWT"| BE
    BE --> DB
    BE -->|"triage + chat + embedding"| AI
```

**Triage akışı (AI ön değerlendirme → klinik onayı):**

```mermaid
sequenceDiagram
    participant K as Klinik Paneli
    participant API as FastAPI
    participant AI as Gemini 2.5 Flash
    participant DB as PostgreSQL

    K->>API: POST /agent/triage (hasta mesajı)
    API->>AI: structured output (TriageAssessment şeması)
    AI-->>API: yapılandırılmış değerlendirme
    API->>DB: Conversation + Message + TriageReport (pending)
    API-->>K: rapor + değerlendirme
    K->>API: POST /triage-reports/{id}/approve
    API->>DB: status = approved
```

**Veritabanı şeması:**

```mermaid
erDiagram
    USERS ||--o| CLINICS : "clinic_id"
    CLINICS ||--o{ PATIENTS : "clinic_id"
    USERS ||--o| PATIENTS : "user_id"
    PATIENTS ||--o{ CONVERSATIONS : ""
    CONVERSATIONS ||--o{ MESSAGES : ""
    PATIENTS ||--o{ TRIAGE_REPORTS : ""
    PATIENTS ||--o{ JOURNEY_STEPS : ""
```

Backend, temiz mimari (clean architecture) ile katmanlıdır: **router → service → repository → model**. Her tablo `created_at`, `updated_at`, `is_deleted` (soft delete) kolonlarını taşır.

---

## 🧰 Teknoloji Yığını

| Katman | Teknoloji |
|---|---|
| Frontend | Next.js 16 (App Router), TypeScript, Tailwind CSS, React Query, Zod |
| Backend | FastAPI, async SQLAlchemy, Alembic |
| Veritabanı | PostgreSQL (+ pgvector) |
| Yapay Zeka | Gemini 2.5 Flash, LangChain + LangGraph (structured output, çok turlu hafızalı agent), gemini-embedding-001 + pgvector (anlamsal arama) |
| Kimlik Doğrulama | JWT (PyJWT + bcrypt) |
| Test & Lint | Pytest (38 test), ruff |
| CI/CD | GitHub Actions |
| Deploy | Render (backend Docker + frontend Node) · Neon (PostgreSQL + pgvector) — tümü ücretsiz katman |

---

## 🖼 Ürün Durumu (Ekran Görüntüleri)

> 🌍 **Çok dilli kanıt — Arapça konuşan hasta ile canlı sohbet:** AI, hastanın dilini otomatik algılayıp uçtan uca Arapça görüşür, gerekli tüm bilgileri toplar ve klinik için yapılandırılmış rapor üretir. (Canlı ortamda gerçek bir konuşma.)

![Arapça hasta sohbeti](docs/screenshots/17-patient-chat-arabic.png)

| Açılış sayfası | Klinik paneli |
|---|---|
| ![Açılış](docs/screenshots/01-landing.png) | ![Panel](docs/screenshots/03-dashboard.png) |

| Hasta yönetimi (çok dilli) | Canlı API dokümantasyonu |
|---|---|
| ![Hastalar](docs/screenshots/04-patients.png) | ![API](docs/screenshots/05-api-docs.png) |

| Hasta AI sohbeti (hafızalı, çok dilli) | Hasta detayı + sohbet linki |
|---|---|
| ![Hasta sohbeti](docs/screenshots/09-patient-chat.png) | ![Hasta detayı](docs/screenshots/08-patient-detail.png) |

| Self-servis davet linki + QR (panel) | Hasta yönetimi (düzenle / not / sil) |
|---|---|
| ![Davet linki](docs/screenshots/10-dashboard-intake.png) | ![Hasta yönetimi](docs/screenshots/11-patient-manage.png) |

| AI ön değerlendirme (hasta detayı) | Rapor onay ekranı + tek tık iletişim |
|---|---|
| ![AI triage](docs/screenshots/06-patient-triage.png) | ![Raporlar](docs/screenshots/07-reports.png) |

| Dönüşüm hunisi (panel) | KVKK rıza + iletişim yakalama (ön kayıt) |
|---|---|
| ![Dönüşüm hunisi](docs/screenshots/13-dashboard-funnel.png) | ![KVKK rıza](docs/screenshots/14-intake-consent.png) |

| Tek tık iletişim + KVKK rozeti (hasta detayı) | Klinik silme — Tehlikeli bölge (Ayarlar) |
|---|---|
| ![İletişim aksiyonları](docs/screenshots/15-patient-contact.png) | ![Ayarlar tehlikeli bölge](docs/screenshots/16-settings-danger.png) |

---

## 🔄 Sprint 1 — Tamamlandı (19 Haziran – 5 Temmuz)

### Sprint Notları
Bu sprintte projenin **çalışan iskeleti canlıya alındı**: FastAPI backend, JWT kimlik doğrulama, klinik/hasta/triage/yolculuk API'leri, ilk yapay zeka (Gemini) entegrasyonu, CI/CD ve Railway'e deploy. Backlog önceliklendirmesinde "önce çalışan uçtan uca bir dikey dilim" prensibi izlendi: kayıt → klinik → hasta → AI triage → onay zinciri baştan sona çalışır hale getirildi.

- **Sprint içinde tamamlanması tahmin edilen puan:** 100
- **Puan tamamlama mantığı:** Toplam ~300 puanlık ürün backlog'u 3 sprint'e bölündü; her sprint için ~100 puanlık iş hedeflendi. Sprint 1'de altyapı + ilk AI entegrasyonu bu bütçeyle tamamlandı.

### Daily Scrum
Proje tek geliştirici (solo) tarafından yürütüldüğü için günlük ilerleme; **conventional commit geçmişi** ve **sprint logları** üzerinden takip edildi. Akademi danışmanı ile iletişim grup kanalı üzerinden sağlandı.

### Sprint Board
Sprint 1 sonu board durumu:

| ✅ Done | 🔬 Test | 📋 To Do (Sprint 2) |
|---|---|---|
| Backend iskeleti (clean architecture) | 22/22 test geçti | Çok turlu hafızalı agent (LangGraph) |
| JWT auth (register/login/me) + rol-guard | ruff lint temiz | Hasta arayüzü (agent sohbeti) |
| Klinik/hasta/triage/yolculuk CRUD | CI (GitHub Actions) yeşil | Klinik panelinde rapor detay/onay ekranı |
| AI triage (Gemini 2.5 Flash) | Canlı uçtan uca doğrulama | Embedding tabanlı klinik eşleştirme |
| Alembic migration'ları (3) | | |
| Railway'e canlı deploy | | |
| Next.js klinik paneli (temel ekranlar) | | |

### Ürün Durumu
Yukarıdaki [Ekran Görüntüleri](#-ürün-durumu-ekran-görüntüleri) bölümüne bakınız. Backend ve frontend canlıda çalışır durumdadır.

### Sprint Review
**Ne çalışıyor:** Tüm backend canlıda. Auth, klinik/hasta yönetimi ve AI triage uçtan uca çalışıyor — gerçek Gemini çağrısıyla hasta mesajından yapılandırılmış rapor üretilip klinik onayına düşüyor. Frontend klinik paneli (kayıt/giriş/panel/hastalar) canlı backend'e bağlı. 22/22 test geçiyor, ruff temiz.

**Sprint Review katılımcıları:** Can Çorapçıoğlu (geliştirici).

**Bir sonraki faz için belirlenenler:** Çok turlu hafızalı agent, hasta arayüzü, klinik panelinde triage rapor detay/onay ekranları.

### Sprint Retrospective
- **İyi giden:** Plana kıyasla önde gidildi — deploy (Sprint 3 hedefiydi) ve frontend başlangıcı (Sprint 2) erken tamamlandı. Her adım testle ve canlı ortamda doğrulandı.
- **Geliştirilmesi gereken:** AI katmanı şu an tek turlu; hafızalı, çok turlu agent'a geçilmeli.
- **Sonraki sprint için aksiyon:** LangGraph ile hafızalı agent, hasta arayüzü ve klinik panelinde rapor onay ekranlarına odaklanmak.

---

## 🔄 Sprint 2 — Tamamlandı (6 Temmuz – 19 Temmuz)

### Sprint Notları
Bu sprintte ürünün **yapay zeka çekirdeği ve uçtan uca kullanıcı deneyimi** tamamlandı: tek seferlik triage yerine **çok turlu, hafızalı bir agent** (LangGraph) devreye alındı — hasta kendi dilinde sohbet ederek ön değerlendirmesini oluşturuyor. Hasta chat arayüzü, klinik rapor onay ekranları, self-servis davet linki (+QR) ve **embedding tabanlı anlamsal arama** eklendi.

- **Sprint içinde tamamlanması tahmin edilen puan:** 100
- **Puan tamamlama mantığı:** ~300 puanlık backlog'un ikinci dilimi (~100 puan) — hafızalı agent, hasta/klinik arayüzleri ve embedding eşleştirme bu sprintte tamamlandı.

### Daily Scrum
Solo geliştirici; günlük ilerleme conventional commit geçmişi ve sprint logları üzerinden takip edildi. Her özellik ayrı PR olarak açılıp gözden geçirilerek merge edildi.

### Sprint Board
Sprint 2 sonu board durumu:

| ✅ Done | 🔬 Test | 📋 To Do (Sprint 3) |
|---|---|---|
| Çok turlu hafızalı agent (LangGraph + PostgreSQL memory) | 34/34 test geçti | Ücretsiz hosting'e göç (canlıya alma) |
| Hasta AI sohbet arayüzü (`/chat/[token]`) | ruff lint temiz | Performans optimizasyonu |
| Klinik panelinde rapor detay + onay/ret ekranları | CI yeşil | 3 dakikalık demo videosu |
| Self-servis davet linki + QR + WhatsApp paylaşımı | Yerel + (Railway'de) canlı doğrulama | Son dokümantasyon |
| Hasta yönetimi (düzenle / not / silme) | | |
| Embedding tabanlı anlamsal arama (Gemini + pgvector) | | |

### Ürün Durumu
Yukarıdaki [Ekran Görüntüleri](#-ürün-durumu-ekran-görüntüleri) bölümündeki hasta sohbeti, self-servis davet ve hasta yönetimi ekranlarına bakınız.

### Sprint Review
**Ne çalışıyor:** Çok turlu hafızalı agent, hastayla kendi dilinde sohbet edip zorunlu tüm bilgileri toplayınca yapılandırılmış rapor üretiyor; klinik bu raporu panelde görüp onaylıyor. Self-servis davet linkiyle hastalar kendi kaydını yapıyor. Klinik doğal dille **anlamsal arama** yapıp (Gemini embedding + pgvector kosinüs benzerliği) en alakalı hasta raporlarını buluyor. 34/34 test geçiyor, ruff temiz.

**Sprint Review katılımcıları:** Can Çorapçıoğlu (geliştirici).

**Bir sonraki faz için belirlenenler:** Ürünü tekrar canlıya almak (Railway ücretsiz trial'ı dolduğu için ücretsiz bir alternatife göç), performans ve 3 dakikalık demo hazırlığı.

### Sprint Retrospective
- **İyi giden:** Sprint 2 kapsamının ötesine geçildi — self-servis davet, hasta yönetimi ve WhatsApp paylaşımı da eklendi. AI davranışı gerçek senaryolarla test edilip iyileştirildi (agent artık zorunlu bilgileri toplamadan sohbeti bitirmiyor).
- **Geliştirilmesi gereken:** Railway ücretsiz trial'ı doldu ve canlı ortam düştü; hosting sürdürülebilir/ücretsiz bir platforma taşınmalı.
- **Sonraki sprint için aksiyon:** Ücretsiz hosting'e göç (Neon Postgres + Render/Koyeb) veya Railway planı; ardından demo videosu ve son dokümantasyon.

## 🔄 Sprint 3 — Tamamlandı (20 Temmuz – 2 Ağustos)

### Sprint Notları
Bu sprintte ürün **tamamen ücretsiz bir yığına canlıya alındı** ve sağlık turizmi akışını olgunlaştıran özelliklerle tamamlandı. Railway ücretsiz trial'ı dolunca hosting **Neon (PostgreSQL + pgvector 0.8.1) + Render (backend Docker + frontend Node)** yığınına taşındı — geçiş kod değişikliği gerektirmedi (`config.py`, `DATABASE_URL`'i asyncpg + SSL'e otomatik normalize eder). Ardından şu özellikler eklendi: **hasta iletişim yakalama + tek tık ulaşım, KVKK açık rıza, hasta tamamlama ekranı, dashboard dönüşüm hunisi ve klinik hesabı silme.**

Canlı: **[Panel](https://carepilot-frontend.onrender.com)** · **[API / Swagger](https://carepilot-backend-0xxe.onrender.com/docs)**

- **Sprint içinde tamamlanması tahmin edilen puan:** ~100
- **Puan tamamlama mantığı:** Backlog'un son dilimi — canlıya alma, hasta akışı olgunlaştırma (iletişim/KVKK/huni), hesap yönetimi, performans, demo ve dokümantasyon.

### Daily Scrum
Solo geliştirici; ilerleme conventional commit geçmişi ve sprint logları üzerinden takip edildi. Her özellik ayrı bir PR olarak açılıp gözden geçirilerek merge edildi.

### Sprint Board
| ✅ Done | 📋 Kullanıcı adımı |
|---|---|
| **Neon + Render'e canlı deploy** (pgvector 0.8.1) — [render.yaml](./render.yaml) + [DEPLOYMENT.md](./DEPLOYMENT.md) | 3 dakikalık demo videosunun kaydı |
| **Hasta iletişim yakalama** (telefon/WhatsApp/e-posta) + tek tık WhatsApp/Ara/E-posta | |
| **KVKK açık rıza** (zorunlu onay + `consent_at` damgası + panel rozeti) | |
| **Hasta tamamlama ekranı** (`is_complete` kalıcı; sohbet bitince net kapanış) | |
| **Dashboard dönüşüm hunisi** (ön kayıt → rapor → onay) | |
| **Klinik silme** (soft-delete + hastaları cascade + onay güvenliği) | |
| Performans (async I/O, connection pooling, FK indeksleri, prod build) | |
| 3 dk demo senaryosu ([DEMO_SCRIPT.md](./DEMO_SCRIPT.md)) + dokümantasyon | |
| **38/38 test** geçti · ruff temiz · CI yeşil | |

### Ürün Durumu
Ürün **canlıda ve uçtan uca doğrulandı** (Render + Neon): giriş, self-servis ön kayıt (KVKK rıza + iletişim yakalama), hafızalı çok dilli AI sohbet, tamamlama ekranı, rapor onayı, anlamsal arama, dönüşüm hunisi ve klinik silme çalışıyor. Demo klinik ve 6 çok uluslu hasta (Türkiye/İngiltere/Almanya/BAE) seed'lendi. Güncel ekranlar için yukarıdaki [Ekran Görüntüleri](#-ürün-durumu-ekran-görüntüleri) bölümüne bakınız.

### Sprint Review
**Ne çalışıyor:** Ürünün tamamı canlıda uçtan uca çalışıyor. Hasta kendi dilinde AI ile sohbet edip KVKK onayı ve iletişim bilgisiyle ön kayıt yapıyor; agent zorunlu bilgileri toplayınca yapılandırılmış rapor üretiyor; klinik raporu onaylayıp **tek tıkla WhatsApp/telefon/e-posta** ile hastaya ulaşıyor; anlamsal arama ve dönüşüm hunisi panelde çalışıyor. Jüri kriteri olan "canlıya alınmış" **fazlasıyla karşılanıyor — yalnızca alınabilir değil, çalışan bir link mevcut.** 38/38 test, ruff temiz, CI yeşil.

**Sprint Review katılımcıları:** Can Çorapçıoğlu (geliştirici).

### Sprint Retrospective
- **İyi giden:** Platformdan bağımsız mimari sayesinde hosting göçü kod değişikliği gerektirmedi; ürün canlıda uçtan uca doğrulandı. Sprint kapsamının ötesine geçilerek iletişim yakalama, KVKK rıza, dönüşüm hunisi ve klinik silme de eklendi.
- **Geliştirilmesi gereken:** Ücretsiz katmanın (Render) uyku/soğuk başlangıç sınırı demo öncesi "uyandırma" gerektiriyor.
- **Sonuç:** Proje bootcamp teslimine hazır — **canlı**, dokümante edilmiş, test edilmiş (38/38) bir ürün.

---

## ⚙️ Kurulum

Ayrıntılı backend kurulumu için [backend/README.md](./backend/README.md), ürün gereksinimleri için [PRD.md](./PRD.md).

```bash
# Backend
cd backend
python -m venv .venv && source .venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env            # GEMINI_API_KEY ve diğer değerleri doldur
docker compose up -d db         # (kök dizinden) PostgreSQL
alembic upgrade head
uvicorn app.main:app --reload   # http://localhost:8000/docs

# Frontend
cd frontend
npm install
npm run dev                      # http://localhost:3000
```

---

## ⚖️ Etik ve Yasal Sınırlar

> **CarePilot'un AI agent'ı kesinlikle tıbbi tanı veya tedavi tavsiyesi vermez.**

Agent yalnızca bilgi toplar, yapılandırır ve klinik onayına sunar; nihai tıbbi karar her zaman yetkili sağlık profesyoneline aittir. Bu sınır sistem promptunda ve arayüzde açıkça belirtilir. Hasta sağlık verisi KVKK kapsamında özel nitelikli kişisel veri sayılır ve buna uygun ele alınır.
