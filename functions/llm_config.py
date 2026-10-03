import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL")

llm= ChatGroq(api_key=GROQ_API_KEY, model=GROQ_MODEL, temperature=0.7, max_tokens=4096)
