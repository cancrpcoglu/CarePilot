# CarePilot — Product Requirements Document

## 1. Problem
Türkiye saç ekimi ve estetik cerrahide dünya lideri ama yabancı hasta süreci dağınık: WhatsApp üzerinden manuel koordinatörler, dil bariyeri, standartsız ön değerlendirme, takip kaybı.

## 2. Çözüm
Çok dilli AI hasta konsiyerj agent'ı: hasta kendi dilinde agent'la görüşür → agent yapılandırılmış ön değerlendirme raporu çıkarır → klinik onaylar → agent ameliyat öncesi/sırası/sonrası süreci hafızasında tutup hastayı proaktif yönlendirir.

## 3. Hedef Kullanıcı (B2B2C)
- **B2B:** Saç ekimi / estetik cerrahi klinikleri (white-label satın alır)
- **C:** Yabancı hasta (klinik üzerinden agent'a erişir)

## 4. MVP Kapsamı

**Dahil:**
- Çok dilli triage agent'ı (sohbet → yapılandırılmış ön değerlendirme, Pydantic şema)
- Hasta profili + konuşma hafızası (PostgreSQL backed)
- Klinik paneli: gelen ön değerlendirmeleri görme, onaylama
- Hasta yolculuk takibi: ameliyat öncesi/sonrası checklist + agent'ın proaktif hatırlatma mesajları (uygulama içi)
- Auth (JWT) — klinik kullanıcıları + hasta kullanıcıları ayrı rol

**Hariç (v2):**
- Ödeme/komisyon sistemi
- Gerçek WhatsApp/SMS entegrasyonu
- Çoklu klinik karşılaştırma/pazar yeri (eşleştirme algoritması)
- Görsel analiz (fotoğraftan saç dökülme derecesi tahmini)

## 5. AI Agent Mimarisi (özet)
- Gemini 2.5 Flash, LangChain/LangGraph orkestrasyon
- Tek ana agent, 2 mod:
  - **Triage modu** — yeni hasta görüşmesi, structured output ile ön değerlendirme raporu üretir
  - **Takip modu** — var olan hasta için hafızadan bağlam çekip proaktif/reaktif iletişim kurar
- PostgreSQL backed conversation memory (ChatMessageHistory)

## 6. Etik/Yasal Sınır (kritik)
Agent **kesinlikle tanı/tedavi tavsiyesi vermez**. Sadece bilgi toplar, yapılandırır, klinik onayına sunar. Bu sınır UI'da ve sistem promptunda açıkça belirtilir.

## 7. Tech Stack
- Backend: FastAPI + PostgreSQL (async SQLAlchemy) + Alembic
- AI: LangChain/LangGraph + Gemini 2.5 Flash
- Frontend: Next.js (App Router) + TypeScript + Tailwind + shadcn/ui
- Deploy: Railway (tek platform, ücretsiz tier)
- CI/CD: GitHub Actions (lint + test + build)

## 8. Uyumluluk
KVKK — hasta sağlık verisi özel nitelikli kişisel veri sayılır, açık rıza metni MVP'de yer alır.

## 9. Ekip
Geliştirici: Can Çorapçıoğlu
Akademi Danışmanı: Hikmet Topak (Grup 153)
Akademi Bölümü: Yapay Zeka ve Veri Bilimi

## 10. Takvim
- Sprint 1: Backend iskelet, auth, temel Gemini entegrasyonu, Railway setup
- Sprint 2: Agent + hafıza, triage akışı, frontend temel ekranlar
- Sprint 3: Klinik paneli, polish, deploy, demo video

## 11. Maliyet
Tamamen ücretsiz tier: Railway hobby tier, Gemini API ücretsiz kota, GitHub Actions ücretsiz dakika.
