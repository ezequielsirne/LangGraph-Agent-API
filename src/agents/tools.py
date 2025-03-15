from datetime import datetime
from langchain_core.tools import tool
from src.services.booking_service import BookingService

# Instancia del servicio de reservas
booking_service = BookingService()

# Lista de departamentos disponibles
ALL_APARTMENTS = {1, 2, 3, 5, 6, 7, 8}

@tool
def check_availability(checkin: str, checkout: str) -> dict:
    """
    Checks the availability of hotel apartments between two given dates.

    :param checkin: Start date (ISO 8601 format, e.g., "2025-03-11T14:00:00")
    :param checkout: End date (ISO 8601 format, e.g., "2025-03-15T11:00:00")

    :return: A dictionary with available and occupied apartments.
    Example output:
    {
        "available_apartments": [2, 3, 5],
        "occupied_apartments": [
            {"apartment": 1, "checkin": "2025-03-11T14:00:00", "checkout": "2025-03-15T11:00:00"},
            {"apartment": 7, "checkin": "2025-03-12T14:00:00", "checkout": "2025-03-14T11:00:00"}
        ]
    }
    """
    try:
        checkin_date = datetime.fromisoformat(checkin)
        checkout_date = datetime.fromisoformat(checkout)
    except ValueError:
        raise ValueError("Invalid date format. Use ISO 8601 (YYYY-MM-DDTHH:MM:SS)")

    reservas = booking_service.get_reservations()

    if not reservas:
        return {"available_apartments": list(ALL_APARTMENTS), "occupied_apartments": []}

    # Filtrar reservas activas y vigentes dentro del rango solicitado
    occupied_reservations = [
        {
            "apartment": reserva["departamento"],
            "checkin": reserva["checkin"],
            "checkout": reserva["checkout"]
        }
        for reserva in reservas
        if reserva["eliminado"] == 0 and reserva["estado"] > 0 and (
            (datetime.fromisoformat(reserva["checkin"]) < checkout_date) and
            (datetime.fromisoformat(reserva["checkout"]) > checkin_date)
        )
    ]

    # Extraer los departamentos ocupados
    occupied_apartments = {reserva["apartment"] for reserva in occupied_reservations}

    # Determinar los departamentos disponibles
    available_apartments = list(ALL_APARTMENTS - occupied_apartments)

    return {
        "available_apartments": available_apartments,
        "occupied_apartments": occupied_reservations
    }
