# CarePilot — Backend

FastAPI + async SQLAlchemy + PostgreSQL tabanlı API.

## Mimari (clean architecture)

```
app/
├── api/            # HTTP katmanı: router'lar + bağımlılıklar (DI)
│   ├── deps.py
│   └── v1/
│       ├── router.py
│       └── endpoints/
├── core/           # config, constants, security, exceptions
├── db/             # Base modeller + async session
├── models/         # SQLAlchemy ORM modelleri
├── schemas/        # Pydantic v2 request/response şemaları
├── repositories/   # Veri erişim katmanı (ORM, ham SQL yok)
├── services/       # İş mantığı
├── agent/          # Yapay zeka agent'ı (Sprint 2)
└── main.py         # Uygulama giriş noktası
```

Akış: **router → service → repository → model**

## Yerel Kurulum

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash)
pip install -r requirements.txt
cp .env.example .env            # değerleri doldur
```

### Veritabanını başlat (Docker)

```bash
# Proje kökünden
docker compose up -d db
```

### Migration

```bash
cd backend
alembic revision --autogenerate -m "ilk şema"
alembic upgrade head
```

### Çalıştır

```bash
uvicorn app.main:app --reload
# http://localhost:8000/docs
```

### Test

```bash
pytest
```
