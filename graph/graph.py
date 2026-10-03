from langgraph.graph import StateGraph, END
from graph.state import GraphState
from functions.functions import classify_request, branching_logic_question_action, handle_question, extract_action_request, generate_trip, refine, extract_rag_query, generate_rag_response
from langgraph.checkpoint.memory import MemorySaver
from functions.guardrails import branching_logic_safety_check, input_safety_check

checkpointer = MemorySaver()

graph = StateGraph(GraphState)
graph.add_node("classify_request", classify_request)
graph.add_node("handle_question", extract_rag_query)
graph.add_node("reply_question", generate_rag_response)
graph.add_node("extract_action_request", extract_action_request)
graph.add_node("generate_trip",generate_trip)
graph.add_node("refine",refine)
graph.add_node("input_safety_check",input_safety_check)


graph.add_conditional_edges("classify_request", branching_logic_question_action, {
    "question": "handle_question",
    "new_action": "extract_action_request",
    "refine_action":"refine"
})

graph.add_conditional_edges("input_safety_check", branching_logic_safety_check, {
    "safe": "classify_request",
    "unsafe": END
})


graph.add_edge("handle_question", "reply_question")
graph.add_edge("reply_question", END)
graph.add_edge("extract_action_request", "generate_trip")
graph.add_edge("refine", END)
graph.add_edge("generate_trip", END)
graph.set_entry_point("input_safety_check")

graph = graph.compile(checkpointer=checkpointer)