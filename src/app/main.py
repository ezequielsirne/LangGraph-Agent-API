# src/app/main.py

import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.agents.graph import graph_runnable

# Page config
st.set_page_config(page_title="La Rosalina Resort", page_icon="🌟")
st.title("🏨 La Rosalina Resort Assistant")
st.markdown("Bienvenido a nuestro asistente de reservas. ¡Estoy aquí para ayudarte!")

# Session state for memory
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = InMemoryChatMessageHistory()
if "graph_state" not in st.session_state:
    st.session_state.graph_state = {
        "chat_memory": st.session_state.chat_memory,
        "user_input": "",
        "retrieved_documents": None,
        "availability": None,
    }

# Chat input
user_input = st.chat_input("¡Escribí tu pregunta!")
if user_input:
    # Update memory and state
    st.session_state.chat_memory.add_user_message(user_input)
    st.session_state.graph_state["user_input"] = user_input

    # Run the graph
    result = graph_runnable.invoke(st.session_state.graph_state)
    final_answer = result.get("final_answer", "[No response generated]")
    st.session_state.graph_state = result

    # Save the assistant's reply
    st.session_state.chat_memory.add_ai_message(final_answer)

# Display chat history
for msg in st.session_state.chat_memory.messages:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.markdown(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(msg.content)
