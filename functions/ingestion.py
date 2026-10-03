import chromadb
from models.rag_query import RAGQuery
import json

with open("data/kb.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

client = chromadb.PersistentClient(path="./data/chroma_db")

collection=client.get_or_create_collection("travel-guide")

collection.add(ids=[doc["id"] for doc in documents],documents=[doc["text"] for doc in documents], metadatas=[doc["metadata"] for doc in documents])