import unittest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from src.agents.tools import check_availability, get_info

class TestCheckAvailability(unittest.TestCase):

    @patch("src.services.booking_service.BookingService.get_reservations")
    def test_check_availability(self, mock_get_reservations):
        """Test that check_availability correctly identifies available and occupied apartments."""

        # Test dates
        checkin_date = datetime.now() + timedelta(days=1)
        checkout_date = datetime.now() + timedelta(days=5)

        # Mocked reservation data
        mock_get_reservations.return_value = [
            {
                "departamento": 1,
                "checkin": (datetime.now() + timedelta(days=1)).isoformat(),
                "checkout": (datetime.now() + timedelta(days=4)).isoformat(),
                "estado": 1,
                "eliminado": 0,
            },
            {
                "departamento": 7,
                "checkin": (datetime.now() + timedelta(days=3)).isoformat(),
                "checkout": (datetime.now() + timedelta(days=6)).isoformat(),
                "estado": 1,
                "eliminado": 0,
            }
        ]

        result = check_availability.invoke({
            "checkin": checkin_date.isoformat(),
            "checkout": checkout_date.isoformat()
        })

        self.assertIsInstance(result, dict)
        self.assertIn("available_apartments", result)
        self.assertIn("occupied_apartments", result)
        self.assertEqual(len(result["available_apartments"]), 5)
        self.assertNotIn(1, result["available_apartments"])
        self.assertNotIn(7, result["available_apartments"])
        self.assertEqual(len(result["occupied_apartments"]), 2)


class TestGetInfo(unittest.TestCase):

    @patch("src.agents.vector_db.get_retriever")
    def test_get_info_returns_data(self, mock_get_retriever):
        """Test that get_info retrieves relevant information from the vector database."""
        mock_retriever = MagicMock()
        mock_retriever.get_relevant_documents.return_value = [
            MagicMock(page_content="The hotel offers breakfast and spa services."),
            MagicMock(page_content="There is also a pool and free Wi-Fi."),
        ]
        mock_get_retriever.return_value = mock_retriever

        result = get_info.invoke("What services does the hotel offer?")
        self.assertIsInstance(result, str)
        self.assertIn("desayuno", result)
        self.assertIn("Wi-Fi", result)


if __name__ == "__main__":
    unittest.main()
