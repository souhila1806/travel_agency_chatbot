import chromadb
from models.rag_query import RAGQuery

client = chromadb.PersistentClient(path="./data/chroma_db")

collection=client.get_or_create_collection("travel-guide")

def get_documents(query: RAGQuery, user_question:str):

    if query.destination is None:
        where_statement={"type": query.type}
    else:
        where_statement={
            "$and": [
                {"destination": query.destination},
                {"type": query.type}
            ]
        }
    results = collection.query(
        query_texts=user_question,
        where=where_statement
    )
    return results["documents"][0]


def get_pricing_information(destination):
    hotel_price = collection.query(
            query_texts=f"get the amount to spend for booking hotel in {destination}",
            where={
            "$and": [
                {"destination": destination},
                {"type": "hotel_offer"}
            ]
        }
        )
    ticket_price = collection.query(
                query_texts=f"get the amount to spend for flight to {destination}",
                where={
                "$and": [
                    {"destination": destination},
                    {"type": "flight_offer"}
                ]
            }
            )

    hotel_text = "\n".join(hotel_price["documents"][0]) if hotel_price["documents"][0] else "No agency hotel pricing available for this destination."
    ticket_text = "\n".join(ticket_price["documents"][0]) if ticket_price["documents"][0] else "No agency ticket pricing available for this destination."
    return hotel_text,ticket_text