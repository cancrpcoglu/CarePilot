"""v1 API ana router'ı — alt endpoint router'larını toplar."""

from fastapi import APIRouter

from app.api.v1.endpoints import health

api_router = APIRouter()
api_router.include_router(health.router)
