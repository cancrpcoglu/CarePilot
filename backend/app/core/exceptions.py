"""Uygulama hataları ve kullanıcı dostu hata yanıtları (ham hata sızdırmayız)."""

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger("carepilot")


class AppException(Exception):
    """İş mantığı hatalarını taşıyan temel istisna."""

    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ) -> None:
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def register_exception_handlers(app: FastAPI) -> None:
    """Global hata yakalayıcıları FastAPI uygulamasına bağlar."""

    @app.exception_handler(AppException)
    async def _app_exception_handler(_: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )

    @app.exception_handler(RequestValidationError)
    async def _validation_exception_handler(
        _: Request, __: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": "Gönderilen veriler geçersiz. Lütfen alanları kontrol edin."},
        )

    @app.exception_handler(Exception)
    async def _unhandled_exception_handler(_: Request, exc: Exception) -> JSONResponse:
        # Ham hatayı kullanıcıya göstermeyiz; loglara yazarız.
        logger.exception("Beklenmeyen hata: %s", exc)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Beklenmeyen bir hata oluştu. Lütfen daha sonra tekrar deneyin."},
        )
