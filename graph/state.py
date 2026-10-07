from typing import Annotated, TypedDict, Optional
from langgraph.graph.message import add_messages
from models.router_output import RouterOutput
from models.action_request import ActionRequest
from models.trip import Trip
from models.rag_query import RAGQuery
from models.guardrails.safety_check import SafetyCheck


class GraphState(TypedDict):
    messages: Annotated[list, add_messages]
    user_question: Optional[str]
    user_id: str 
    router_output: Optional[RouterOutput]
    action_request: Optional[ActionRequest]
    trip: Optional[Trip]
    rag_query: Optional[RAGQuery]
    safety_check: Optional[SafetyCheck]
    rag_documents: Optional[list[str]]