from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableLambda
from typing import Literal
from src.agents.state import GraphState

# Simple routing prompt
router_prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a routing assistant for a hotel reservation system.\n"
     "Your job is to classify the user input into one of the following categories:\n"
     "- info_node: if the user asks for general hotel information or services.\n"
     "- availability_node: if the user asks about reservation dates or availability.\n"
     "- both_node: if the user asks for both availability and general hotel information.\n"
     "- end: if the message is a greeting or not actionable.\n\n"
     "Respond ONLY with one of the following: info_node, availability_node, both_node, end.\n"
     "Do not provide explanations or additional text."),
    ("user", "{input}")
])

# LLM setup
llm = ChatOpenAI(model="gpt-4", temperature=0)

# Simple output parser (ensures clean routing decision)
output_parser = StrOutputParser()

# Full runnable chain
router_chain = router_prompt | llm | output_parser

# Node function to use in LangGraph
def router_node(state: GraphState) -> Literal["info_node", "availability_node", "both_node", "end"]:
    user_input = state["user_input"]
    decision = router_chain.invoke({"input": user_input})
    return decision

# Runnable for LangGraph
router_node_runnable = RunnableLambda(router_node)

# Quick testing
if __name__ == "__main__":
    test_inputs = [
        "¿Qué servicios incluye el hotel?",
        "¿Tienen disponibilidad este fin de semana?",
        "Me gustaría saber qué ofrecen y si puedo reservar para mañana",
        "Hola, gracias!"
    ]

    for text in test_inputs:
        state = {"user_input": text, "conversation_history": [], "info_docs": None, "availability": None}
        print(f"Input: {text}")
        print(f"Route decision: {router_node(state)}")
