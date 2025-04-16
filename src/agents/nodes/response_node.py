# src/agents/nodes/response_node.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from src.agents.state import GraphState

# LLM configuration
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Prompt template with dynamic language and contextual memory
response_prompt = ChatPromptTemplate.from_messages([
    ("system", 
     "You are a helpful assistant at **La Rosalina Resort**, a countryside hotel that offers reservations for apartments. "
     "Respond in the same language as the user's message. "
     "Use the context below to answer questions, describe services, or confirm availability.\n\n"
     "Context:\n{context}"),
    ("user", "{user_input}")
])

def response_node(state: GraphState) -> GraphState:
    user_input = state["user_input"]

    # Build context from info and availability
    context_parts = []

    if state.get("info_docs"):
        context_parts.append("Hotel information:\n" + "\n".join(state["info_docs"]))

    if state.get("availability"):
        context_parts.append("Availability:\n" + str(state["availability"]))

    if not context_parts:
        context_parts.append("No additional context available.")

    full_context = "\n\n".join(context_parts)

    # Format the prompt with context and user message
    prompt = response_prompt.format_messages(
        context=full_context,
        user_input=user_input
    )

    # Generate response using the LLM
    reply = llm.invoke(prompt)

    # Update state with assistant response (if needed later)
    return {
        **state,
        "assistant_response": reply.content
    }

# Runnable version
response_node_runnable = RunnableLambda(response_node)


if __name__ == "__main__":
    sample_state = {
        "conversation_history": [],
        "user_input": "¿El desayuno está incluido?",
        "info_docs": [
            "El desayuno está incluido en todas las tarifas.",
            "El horario del desayuno es de 8:00 a 10:30 AM."
        ],
        "availability": None,
    }

    result_state = response_node(sample_state)
    print("Assistant Response:")
    print(result_state["assistant_response"])
