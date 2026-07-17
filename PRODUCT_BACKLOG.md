# 📌 CarePilot — Product Backlog

Toplam tahmini: **~300 puan** · 3 sprint · hedef **~100 puan/sprint**

Durum: ✅ Done · 🚧 In Progress · 📋 To Do

---

## Epic 1 — Altyapı & Kimlik Doğrulama

| # | User Story | Puan | Sprint | Durum |
|---|---|---|---|---|
| 1 | Geliştirici olarak clean architecture backend iskeleti istiyorum | 15 | 1 | ✅ |
| 2 | Kullanıcı olarak klinik hesabı oluşturup giriş yapmak istiyorum (JWT) | 15 | 1 | ✅ |
| 3 | Sistem olarak klinik/hasta rollerini ayrı yetkilendirmek istiyorum | 8 | 1 | ✅ |
| 4 | Geliştirici olarak veritabanı migration'larını yönetmek istiyorum (Alembic) | 8 | 1 | ✅ |

## Epic 2 — Klinik & Hasta Yönetimi

| # | User Story | Puan | Sprint | Durum |
|---|---|---|---|---|
| 5 | Klinik yöneticisi olarak klinik profilimi oluşturmak/güncellemek istiyorum | 8 | 1 | ✅ |
| 6 | Klinik olarak hasta ekleyip listelemek istiyorum | 13 | 1 | ✅ |
| 7 | Sistem olarak her kliniğin yalnızca kendi verisine erişmesini istiyorum (izolasyon) | 8 | 1 | ✅ |
| 8 | Klinik olarak hasta yolculuk adımlarını takip etmek istiyorum | 8 | 1 | ✅ |

## Epic 3 — Yapay Zeka Triage

| # | User Story | Puan | Sprint | Durum |
|---|---|---|---|---|
| 9 | Klinik olarak hasta mesajından AI ön değerlendirme üretmek istiyorum (Gemini) | 20 | 1 | ✅ |
| 10 | Sistem olarak AI çıktısını yapılandırılmış (structured output) almak istiyorum | 10 | 1 | ✅ |
| 11 | Klinik olarak gelen ön değerlendirmeleri onaylamak/reddetmek istiyorum | 8 | 1 | ✅ |
| 12 | Hasta olarak agent ile çok turlu, hafızalı sohbet etmek istiyorum | 25 | 2 | ✅ |
| 13 | Sistem olarak konuşma hafızasını PostgreSQL'de tutmak istiyorum | 15 | 2 | ✅ |

## Epic 4 — Frontend

| # | User Story | Puan | Sprint | Durum |
|---|---|---|---|---|
| 14 | Ziyaretçi olarak ürünü anlatan bir açılış sayfası görmek istiyorum | 8 | 1 | ✅ |
| 15 | Klinik olarak kayıt/giriş yapıp panele erişmek istiyorum | 13 | 1 | ✅ |
| 16 | Klinik olarak panelde hasta yönetimi yapmak istiyorum | 13 | 1 | ✅ |
| 17 | Klinik olarak triage raporlarını panelde görüntüleyip onaylamak istiyorum | 20 | 2 | ✅ |
| 18 | Hasta olarak kendi arayüzümden agent ile görüşmek istiyorum | 20 | 2 | ✅ |

## Epic 5 — DevOps & Deploy

| # | User Story | Puan | Sprint | Durum |
|---|---|---|---|---|
| 19 | Geliştirici olarak her PR'da otomatik lint+test istiyorum (CI) | 8 | 1 | ✅ |
| 20 | Ürünü canlıya almak istiyorum (Railway + PostgreSQL) | 13 | 1 | ✅ |
| 21 | Embedding tabanlı anlamsal rapor arama istiyorum (Gemini + pgvector) | 20 | 2 | ✅ |
| 22 | Performans optimizasyonu ve demo hazırlığı istiyorum | 15 | 3 | 📋 |

---

## Sprint Dağılımı

| Sprint | Tarih | Hedef Puan | Tamamlanan | Odak |
|---|---|---|---|---|
| **Sprint 1** | 19 Haz – 5 Tem | 100 | ✅ 100 | Altyapı, auth, CRUD, ilk AI, deploy |
| **Sprint 2** | 6 Tem – 19 Tem | ~100 | ✅ ~100 | Hafızalı agent, hasta/klinik arayüzleri, embedding arama |
| **Sprint 3** | 20 Tem – 2 Ağu | ~100 | 📋 | Ücretsiz hosting'e göç, optimizasyon, demo |
