"""Parola hashleme ve JWT token üretimi/çözümü."""

from datetime import UTC, datetime, timedelta

import bcrypt
import jwt

from app.core import constants
from app.core.config import settings


def hash_password(password: str) -> str:
    """Düz parolayı bcrypt ile hashler."""
    pwd_bytes = password.encode("utf-8")[: constants.BCRYPT_MAX_PASSWORD_BYTES]
    salt = bcrypt.gensalt(rounds=constants.BCRYPT_ROUNDS)
    return bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Düz parolayı hash ile karşılaştırır."""
    pwd_bytes = plain_password.encode("utf-8")[: constants.BCRYPT_MAX_PASSWORD_BYTES]
    try:
        return bcrypt.checkpw(pwd_bytes, hashed_password.encode("utf-8"))
    except ValueError:
        # Bozuk/geçersiz hash formatı
        return False


def create_access_token(subject: str, expires_delta: timedelta | None = None) -> str:
    """Verilen subject (genelde user id) için imzalı JWT üretir."""
    now = datetime.now(UTC)
    expire = now + (
        expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    payload = {"sub": subject, "exp": expire, "iat": now}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=constants.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict | None:
    """JWT'yi doğrular ve payload döner; geçersizse None."""
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[constants.JWT_ALGORITHM],
        )
    except jwt.PyJWTError:
        return None
