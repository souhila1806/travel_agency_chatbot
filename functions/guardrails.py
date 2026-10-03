from graph.state import GraphState
from functions.llm_config import llm
from models.guardrails.safety_check import SafetyCheck
from prompts.guardrails import SAFETY_CHECK_PROMPT
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import AIMessage
 


def input_safety_check(state:GraphState):
    message= state["messages"][-1].content
    prompt=PromptTemplate(input_variables=["message"],
    template=SAFETY_CHECK_PROMPT)
    structured_llm = llm.with_structured_output(SafetyCheck, method="json_mode")
    chain= prompt | structured_llm 
    response=chain.invoke({"message":message})
    if not response.safe:
        refusal = AIMessage(content=f"I'm not able to help with that. {response.reason or ''}")
        return {"safety_check": response, "messages": [refusal]}
    return {"safety_check":response}

def branching_logic_safety_check(state:GraphState):
    if state["safety_check"].safe:
        return "safe"
    else:
        return "unsafe"