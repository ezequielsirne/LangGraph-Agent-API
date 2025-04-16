from langchain_core.runnables import RunnableLambda
from src.agents.state import GraphState
from src.agents.vector_db import get_retriever

def info_node(state: GraphState) -> GraphState:
    """
    Retrieves relevant chunks of text from the vector DB based on user input.
    """
    user_input = state["user_input"]
    retriever = get_retriever()
    docs = retriever.invoke(user_input)

    # Save retrieved documents' content in the state
    return {
        **state,
        "info_docs": [doc.page_content for doc in docs]
    }

info_node_runnable = RunnableLambda(info_node)

if __name__ == "__main__":
    import json

    test_inputs = [
        "¿Qué servicios ofrece el hotel?",
        "¿El desayuno está incluido?",
        "¿Tienen estacionamiento privado?",
    ]

    for idx, input_text in enumerate(test_inputs, 1):
        print(f"\nTest #{idx}")
        try:
            fake_state = {
                "conversation_history": [],
                "user_input": input_text,
                "info_docs": None,
                "availability": None,
            }

            updated_state = info_node(fake_state)

            print("User input:", input_text)
            print("Retrieved documents:")
            for i, doc in enumerate(updated_state["info_docs"], 1):
                print(f"- Chunk #{i}:\n{doc[:250]}...\n")

        except Exception as e:
            print(f"Error in test #{idx}: {e}")

