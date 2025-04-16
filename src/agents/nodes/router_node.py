from typing import Literal
from src.agents.state import GraphState

def router_node(state: GraphState) -> Literal["info_node", "availability_node", "both_node", "end"]:
    """
    Analyzes the user_input to determine the path in the graph.

    Returns:
        - "info_node" → for general questions about the hotel
        - "availability_node" → when the message is about reservation dates
        - "both_node" → when both info and availability are requested
        - "end" → when there's no actionable intent (e.g. greetings)
    """
    user_input = state["user_input"].lower()

    info_keywords = ["precio", "servicio", "incluye", "ofrece", "habitacion", "servicios", "hotel"]
    availability_keywords = ["disponibilidad", "available", "availability", "reserva", "reservar", "checkin", "checkout"]

    has_info = any(word in user_input for word in info_keywords)
    has_availability = any(word in user_input for word in availability_keywords)

    if has_info and has_availability:
        return "both_node"
    elif has_info:
        return "info_node"
    elif has_availability:
        return "availability_node"
    else:
        return "end"
