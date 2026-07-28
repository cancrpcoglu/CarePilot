# 🎬 CarePilot — 3 Dakikalık Demo Video Senaryosu

Hedef süre: **~3:00**. Ekranı paylaşarak canlı akışı göster; her sahnede aşağıdaki
konuşma metnini kullanabilirsin. (İki sekme aç: **klinik paneli** ve **hasta linki**.)

---

### 0:00 – 0:25 — Problem & Çözüm
> "Türkiye saç ekimi ve estetik cerrahide dünya lideri; ama yabancı hasta süreci
> dağınık: dil bariyeri, WhatsApp'tan manuel koordinasyon, standart olmayan ön
> değerlendirme. CarePilot bunu çözen, çok dilli ve **hafızalı bir yapay zeka
> hasta konsiyerj platformu**."

Ekran: açılış sayfası.

### 0:25 – 0:50 — Klinik & Self-servis davet linki
> "Klinik kaydolur ve tek bir **davet linki + QR** alır — web sitesine koyar."

Ekran: panele giriş → dashboard'daki "Klinik davet linki" kartı + QR. Linki kopyala.

### 0:50 – 1:45 — Hasta: AI ile sohbet (asıl gösteri)
> "Hasta bu linke tıklar, adını yazar ve yapay zeka asistanıyla **kendi dilinde**
> sohbet eder. Agent **hafızalıdır** — önceki cevapları hatırlar ve zorunlu tüm
> bilgileri (tedavi, sağlık geçmişi, ilaç, sigara) toplayana kadar tek tek sorar."

Ekran: intake linki → ad gir → chat. İngilizce/Arapça birkaç mesaj yaz; agent'ın
takip soruları sorup sonunda "değerlendirmeniz kliniğe iletildi" demesini göster.

> "Arka planda Gemini 2.5 Flash + LangGraph orkestrasyonu çalışıyor; çıktı serbest
> metin değil, **yapılandırılmış** bir ön değerlendirme (structured output)."

### 1:45 – 2:20 — Klinik: rapor onayı & hasta yönetimi
> "Sohbet biter bitmez klinik panelinde **yapılandırılmış rapor** belirir: tedavi
> alanı, şikayetler, sağlık geçmişi, eksik bilgiler. Klinik inceler ve onaylar."

Ekran: Raporlar sayfası → rapor detayı → Onayla. Sonra hasta detayına gir; **not
ekle**, bilgileri düzenle.

### 2:20 – 2:45 — Embedding tabanlı anlamsal arama
> "Klinik yüzlerce hasta arasında **doğal dille** arama yapabilir — 'diyabetli
> estetik hastaları' gibi. Gemini embedding + pgvector ile en alakalı raporlar
> anlam benzerliğine göre sıralanır."

Ekran: Raporlar sayfası → arama kutusu → sorgu yaz → sonuçların sıralanışını göster.

### 2:45 – 3:00 — Kapanış
> "Özetle: çok dilli, hafızalı bir AI agent; klinik onay akışı; embedding tabanlı
> arama. FastAPI + LangGraph + Gemini + pgvector, Next.js panel. Temiz mimari,
> 34 test, CI/CD. Teşekkürler."

Ekran: mimari diyagramı (README) veya Swagger `/docs`.

---

## Çekim ipuçları
- Demo öncesi 2-3 örnek hasta + rapor oluştur (arama sonuçları dolu görünsün).
- Canlı deploy uykudaysa önce bir istek atıp uyandır (soğuk başlangıç).
- Ekran kaydı: OBS veya Windows `Win+G`. 1080p, sistem sesi + mikrofon.
- Kişisel/gerçek hasta verisi kullanma; örnek isimler kullan.
