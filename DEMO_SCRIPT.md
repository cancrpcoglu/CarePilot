# 🎬 CarePilot — 3 Dakikalık Demo Video Senaryosu

Hedef süre: **~3:00**. Ekranı paylaşarak **canlı** akışı göster; her sahnede aşağıdaki
konuşma metnini kullanabilirsin.

**Canlı ortam**
- Panel: <https://carepilot-frontend.onrender.com>
- Demo giriş: `carepilot.demo2026@gmail.com` / `CarePilotDemo2026`
- Hasta davet linki: <https://carepilot-frontend.onrender.com/intake/mQAvur98WPbNanSRdG9hsA>

> İki sekme aç: **klinik paneli** (giriş yapılmış) ve **hasta davet linki**.
> Kayıttan ~2 dk önce ikisini de bir gezerek servisleri uyandır (soğuk başlangıç).

---

### 0:00 – 0:20 — Problem & Çözüm
> "Türkiye saç ekimi ve estetik cerrahide dünya lideri; ama yabancı hasta süreci
> dağınık: dil bariyeri, WhatsApp'tan manuel koordinasyon, standart olmayan ön
> değerlendirme. CarePilot bunu çözen, çok dilli ve **hafızalı bir yapay zeka
> hasta konsiyerj platformu**."

Ekran: açılış sayfası.

### 0:20 – 0:45 — Klinik paneli, dönüşüm hunisi & davet linki
> "Klinik giriş yapar; panelde hasta akışını **dönüşüm hunisiyle** görür: ön kayıt →
> ön değerlendirme → onay. Tek bir **davet linki + QR** alır ve web sitesine koyar."

Ekran: dashboard → **dönüşüm hunisi** kartı, sonra "Klinik davet linki" kartı + QR. Linki kopyala.

### 0:45 – 1:40 — Hasta: KVKK rıza + AI ile sohbet (asıl gösteri)
> "Hasta linke tıklar; adını, **telefon/WhatsApp** bilgisini bırakır ve **KVKK açık
> rıza** verir — sağlık verisi topladığımız için bu zorunlu. Sonra yapay zeka
> asistanıyla **kendi dilinde** sohbet eder."

Ekran: intake linki → ad + telefon gir → **KVKK onay kutusunu işaretle** → başlat → chat.

> "Agent **hafızalıdır** — önceki cevapları hatırlar ve zorunlu tüm bilgileri
> (tedavi, şikayet, kronik hastalık, ilaç, geçmiş ameliyat, sigara/alkol) toplayana
> kadar tek tek sorar. Arka planda Gemini 2.5 Flash + LangGraph çalışıyor; çıktı
> serbest metin değil, **yapılandırılmış** bir ön değerlendirme."

Ekran: İngilizce/Arapça birkaç mesaj yaz; agent takip sorularını sorsun. Bilgiler
tamamlanınca **"Ön değerlendirmeniz tamamlandı — klinik sizinle iletişime geçecek"**
kapanış ekranını göster.

### 1:40 – 2:15 — Klinik: rapor onayı & tek tık iletişim (lead teslimi)
> "Sohbet biter bitmez klinik panelinde **yapılandırılmış rapor** belirir: tedavi
> alanı, şikayetler, sağlık geçmişi, eksik bilgiler. Klinik inceler ve onaylar —
> ardından hastaya **tek tıkla WhatsApp / Ara / E-posta** ile ulaşır."

Ekran: Raporlar → rapor detayı → **Onayla** → rapor kartındaki **WhatsApp/Ara/E-posta**
butonlarını göster. (İstersen hasta detayına gir: KVKK rozeti + iletişim aksiyonları.)

### 2:15 – 2:40 — Embedding tabanlı anlamsal arama
> "Klinik yüzlerce hasta arasında **doğal dille** arama yapabilir — 'diyabetli
> estetik hastaları' gibi. Gemini embedding + pgvector ile en alakalı raporlar
> anlam benzerliğine göre sıralanır."

Ekran: Raporlar → arama kutusu → sorgu yaz → sonuçların anlamca sıralanışını göster.

### 2:40 – 3:00 — Kapanış
> "Özetle: KVKK uyumlu, çok dilli, hafızalı bir AI agent; iletişim yakalama ve tek
> tık lead teslimi; klinik onay akışı; embedding tabanlı arama; dönüşüm hunisi.
> FastAPI + LangGraph + Gemini + pgvector, Next.js panel. Temiz mimari, **38 test**,
> CI/CD ve **canlı** deploy (Render + Neon). Teşekkürler."

Ekran: mimari diyagramı (README) veya Swagger `/docs`.

---

## Çekim ipuçları
- **Servisleri uyandır:** kayıttan ~2 dk önce hem paneli hem hasta linkini gez (Render
  ücretsiz katman uykuya geçer; ilk istekte ~1 dk soğuk başlangıç).
- Demo verisi hazır: demo klinikte **6 çok uluslu hasta** (telefon/e-posta/KVKK onaylı)
  ve raporlar seed'li — arama ve huni dolu görünür.
- **Klinik silmeyi demoda ÇALIŞTIRMA** (Ayarlar → Tehlikeli bölge) — demo verisini
  siler. Sadece bahset: "hesap yönetiminde klinik güvenli onayla silinebilir."
- Ekran kaydı: OBS veya Windows `Win+G`. 1080p, sistem sesi + mikrofon.
- Kişisel/gerçek hasta verisi kullanma; örnek isimler kullan.
