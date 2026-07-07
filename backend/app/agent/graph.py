"""LangGraph tabanlı çok turlu, hafızalı triage sohbet agent'ı.

Orkestrasyon: `respond` düğümü Gemini'yi structured output ile çağırır; koşullu
kenar, agent yeterli bilgi topladığında (is_complete) `finalize` düğümüne gider.
Konuşma hafızası (geçmiş mesajlar) service katmanında PostgreSQL'den yüklenir ve
her invoke'ta state olarak verilir.
"""

from typing import TypedDict

from fastapi import status
from langchain_core.messages import BaseMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

from app.agent.schemas import TriageTurn
from app.core import constants
from app.core.config import settings
from app.core.exceptions import AppException


class TriageState(TypedDict):
    messages: list[BaseMessage]
    turn: TriageTurn | None
    report_ready: bool


def _build_structured_llm():
    llm = ChatGoogleGenerativeAI(
        model=constants.GEMINI_MODEL,
        temperature=constants.TRIAGE_TEMPERATURE,
        api_key=settings.GEMINI_API_KEY,
    )
    return llm.with_structured_output(TriageTurn)


async def _respond(state: TriageState) -> dict:
    structured_llm = _build_structured_llm()
    turn = await structured_llm.ainvoke(state["messages"])
    return {"turn": turn}


def _route(state: TriageState) -> str:
    turn = state["turn"]
    if turn is not None and turn.is_complete and turn.assessment is not None:
        return "finalize"
    return END


async def _finalize(state: TriageState) -> dict:
    # Orkestrasyon işareti; raporun kalıcılaştırılması service katmanında yapılır.
    return {"report_ready": True}


def build_triage_graph():
    graph = StateGraph(TriageState)
    graph.add_node("respond", _respond)
    graph.add_node("finalize", _finalize)
    graph.set_entry_point("respond")
    graph.add_conditional_edges("respond", _route, {"finalize": "finalize", END: END})
    graph.add_edge("finalize", END)
    return graph.compile()


_compiled_graph = None


def _get_graph():
    global _compiled_graph
    if _compiled_graph is None:
        _compiled_graph = build_triage_graph()
    return _compiled_graph


async def run_chat_turn(messages: list[BaseMessage]) -> TriageTurn:
    """Konuşma mesajlarıyla grafı çalıştırır ve agent'ın tur çıktısını döner."""
    if not settings.GEMINI_API_KEY:
        raise AppException(
            "Yapay zeka servisi şu an yapılandırılmamış.",
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    graph = _get_graph()
    result = await graph.ainvoke(
        {"messages": messages, "turn": None, "report_ready": False}
    )
    return result["turn"]
