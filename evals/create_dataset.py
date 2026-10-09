import json
from dotenv import load_dotenv
load_dotenv()
from langsmith import Client

client = Client()

with open("evals/examples.json", "r", encoding="utf-8") as f:
    examples = json.load(f)

dataset = client.create_dataset(dataset_name="travel-agent-eval")

client.create_examples(
    dataset_id=dataset.id,
    examples=[
        {
            "inputs": {"turns": ex["turns"]},
            "outputs": {"reference": ex["reference"]},
            "metadata": {"id": ex["id"], "category": ex["category"]},
        }
        for ex in examples
    ],
)