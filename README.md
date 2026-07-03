# 🩺 CarePilot

**Çok dilli ve hafızalı, yapay zeka destekli sağlık turizmi hasta konsiyerj platformu.**

> YZTA (Yapay Zeka ve Teknoloji Akademisi) Bootcamp 2026 kapsamında geliştirilmektedir.

### 🟢 Canlı Demo (API)

Backend Railway üzerinde canlıda:

- **API:** https://carepilot-backend-production.up.railway.app
- **Sağlık kontrolü:** [`/api/v1/health`](https://carepilot-backend-production.up.railway.app/api/v1/health)
- **Etkileşimli API dokümantasyonu (Swagger):** [`/docs`](https://carepilot-backend-production.up.railway.app/docs)

---

## 📋 İçindekiler

- [Problem](#-problem)
- [Çözüm](#-çözüm)
- [Hedef Kullanıcı](#-hedef-kullanıcı)
- [Temel Özellikler](#-temel-özellikler-mvp)
- [Sistem Mimarisi](#-sistem-mimarisi)
- [Yapay Zeka Agent Mimarisi](#-yapay-zeka-agent-mimarisi)
- [Teknoloji Yığını](#-teknoloji-yığını)
- [Veritabanı Şeması](#-veritabanı-şeması)
- [Etik ve Yasal Sınırlar](#-etik-ve-yasal-sınırlar)
- [Proje Yapısı](#-proje-yapısı)
- [Kurulum](#-kurulum)
- [Yol Haritası](#-yol-haritası)
- [Ekip](#-ekip)
- [Sprint Logları](#-sprint-logları)

---

## 🎯 Problem

Türkiye, saç ekimi ve estetik cerrahide **dünya lideri** ülkelerden biri — her yıl yüz binlerce yabancı hasta bu tedaviler için Türkiye'ye geliyor. Ancak bu süreç hâlâ büyük ölçüde manuel ve dağınık şekilde yönetiliyor:

- 🌍 **Dil bariyeri** — hasta ile klinik arasında doğru iletişim kurulamıyor
- 📱 **Dağınık koordinasyon** — süreç genellikle WhatsApp üzerinden, standart olmayan şekilde yürütülüyor
- 📋 **Standart olmayan ön değerlendirme** — her koordinatör farklı bilgi topluyor, klinikler tutarsız veri alıyor
- 🔁 **Takip kaybı** — ameliyat sonrası süreçte hasta ile iletişim kopuyor, hatırlatmalar unutuluyor

## 💡 Çözüm

**CarePilot**, hasta yolculuğunun başından sonuna kadar (ön görüşme → ameliyat → takip) refakat eden, çok dilli ve hafızalı bir **AI hasta konsiyerj agent'ı** sunar:

1. Hasta, kendi dilinde AI agent ile sohbet eder
2. Agent, bu sohbetten **yapılandırılmış bir ön değerlendirme raporu** çıkarır (saç dökülme derecesi, beklenti, sağlık geçmişi vb.)
3. Klinik, bu raporu inceleyip onaylar
4. Agent, ameliyat öncesi/sırası/sonrası süreç boyunca hastayı **hafızasında tutarak** proaktif şekilde yönlendirir, hatırlatır, takip eder

## 👥 Hedef Kullanıcı

CarePilot bir **B2B2C** modeliyle çalışır:

| Taraf | Kim | Nasıl kullanır |
|---|---|---|
| **B2B** | Saç ekimi / estetik cerrahi klinikleri | Platformu white-label satın alır, kendi hastalarına sunar |
| **C** | Yabancı hasta | Klinik üzerinden AI agent'a erişir, sürecini takip eder |

MVP odağı: **saç ekimi ve estetik cerrahi**.

## ✨ Temel Özellikler (MVP)

- 🤖 **Çok dilli triage agent'ı** — hastayla doğal dilde görüşür, yapılandırılmış ön değerlendirme raporu üretir (Pydantic schema + structured output)
- 🧠 **Hafızalı hasta yolculuğu** — PostgreSQL tabanlı konuşma hafızası, hastanın tüm geçmişini ve bağlamını korur
- 🏥 **Klinik paneli** — gelen ön değerlendirmeleri görüntüleme ve onaylama
- 📅 **Proaktif takip** — ameliyat öncesi/sonrası checklist ve agent'ın otomatik hatırlatma mesajları
- 🔐 **Rol tabanlı kimlik doğrulama** — JWT ile klinik ve hasta rolleri ayrı yetkilendirilir

## 🏗 Sistem Mimarisi

```
┌──────────────────┐         ┌───────────────────┐
│ Next.js Frontend  │ ◄─────► │  FastAPI Backend   │
│ (Klinik paneli +   │  REST   │  (Railway)          │
│  Hasta arayüzü)     │         │                     │
└──────────────────┘         └─────────┬─────────┘
                                         │
                ┌────────────────────────┼────────────────────────┐
                │                        │                        │
        ┌───────▼───────┐      ┌─────────▼─────────┐     ┌────────▼────────┐
        │  Auth Service  │      │   Agent Service     │     │ Clinic/Patient   │
        │     (JWT)      │      │   (LangGraph)        │     │    Service        │
        └───────┬───────┘      └─────────┬─────────┘     └────────┬────────┘
                │                        │                        │
                └────────────┬───────────┴───────────┬────────────┘
                              │                       │
                    ┌─────────▼─────────┐    ┌────────▼────────┐
                    │    PostgreSQL       │    │  Gemini 2.5      │
                    │ (kullanıcı, hasta,   │    │  Flash API        │
                    │  konuşma, rapor)     │    └─────────────────┘
                    └─────────────────────┘
```

**Backend mimarisi (clean architecture):**

```
router → service → repository → model
```

Her katman tek bir sorumluluğa sahiptir: router HTTP'yi yönetir, service iş mantığını uygular, repository veri erişimini soyutlar, model veritabanı şemasını temsil eder.

## 🧩 Yapay Zeka Agent Mimarisi

CarePilot'un kalbi, **LangGraph** ile orkestre edilen ve **Gemini 2.5 Flash**'ı kullanan tek bir agent'tır. Agent iki modda çalışır:

1. **Giriş düğümü** — hastanın mevcut durumuna göre modu belirler (yeni hasta → triage, mevcut hasta → followup)
2. **Triage alt-akışı** — çok turlu soru-cevap yürütür → yanıtlardan yapılandırılmış alanları çıkarır (Pydantic schema, function calling) → bilgi eksikse takip sorusu sorar → rapor tamamlanınca `pending` durumunda kaydeder
3. **Followup alt-akışı** — hastanın yolculuk durumunu ve konuşma hafızasını yükler → bir sonraki aksiyonu belirler → proaktif mesaj üretir veya hastanın mesajına bağlam içinde yanıt verir
4. **Guardrail düğümü** — her yanıt, kullanıcıya dönmeden önce "tıbbi tavsiye değil" kontrolünden geçer

**Hafıza:** PostgreSQL tabanlı `ChatMessageHistory` — her hastanın tüm konuşma geçmişi kalıcı olarak saklanır ve agent'ın bağlamını besler.

**Structured output:** Agent yanıtları, JSON mode değil **function calling / Pydantic şema** ile yapılandırılır — bu, çıktının her zaman doğrulanabilir ve tutarlı olmasını garanti eder.

## ⚙️ Teknoloji Yığını

| Katman | Teknoloji |
|---|---|
| Backend | FastAPI, async SQLAlchemy, Alembic |
| Veritabanı | PostgreSQL (+ pgvector) |
| Yapay Zeka | LangChain / LangGraph, Gemini 2.5 Flash |
| Frontend | Next.js (App Router), TypeScript, Tailwind CSS, shadcn/ui |
| Kimlik Doğrulama | JWT |
| Test | Pytest, ruff (lint) |
| CI/CD | GitHub Actions |
| Deploy | Railway |

## 🗄 Veritabanı Şeması

| Tablo | Açıklama |
|---|---|
| `users` | Kullanıcılar (klinik yöneticisi veya hasta), rol bazlı |
| `clinics` | Klinik bilgileri |
| `patients` | Hasta profili, dil, klinik ilişkisi |
| `conversations` | Hasta-agent konuşma oturumları (triage/followup) |
| `messages` | Konuşma mesajları |
| `triage_reports` | Yapılandırılmış ön değerlendirme raporları (pending/approved/rejected) |
| `journey_steps` | Hasta yolculuğu adımları (ameliyat öncesi/sonrası checklist) |

Tüm tablolar `created_at`, `updated_at` ve `is_deleted` (soft delete) kolonlarını içerir.

## ⚖️ Etik ve Yasal Sınırlar

> **CarePilot'un AI agent'ı kesinlikle tanı veya tedavi tavsiyesi vermez.**

Agent yalnızca bilgi toplar, yapılandırır ve klinik onayına sunar. Nihai tıbbi karar her zaman yetkili sağlık profesyoneline aittir. Bu sınır, sistem promptunda ve kullanıcı arayüzünde açıkça belirtilir.

Hasta sağlık verisi, KVKK kapsamında **özel nitelikli kişisel veri** sayılır; açık rıza metni ve veri güvenliği önlemleri bu doğrultuda tasarlanmıştır.

## 📁 Proje Yapısı

```
CarePilot/
├── backend/
│   ├── app/
│   │   ├── api/            # HTTP katmanı: router'lar + DI bağımlılıkları
│   │   ├── core/            # config, constants, security, exceptions
│   │   ├── db/               # Base modeller + async session
│   │   ├── models/          # SQLAlchemy ORM modelleri
│   │   ├── schemas/         # Pydantic v2 şemaları
│   │   ├── repositories/    # Veri erişim katmanı
│   │   ├── services/        # İş mantığı
│   │   ├── agent/            # Yapay zeka agent'ı (LangGraph)
│   │   └── main.py
│   ├── alembic/             # Veritabanı migration'ları
│   ├── tests/
│   └── requirements.txt
├── frontend/                # Next.js uygulaması (Sprint 2)
├── .github/workflows/        # CI pipeline
├── docker-compose.yml
├── PRD.md                    # Detaylı ürün gereksinimleri
└── README.md
```

## 🚀 Kurulum

### Gereksinimler
- Python 3.12+
- Docker (PostgreSQL için)
- Node.js 20+ (frontend için, Sprint 2'den itibaren)

### Backend

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate      # Windows (Git Bash)
pip install -r requirements.txt
cp .env.example .env                # değerleri doldur

# Veritabanını başlat
docker compose up -d db

# Migration uygula
alembic upgrade head

# Sunucuyu çalıştır
uvicorn app.main:app --reload
# API: http://localhost:8000  |  Docs: http://localhost:8000/docs
```

### Test

```bash
cd backend
pytest
ruff check .
```

## 🗺 Yol Haritası

- [x] **Sprint 1** — Backend iskeleti, auth, veri modelleri, CRUD API'ler, ilk AI (Gemini) entegrasyonu, CI/CD, **Railway'e canlı deploy ✅**
- [ ] **Sprint 2** — Çok turlu hafızalı agent (LangGraph), frontend klinik paneli (başladı), hasta arayüzü
- [ ] **Sprint 3** — Demo hazırlığı, son optimizasyon, dokümantasyon

## 👤 Ekip

| Rol | Kişi |
|---|---|
| Geliştirici | Can Çorapçıoğlu |
| Akademi Danışmanı | Hikmet Topak |
| Grup Numarası | 153 |
| Akademi Bölümü | Yapay Zeka ve Veri Bilimi |

Detaylı ürün gereksinimleri için → [PRD.md](./PRD.md)

---

## 📅 Sprint Logları

### Sprint 1 — Tamamlandı (19 Haziran – 5 Temmuz)

#### Tamamlanan User Story'ler
- [x] Backend proje iskeleti (clean architecture: router → service → repository)
- [x] Veri modelleri: User, Clinic, Patient, Conversation, Message, TriageReport, JourneyStep (+ soft-delete/timestamp mixin'leri)
- [x] JWT kimlik doğrulama (register / login / me) + rol-guard (clinic_admin / patient)
- [x] Klinik / hasta / triage / yolculuk CRUD endpoint'leri (klinik scope'lu, klinikler arası izolasyon)
- [x] **Temel AI entegrasyonu:** Gemini 2.5 Flash + LangChain structured output ile hasta mesajından yapılandırılmış triage ön değerlendirmesi
- [x] Alembic migration'ları (3 adet, geri-alınabilir)
- [x] Global hata yönetimi (kullanıcıya ham hata gösterilmez)
- [x] GitHub Actions CI (lint + test) — 22 test
- [x] Railway'e canlı deploy (backend + PostgreSQL)

#### Sprint Review
**Ne çalışıyor:** Tüm backend canlıda. Auth, klinik/hasta yönetimi ve AI triage uçtan uca çalışıyor — gerçek Gemini çağrısıyla hasta mesajından yapılandırılmış rapor üretilip klinik onayına düşüyor. 22/22 test geçiyor, ruff temiz. Canlı: https://carepilot-backend-production.up.railway.app/docs
**Ne çalışmıyor / eksik:** Hasta arayüzü (agent sohbeti) ve klinik panelinin bazı ekranları Sprint 2'de. AI şu an tek turlu; çok turlu hafıza Sprint 2'de gelecek.

#### Sprint Retrospective
**İyi giden:** Planın önüne geçildi — deploy (Sprint 3 hedefiydi) ve frontend başlangıcı (Sprint 2) erken tamamlandı. Her adım testle doğrulandı.
**Geliştirilmesi gereken:** AI katmanı tek turlu; LangGraph ile hafızalı, çok turlu agent'a geçilmeli.
**Sonraki sprint için aksiyon:** Hafızalı agent, hasta arayüzü, klinik panelinde triage rapor detay/onay ekranları.
