from datetime import datetime
from langchain_core.tools import tool
from src.services.booking_service import BookingService
from src.agents.vector_db import get_retriever
from src.agents.schemas import AvailabilityInput, InfoRequest, ReservationData

# Instancia del servicio de reservas
booking_service = BookingService()

# Lista de departamentos disponibles
ALL_APARTMENTS = {1, 2, 3, 5, 6, 7, 8}

@tool(args_schema=AvailabilityInput)
def check_availability(checkin: str, checkout: str) -> dict:
    """
    Checks the availability of hotel apartments between two given dates.
    """
    try:
        checkin_date = datetime.fromisoformat(checkin)
        checkout_date = datetime.fromisoformat(checkout)
    except ValueError:
        raise ValueError("Invalid date format. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)")

    reservations = booking_service.get_reservations()

    if not reservations:
        return {"available_apartments": list(ALL_APARTMENTS), "occupied_apartments": []}

    occupied_reservations = [
        {
            "apartment": reservation["departamento"],
            "checkin": reservation["checkin"],
            "checkout": reservation["checkout"]
        }
        for reservation in reservations
        if reservation["eliminado"] == 0 and reservation["estado"] > 0 and (
            (datetime.fromisoformat(reservation["checkin"]) < checkout_date) and
            (datetime.fromisoformat(reservation["checkout"]) > checkin_date)
        )
    ]

    occupied_apartments = {res["apartment"] for res in occupied_reservations}
    available_apartments = list(ALL_APARTMENTS - occupied_apartments)

    return {
        "available_apartments": available_apartments,
        "occupied_apartments": occupied_reservations
    }

@tool(args_schema=InfoRequest)
def get_info(query: str) -> list:
    """
    Retrieves relevant documents from the vector database for the given query.
    """
    retriever = get_retriever()
    documents = retriever.invoke(query)
    return [doc.page_content for doc in documents]

@tool
def create_reservation(data: ReservationData) -> str:
    """
    Placeholder tool to create a reservation in the system.
    Currently not implemented.
    """
    return f"Received reservation request for {data.nombre}, but reservation creation is not yet implemented."


if __name__ == "__main__":
    print(check_availability.invoke({"checkin": "2025-03-11T14:00:00", "checkout": "2025-03-15T11:00:00"}))
    print(get_info.invoke({"query": "What services does the hotel offer?"}))
    print(create_reservation.invoke({
        "data": {
            "nombre": "John Doe",
            "checkin": "2025-05-01T14:00:00",
            "checkout": "2025-05-05T11:00:00",
            "departamento": 3
        }
    }))
