# src/agents/nodes/response_node.py
from typing import Dict, Any, List

from langchain_core.messages import SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI

from langchain.schema import SystemMessage, HumanMessage, AIMessage, BaseMessage
import langchain_core.messages as core_msgs

from src.agents.state import GraphState
from src.config.settings import settings

# ── LLM config ────────────────────────────────────────────────────────────────
llm = ChatOpenAI(model=settings.model, temperature=0)

SYSTEM_TEMPLATE = (
    "You are a helpful assistant at **La Rosalina Resort**, a countryside hotel "
    "that offers reservations for apartments. Respond in the same language as "
    "the user's message. Use the context below to answer questions, describe "
    "services, or confirm availability.\n\n"
    "Context:\n{context}"
)

def _core_to_schema(msg: core_msgs.BaseMessage) -> BaseMessage:
    """Convert any langchain_core BaseMessage (dynamic class) into
    the equivalent langchain.schema message that ChatOpenAI expects."""
    # msg.type is a string: "human" | "ai" | "system" | "tool"
    if msg.type == "human":
        return HumanMessage(content=msg.content)
    if msg.type == "ai":
        return AIMessage(content=msg.content)
    if msg.type == "system":
        return SystemMessage(content=msg.content)
    # Add more branches if you store tool/assistant messages
    raise TypeError(f"Unsupported message type {msg.type!r}")

def response_node(state: GraphState) -> Dict[str, Any]:
    """
    Build the assistant reply using existing chat_memory but *do not*
    mutate it; Streamlit handles memory updates.
    """

    # Build contextual string
    parts: List[str] = []

    if state.retrieved_documents:
        parts.append("Hotel information:\n" + "\n".join(state.retrieved_documents))
    if state.availability:
        parts.append("Availability:\n" + str(state.availability))
    if not parts:
        parts.append("No additional context available.")

    context = "\n\n".join(parts)

    # Assemble message list (schema types only)
    messages: List[BaseMessage] = [
        SystemMessage(content=SYSTEM_TEMPLATE.format(context=context))
    ]
    if state.chat_memory:
        messages.extend(_core_to_schema(m) for m in state.chat_memory.messages)
    
    messages.append(HumanMessage(content=state.user_input))

    # Call the model
    assistant_reply = llm.invoke(messages)

    # Return *new* state dict (memory is unchanged)
    return {
        **state.dict(),
        "final_answer": assistant_reply.content,
    }

# Runnable for the graph
response_node_runnable = RunnableLambda(response_node)


# ── Quick manual test ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    from langchain_core.chat_history import InMemoryChatMessageHistory

    mock_memory = InMemoryChatMessageHistory()
    mock_memory.add_user_message("¿Tienen disponibilidad para este fin de semana?")

    sample_state = GraphState(
        chat_memory=mock_memory,
        user_input="¿El desayuno está incluido?",
        retrieved_documents=[
            "El desayuno está incluido en todas las tarifas.",
            "Horario: 8:00 a 10:30 AM."
        ],
        availability=None,
    )

    result_state = response_node(sample_state)
    print("Assistant Response:\n", result_state["final_answer"])
