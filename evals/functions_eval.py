import uuid
from graph.graph import graph
from langchain_core.messages import HumanMessage
from evals.prompts_eval import EVALUATION_PROMPT
from langchain_core.prompts import PromptTemplate
from functions.llm_config import llm
from evals.target_response import TargetResponse


def target_function(input:dict)->dict:
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    for user_input in input["turns"]:
        result = graph.invoke({"messages": [HumanMessage(content=user_input)]}, config=config)

    return {"response": result["messages"][-1].content}

def evaluator(inputs: dict, outputs: dict, reference_outputs: dict) -> dict:
    print(f"INPUTS: {inputs}\n")
    print(f"OUTPUTS: {outputs}\n")
    print(f"REFERENCE OUTPUTS: {reference_outputs}\n")

    prompt = PromptTemplate(
    input_variables=["user_request", "ai_response", "expected"],
    template=EVALUATION_PROMPT,)
    structured_llm = llm.with_structured_output(
    TargetResponse,
    method="json_mode",)
    chain = prompt | structured_llm
    conversation = "\n".join(f"user: {t}" for t in inputs["turns"])
    verdict = chain.invoke({"user_request": conversation, "ai_response": outputs["response"], "expected": reference_outputs["reference"]})
    return {
        "key": "correct",
        "score": int(verdict.is_correct),
        "comment": verdict.reason,
    }