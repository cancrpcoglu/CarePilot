"""Ortak FastAPI bağımlılıkları (DI)."""

import uuid
from collections.abc import Callable
from typing import Annotated

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.exceptions import AppException
from app.core.security import decode_access_token
from app.db.session import get_db
from app.models.user import User, UserRole
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


def require_role(*allowed_roles: UserRole) -> Callable[..., User]:
    """Yalnızca belirtilen rollere izin veren bir bağımlılık üretir."""

    def _checker(current_user: CurrentUser) -> User:
        if current_user.role not in allowed_roles:
            raise AppException(
                "Bu işlem için yetkiniz yok.",
                status.HTTP_403_FORBIDDEN,
            )
        return current_user

    return _checker


# İki panelin yetki ayrımı için hazır rol-guard'ları
require_clinic_admin = require_role(UserRole.CLINIC_ADMIN)
require_patient = require_role(UserRole.PATIENT)

ClinicAdmin = Annotated[User, Depends(require_clinic_admin)]


async def get_current_clinic_id(admin: ClinicAdmin) -> uuid.UUID:
    """Klinik yöneticisinin bağlı olduğu klinik id'sini döner.

    Henüz klinik oluşturmamışsa 409 ile uyarır (önce /clinics çağrılmalı).
    """
    if admin.clinic_id is None:
        raise AppException(
            "Önce bir klinik profili oluşturmalısınız.",
            status.HTTP_409_CONFLICT,
        )
    return admin.clinic_id


CurrentClinicId = Annotated[uuid.UUID, Depends(get_current_clinic_id)]
