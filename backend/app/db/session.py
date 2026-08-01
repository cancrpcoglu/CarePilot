"""Async veritabanı motoru, oturum fabrikası ve get_db bağımlılığı."""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=False,
    future=True,
    pool_pre_ping=True,  # bayat bağlantıları kullanmadan önce doğrula
    pool_size=5,  # ücretsiz/serverless DB bağlantı limitini aşmamak için ölçülü havuz
    max_overflow=5,
    pool_recycle=300,  # 5 dk'da bir geri dönüştür (Neon boşta bağlantıyı kapatır)
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """İstek başına bir async oturum sağlar; hata olursa rollback eder."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
