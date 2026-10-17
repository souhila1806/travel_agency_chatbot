import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
from langchain_ollama import ChatOllama

base_url=os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
llm_provider=os.environ.get("LLM_PROVIDER", "ollama")

if llm_provider == "ollama":
    llm = ChatOllama(
        model="llama3.2",
        temperature=0,
        base_url=base_url
    )
elif llm_provider == "groq":
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROQ_MODEL = os.getenv("GROQ_MODEL")
    if not GROQ_API_KEY or not GROQ_MODEL:
        raise ValueError("GROQ_API_KEY and GROQ_MODEL must be set in the environment variables.")
    llm = ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0, max_tokens=4096, max_retries=5,)
else:
    raise ValueError(f"Unsupported LLM provider: {llm_provider}")
