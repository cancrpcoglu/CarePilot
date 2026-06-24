"""Kimlik doğrulama iş mantığı (service katmanı)."""

from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AppException
from app.core.security import create_access_token, hash_password, verify_password
from app.models.user import User, UserRole
from app.repositories.user import UserRepository
from app.schemas.auth import RegisterRequest


class AuthService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.users = UserRepository(session)

    async def register_clinic_admin(self, data: RegisterRequest) -> User:
        """Yeni bir klinik yöneticisi hesabı oluşturur."""
        existing = await self.users.get_by_email(data.email)
        if existing is not None:
            raise AppException(
                "Bu e-posta adresi zaten kayıtlı.",
                status.HTTP_409_CONFLICT,
            )
        user = User(
            email=data.email,
            hashed_password=hash_password(data.password),
            full_name=data.full_name,
            role=UserRole.CLINIC_ADMIN,
        )
        user = await self.users.create(user)
        await self.session.commit()
        return user

    async def authenticate(self, email: str, password: str) -> str:
        """E-posta/parola doğrular ve JWT access token döner."""
        user = await self.users.get_by_email(email)
        if user is None or not verify_password(password, user.hashed_password):
            raise AppException(
                "E-posta veya parola hatalı.",
                status.HTTP_401_UNAUTHORIZED,
            )
        if not user.is_active:
            raise AppException("Hesabınız pasif durumda.", status.HTTP_403_FORBIDDEN)
        return create_access_token(str(user.id))
