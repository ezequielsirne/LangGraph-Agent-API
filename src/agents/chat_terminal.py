# src/agents/chat_terminal.py
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from src.agents.graph import graph_runnable

# Initialize empty conversation state
chat_memory = InMemoryChatMessageHistory()

state = {
    "chat_memory": chat_memory,
    "user_input": "",
    "retrieved_documents": None,
    "availability": None,
}

print("💬 Welcome to La Rosalina Resort assistant!")
print("Type 'exit' to quit.\n")

while True:
    try:
        user_input = input("👤 You: ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        # Update state
        state["user_input"] = user_input
        chat_memory.add_user_message(user_input)

        # Run graph
        state = graph_runnable.invoke(state)

        # Show response
        response = state.get("final_answer", "[No response generated]")
        print(f"🤖 Agent: {response}\n")

        # Add to memory
        chat_memory.add_ai_message(response)

    except Exception as e:
        print(f"⚠️ Error: {e}")
