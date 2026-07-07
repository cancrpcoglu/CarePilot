# 🩺 CarePilot

**Çok dilli ve hafızalı, yapay zeka destekli sağlık turizmi hasta konsiyerj platformu.**

> YZTA (Yapay Zeka ve Teknoloji Akademisi) Bootcamp 2026 — **Grup 153**

[![Canlı API](https://img.shields.io/badge/Canl%C4%B1_API-Railway-0B0D0E?logo=railway)](https://carepilot-backend-production.up.railway.app/api/v1/health)
[![Swagger](https://img.shields.io/badge/API_Docs-Swagger-85EA2D?logo=swagger&logoColor=black)](https://carepilot-backend-production.up.railway.app/docs)

- **Canlı API:** https://carepilot-backend-production.up.railway.app
- **Etkileşimli API dokümantasyonu:** https://carepilot-backend-production.up.railway.app/docs

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
- 🌍 **Çok dilli:** Hasta herhangi bir dilde yazar; agent dili tespit edip klinik için Türkçe özet üretir
- 🏥 **Klinik paneli:** Hasta yönetimi, gelen ön değerlendirmeleri görüntüleme ve onaylama/reddetme
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
    subgraph client["İstemci"]
      FE["Next.js Frontend<br/>Klinik Paneli"]
    end
    subgraph railway["Railway (Canlı)"]
      BE["FastAPI Backend<br/>router → service → repository"]
      DB[("PostgreSQL")]
    end
    AI["Gemini 2.5 Flash<br/>LangChain structured output"]

    FE -->|"REST + JWT"| BE
    BE --> DB
    BE -->|"triage (function calling)"| AI
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
| Yapay Zeka | Gemini 2.5 Flash, LangChain (structured output / function calling) |
| Kimlik Doğrulama | JWT (PyJWT + bcrypt) |
| Test & Lint | Pytest, ruff |
| CI/CD | GitHub Actions |
| Deploy | Railway (backend + PostgreSQL) |

---

## 🖼 Ürün Durumu (Ekran Görüntüleri)

| Açılış sayfası | Klinik paneli |
|---|---|
| ![Açılış](docs/screenshots/01-landing.png) | ![Panel](docs/screenshots/03-dashboard.png) |

| Hasta yönetimi (çok dilli) | Canlı API dokümantasyonu |
|---|---|
| ![Hastalar](docs/screenshots/04-patients.png) | ![API](docs/screenshots/05-api-docs.png) |

| AI ön değerlendirme (hasta detayı) | Rapor onay ekranı |
|---|---|
| ![AI triage](docs/screenshots/06-patient-triage.png) | ![Raporlar](docs/screenshots/07-reports.png) |

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

## 🔄 Sprint 2 — Planlanan (6 Temmuz – 19 Temmuz)
- Çok turlu, hafızalı triage agent (LangGraph + PostgreSQL conversation memory)
- Hasta arayüzü: agent ile sohbet ekranı
- Klinik panelinde triage rapor listesi + detay + onay/ret ekranları
- Embedding tabanlı klinik/uzman yönlendirme (pgvector)

## 🔄 Sprint 3 — Planlanan (20 Temmuz – 2 Ağustos)
- Performans optimizasyonu ve son rötuşlar
- 3 dakikalık demo videosu
- Dokümantasyonun tamamlanması

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
