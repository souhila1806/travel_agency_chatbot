import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()
from langchain_ollama import ChatOllama

llm = ChatOllama(
    model="llama3.2",
    temperature=0,
)

# GROQ_API_KEY = os.getenv("GROQ_API_KEY")
# GROQ_MODEL = os.getenv("GROQ_MODEL")

# llm= ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0, max_tokens=4096,max_retries=5,)
