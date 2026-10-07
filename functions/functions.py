from prompts.prompts import QUESTION_CLASSIFICATION_PROMPT,ACTION_REQUEST_EXTRACTION_PROMPT, GENERATE_TRIP_PROMPT, REFINE_TRIP_PROMPT, EXTRACT_RAG_QUERY_PROMPT,GENERATE_RAG_RESPONSE_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
from models.router_output import RouterOutput
from models.action_request import ActionRequest
from models.trip import Trip
from models.rag_query import RAGQuery
from graph.state import GraphState
from functions.llm_config import llm
from datetime import date
from functions.retreival import get_documents, get_pricing_information

def classify_request(state: GraphState):
    request= state["messages"][-1].content
    prompt=PromptTemplate(input_variables=["request"],
    template=QUESTION_CLASSIFICATION_PROMPT)
    structured_llm= llm.with_structured_output(RouterOutput, method="json_mode")
    chain= prompt | structured_llm 
    router_output = chain.invoke({"request": request})
    return {"router_output": router_output}

def branching_logic_question_action(state: GraphState):
    intent= state["router_output"].intent
    if intent.lower()=="question":
        return "question"
    elif intent.lower()=="action":
            if state.get("trip")==None:
                return "new_action"
            else:
                return "refine_action"
    else:
        raise ValueError(f"Unknown intent: {intent}")

def handle_question(state: GraphState):
    print("handling question")


def extract_action_request(state: GraphState):
    recent_messages = state["messages"][-6:]  # last 6 messages (3 exchanges), tune as needed
    request = "\n".join([f"{msg.type}: {msg.content}" for msg in recent_messages])
    prompt=PromptTemplate(input_variables=["request","date"],
    template=ACTION_REQUEST_EXTRACTION_PROMPT)
    structured_llm= llm.with_structured_output(ActionRequest, method="function_calling")
    chain= prompt | structured_llm 
    action_request = chain.invoke({"request": request, "date": date.today()})
    return {"action_request": action_request}


def generate_trip(state: GraphState):
    request_details= state["action_request"]
    prompt=PromptTemplate(input_variables=["request_details","pricing_information"],
    template=GENERATE_TRIP_PROMPT)
    structured_llm= llm.with_structured_output(Trip, method="json_mode")
    chain= prompt | structured_llm 

    hotel_price,ticket_price=get_pricing_information(request_details.destination)
    pricing_information=f"hotel cost {hotel_price} and ticket price {ticket_price}"
    trip = chain.invoke({"request_details": request_details, "pricing_information":pricing_information})

    summary = format_trip_summary(trip)
    return {"trip": trip, "messages": [AIMessage(content=summary)]}



def refine(state: GraphState):
    previous_trip= state["trip"]
    feedback= state["messages"][-1].content
    hotel_price,ticket_price=get_pricing_information(previous_trip.destination)
    pricing_information=f"hotel cost {hotel_price} and ticket price {ticket_price}"
    
    prompt=PromptTemplate(input_variables=["previous_trip","feedback", "pricing_information"],
    template=REFINE_TRIP_PROMPT)
    structured_llm= llm.with_structured_output(Trip, method="json_mode")
    chain= prompt | structured_llm 
    trip = chain.invoke({"previous_trip": previous_trip,"feedback":feedback, "pricing_information": pricing_information})
    summary = format_trip_summary(trip)
    return {"trip": trip, "messages": [AIMessage(content=summary)]}


def extract_rag_query(state: GraphState):
    recent_messages = state["messages"][-6:]  # last 6 messages (3 exchanges), tune as needed
    query = "\n".join([f"{msg.type}: {msg.content}" for msg in recent_messages])
    prompt=PromptTemplate(input_variables=["query"],
    template=EXTRACT_RAG_QUERY_PROMPT)
    structured_llm = llm.with_structured_output(RAGQuery, method="json_mode")
    chain= prompt | structured_llm 
    query = chain.invoke({"query": query})
    return {"rag_query": query}


def generate_rag_response(state:GraphState):
    query= state["rag_query"]
    user_question=state["messages"][-1].content
    documents= get_documents(query,user_question)

    prompt=PromptTemplate(input_variables=["query","documents"],
    template=GENERATE_RAG_RESPONSE_PROMPT)
    chain= prompt | llm 
    response = chain.invoke({"query": query, "documents":documents})
    return {"messages": [response], "rag_documents": documents}

def format_trip_summary(trip: Trip) -> str:
    lines = [
        f"🧳 {trip.trip_name}",
        f"Destination: {trip.destination}",
        f"Dates: {trip.arrival_date} to {trip.departure_date}",
        ""
    ]

    for stop in trip.travel_stops:
        lines.append(f"📍 {stop.location} ({stop.arrival_date} → {stop.departure_date}) — budget: {stop.budget} EUR")
        for activity in stop.activities:
            lines.append(f"   - {activity}")
        lines.append("")

    lines.append(f"Stops budget: {trip.total_stops_budget} EUR")
    lines.append(f"Other expenses: {trip.other_expenses} EUR")
    lines.append(f"Total budget: {trip.total_budget} EUR")

    return "\n".join(lines)