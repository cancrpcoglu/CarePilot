"""Kimlik doğrulama endpoint'leri: kayıt, giriş, mevcut kullanıcı."""

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import CurrentUser, DbSession
from app.schemas.auth import RegisterRequest
from app.schemas.token import Token
from app.schemas.user import UserRead
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Klinik hesabı kaydı",
)
async def register(data: RegisterRequest, session: DbSession) -> UserRead:
    service = AuthService(session)
    user = await service.register_clinic_admin(data)
    return user


@router.post("/login", response_model=Token, summary="Giriş (JWT döner)")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: DbSession,
) -> Token:
    service = AuthService(session)
    token = await service.authenticate(form_data.username, form_data.password)
    return Token(access_token=token)


@router.get("/me", response_model=UserRead, summary="Mevcut kullanıcı")
async def read_me(current_user: CurrentUser) -> UserRead:
    return current_user
