from graph.graph import graph
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv
import uuid



load_dotenv()

if __name__== "__main__":

    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}

    # 6. Run it
    print(f"STARTING GRAPH EXECUTION for id: {thread_id}")

    

    user_input= input("AI:hey how can i help?\nYOU:")
    while(user_input.lower()!="exit"):
        result = graph.invoke({
            "messages": [HumanMessage(content=user_input)]
            }, config=config)

        print(f"AI:{result['messages'][-1].content}")
        user_input= input("YOU:")
