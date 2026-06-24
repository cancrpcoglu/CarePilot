"""Ortak FastAPI bağımlılıkları (DI)."""

import uuid
from typing import Annotated

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User
from app.repositories.user import UserRepository

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login"
)

DbSession = Annotated[AsyncSession, Depends(get_db)]


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: DbSession,
) -> User:
    """JWT'den aktif kullanıcıyı çözer; aksi halde 401 döner."""
    payload = decode_access_token(token)
    if payload is None or payload.get("sub") is None:
        raise AppException(
            "Oturum geçersiz veya süresi dolmuş.",
            status.HTTP_401_UNAUTHORIZED,
        )
    try:
        user_id = uuid.UUID(str(payload["sub"]))
    except (ValueError, TypeError):
        raise AppException(
            "Oturum geçersiz.", status.HTTP_401_UNAUTHORIZED
        ) from None

    repo = UserRepository(session)
    user = await repo.get_by_id(user_id)
    if user is None or not user.is_active:
        raise AppException(
            "Kullanıcı bulunamadı veya pasif.",
            status.HTTP_401_UNAUTHORIZED,
        )
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
