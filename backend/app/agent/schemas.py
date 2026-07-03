"""Agent'ın structured output ile ürettiği şemalar (Pydantic).

Bu şema Gemini'ye function-calling ile verilir; model çıktısını bu yapıya
uygun döndürmek zorundadır (JSON mode değil, structured output).
"""

import enum

from pydantic import BaseModel, Field


class TreatmentArea(str, enum.Enum):
    HAIR_TRANSPLANT = "hair_transplant"
    AESTHETIC_SURGERY = "aesthetic_surgery"
    OTHER = "other"


class TriageAssessment(BaseModel):
    """Hasta mesajından çıkarılan yapılandırılmış ön değerlendirme."""

    detected_language: str = Field(
        description="Hastanın yazdığı dilin ISO 639-1 kodu (örn. 'en', 'tr', 'ar')."
    )
    treatment_area: TreatmentArea = Field(
        description="Hastanın ilgilendiği ana tedavi alanı."
    )
    summary: str = Field(
        description=(
            "Klinik için Türkçe, 1-2 cümlelik nötr özet. "
            "Kesinlikle tıbbi tanı veya tedavi tavsiyesi içermez."
        )
    )
    primary_concerns: list[str] = Field(
        default_factory=list,
        description="Hastanın belirttiği ana şikayet/istekler (kısa ifadeler).",
    )
    patient_expectations: str | None = Field(
        default=None, description="Hastanın belirttiği beklenti (varsa)."
    )
    relevant_medical_history: list[str] = Field(
        default_factory=list,
        description=(
            "Hastanın belirttiği ilgili sağlık geçmişi bilgileri. "
            "Hastanın söylemediği hiçbir bilgi uydurulmaz."
        ),
    )
    missing_information: list[str] = Field(
        default_factory=list,
        description=(
            "Klinik değerlendirmesi için eksik olan ve hastaya sorulması "
            "gereken takip soruları."
        ),
    )
    recommended_specialty: str | None = Field(
        default=None,
        description=(
            "Önerilen uzmanlık/yönlendirme (örn. saç ekimi, plastik cerrahi). "
            "Bu bir tanı değil, koordinasyon amaçlı yönlendirmedir."
        ),
    )
