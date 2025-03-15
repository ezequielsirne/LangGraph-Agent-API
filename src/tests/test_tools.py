import unittest
from datetime import datetime, timedelta
from unittest.mock import patch
from src.agents.tools import check_availability

class TestCheckAvailability(unittest.TestCase):

    @patch("src.services.booking_service.BookingService.get_reservations")
    def test_check_availability(self, mock_get_reservations):
        """Test that check_availability correctly identifies available and occupied apartments."""

        # Fechas de prueba
        checkin_date = datetime.now() + timedelta(days=1)
        checkout_date = datetime.now() + timedelta(days=5)

        # Datos simulados de reservas
        mock_get_reservations.return_value = [
            {
                "departamento": 1,
                "checkin": (datetime.now() + timedelta(days=1)).isoformat(),
                "checkout": (datetime.now() + timedelta(days=4)).isoformat(),
                "estado": 1,  # ✅ Pendiente (válida)
                "eliminado": 0,
            },
            {
                "departamento": 7,
                "checkin": (datetime.now() + timedelta(days=3)).isoformat(),
                "checkout": (datetime.now() + timedelta(days=6)).isoformat(),
                "estado": 1,  # ✅ Pendiente (válida)
                "eliminado": 0,
            }
        ]

        # Ejecutar la tool
        result = check_availability.invoke({
            "checkin": checkin_date.isoformat(),
            "checkout": checkout_date.isoformat()
        })

        # Evaluar el resultado esperado
        self.assertIsInstance(result, dict)
        self.assertIn("available_apartments", result)
        self.assertIn("occupied_apartments", result)

        # Solo 5 departamentos deben estar disponibles
        self.assertEqual(len(result["available_apartments"]), 5)
        self.assertNotIn(1, result["available_apartments"])  # Está ocupado
        self.assertNotIn(7, result["available_apartments"])  # Está ocupado

        # Debe haber 2 departamentos ocupados
        self.assertEqual(len(result["occupied_apartments"]), 2)

if __name__ == "__main__":
    unittest.main()
