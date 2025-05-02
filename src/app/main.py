# src/app/main.py
import streamlit as st
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.chat_history import InMemoryChatMessageHistory
import sys, os, time

# Add project root to PYTHONPATH so “src.agents.graph” can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from src.agents.graph import graph_runnable

# ---------- Page configuration ----------
st.set_page_config(
    page_title="La Rosalina Resort Assistant",
    page_icon="src/app/assets/logo_larosalina.png",
    layout="centered",
)

# ---------- Sidebar (unchanged) ----------
with st.sidebar:
    st.image("src/app/assets/logo_larosalina.png", width=250)
    st.markdown(
        "## 🌟 About the Project\n"
        "La Rosalina Assistant is a chatbot that helps guests by answering questions "
        "about hotel services and room availability.\n"
    )
    # Project Overview
    st.title("🛠️ Project Overview")
    st.markdown(
        """        
        **Technologies Used:**
        - Python 3.11
        - Streamlit (Frontend)
        - LangGraph (Graph-based agent orchestration)
        - LangChain Core (Memory, Chat Messages, Runnables)
        - OpenAI (GPT-4.1 API for reasoning)
        - Pinecone (Vector database for RAG)
        
        **Architecture:**
        - Hybrid RAG + Tool-Use agent
        - Modular LangGraph nodes:
            - Router Node (LLM-based ReAct decision)
            - Info Node (RAG over vector database)
            - Availability Node (LLM + Booking API check)
            - Response Node (Dynamic response generation)
        - Parallel execution for multi-intent queries
        - Streamlit state management for chat history
        
        **Goal:**
        - Build a technical demo showcasing LLM orchestration, retrieval-augmented generation, and tool usage in a realistic hotel assistant scenario.
        """
    )

# ---------- Header ----------
st.title("La Rosalina Resort Assistant")
st.markdown(
    "[![GitHub Repo]"
    "(https://img.shields.io/badge/GitHub-Repository-black?logo=github)]"
    "(https://github.com/ezequielsirne/LangGraph-Agent-API)"
)

# Description cards
col1, col2 = st.columns(2)
with col1:
    st.markdown("🌎 English")
    st.caption(
        """
        This project is a customer service assistant capable of advising clients and answering questions about services and room availability.
        It was built leveraging a hotel management API to explore real-world LLM agent integrations.
        It combines LLM capabilities and RAG to deliver smart responses, real-time availability checks, and has plans for future booking registration.
        """
    )
with col2:
    st.markdown("🌎 Español")
    st.caption(
        """
        Este proyecto es un asistente de atención al público capaz de asesorar clientes y responder dudas sobre servicios y disponibilidad.
        Fue desarrollado aprovechando una API de gestión hotelera para explorar la integración de agentes LLM en sistemas reales.
        Combina un modelo de lenguaje y RAG para brindar respuestas inteligentes y verificar disponibilidad en tiempo real.
        """
    )
st.divider()

# ---------- Session‑state ----------
if "chat_memory" not in st.session_state:
    st.session_state.chat_memory = InMemoryChatMessageHistory()
    
if "graph_state" not in st.session_state:
    st.session_state.graph_state = {
        "chat_memory": st.session_state.chat_memory,
        "user_input": "",
        "retrieved_documents": None,
        "availability": None,
    }

# ---------- Helper: stream assistant reply ----------
def stream_answer(text: str):
    """Yield one word at a time so st.write_stream streams the reply."""
    for word in text.split():
        yield word + " "
        time.sleep(0.03)  # feel free to tweak / remove

# ---------- Quick suggestions ----------
st.subheader("🛎️ Quick Suggestions / Sugerencias Rápidas")

col1, col2 = st.columns(2)

with col1:
    st.markdown("**🇬🇧 English**")
    if st.button("What services does the hotel offer?", key="en_services"):
        st.session_state.pending_prompt = "What services does the hotel offer?"
    if st.button("Is there availability for this weekend?", key="en_weekend"):
        st.session_state.pending_prompt = "Is there availability for this weekend?"

with col2:
    st.markdown("**🇪🇸 Español**")
    if st.button("¿Qué servicios ofrece el hotel?", key="es_services"):
        st.session_state.pending_prompt = "¿Qué servicios ofrece el hotel?"
    if st.button("¿Tienen disponibilidad para este fin de semana?", key="es_weekend"):
        st.session_state.pending_prompt = "¿Tienen disponibilidad para este fin de semana?"

# ---------- Display chat history ----------
for msg in st.session_state.chat_memory.messages:
    role = "user" if isinstance(msg, HumanMessage) else "assistant"
    with st.chat_message(role):
        st.markdown(msg.content)

# ---------- Retrieve pending prompt from buttons ----------
prompt = st.session_state.pop("pending_prompt", None)

# ---------- Free‑form chat input ----------
if not prompt:
    prompt = st.chat_input("Write your question! / ¡Escribí tu pregunta!")

if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)

    result = graph_runnable.invoke(
        {
            "chat_memory": st.session_state.chat_memory,
            "user_input": prompt,
            "retrieved_documents": None,
            "availability": None,
        }
    )
    final_answer = result.get("final_answer", "[No response generated]")

    with st.chat_message("assistant"):
        st.write_stream(stream_answer(final_answer))

    # Persist both messages
    st.session_state.chat_memory.add_user_message(prompt)
    st.session_state.chat_memory.add_ai_message(final_answer)

    # Force a rerun so st.chat_input is rendered again
    st.rerun()