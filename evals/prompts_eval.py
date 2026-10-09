EVALUATION_PROMPT = """You are grading an AI travel assistant.

You are given the user's conversation, the assistant's final answer, and a description of the EXPECTED BEHAVIOR.
The expected behavior is a description of what a correct answer must or must not do. It is not exact wording, so judge whether the answer satisfies it.

Respond with a JSON object containing exactly these fields:
- is_correct (boolean: true if the answer satisfies the expected behavior)
- reason (string: one or two sentences explaining your verdict)

conversation:
{user_request}

assistant's final answer:
{ai_response}

expected behavior:
{expected}
"""