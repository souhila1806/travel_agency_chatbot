import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
import uuid
from graph.graph import graph
from langchain_core.messages import HumanMessage

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])


user_input = st.chat_input("Type your message...")

config = {"configurable": {"thread_id": st.session_state.thread_id}}
if user_input:
    # append + display the user's message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)


    result = graph.invoke({
    "messages": [HumanMessage(content=user_input)]
    }, config=config)
    st.session_state.messages.append({"role": "assistant", "content": result['messages'][-1].content})
    with st.chat_message("assistant"):
            st.write(result['messages'][-1].content)

