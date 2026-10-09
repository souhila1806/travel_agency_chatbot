import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from dotenv import load_dotenv
load_dotenv()
from langsmith import Client
from evals.functions_eval import target_function, evaluator



print("Current directory:", os.getcwd())
print("Python executable:", sys.executable)
print("Python path:", sys.path)


client = Client()
client.evaluate(
    target_function,
    data="travel-agent-eval",
    evaluators=[evaluator],
    experiment_prefix="travel-agent-v1",
    max_concurrency=1,
)