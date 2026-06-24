"""v1 API ana router'ı — alt endpoint router'larını toplar."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    auth,
    clinics,
    health,
    journey_steps,
    patients,
    triage_reports,
)

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(clinics.router)
api_router.include_router(patients.router)
api_router.include_router(triage_reports.router)
api_router.include_router(journey_steps.router)
