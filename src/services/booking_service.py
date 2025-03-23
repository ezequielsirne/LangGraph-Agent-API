import requests
from src.config.settings import settings  # Usamos settings centralizados

class BookingService:
    def __init__(self):
        self.base_url = settings.booking_api_url
        self.username = settings.booking_api_user
        self.password = settings.booking_api_pass
        self.session = requests.Session()
        self.token = None
        self.authenticate()

    def authenticate(self):
        """Authenticate the user and obtain a session token."""
        url = f"{self.base_url}/api/users/login"
        payload = {"nick": self.username, "password": self.password}
        response = self.session.post(url, json=payload)
        
        print("Payload sent:", payload)
        print("API response:", response.json())

        if response.status_code == 200 and response.json().get("isSuccess"):
            self.token = response.json()["result"]["token"]
            print(f"Authentication successful. Token received: {self.token[:10]}...")
        else:
            raise Exception(f"Authentication error: {response.text}")

    def get_reservations(self):
        """Get the list of reservations."""
        if not self.token:
            self.authenticate()

        url = f"{self.base_url}/api/reservas"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("Token expired. Re-authenticating...")
            self.authenticate()
            return self.get_reservations()
        else:
            raise Exception(f"Error fetching reservations: {response.text}")
        
    def get_states(self):
        """Get the list of reservation states."""
        if not self.token:
            self.authenticate()

        url = f"{self.base_url}/api/estados"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("Token expired. Re-authenticating...")
            self.authenticate()
            return self.get_states()
        else:
            raise Exception(f"Error fetching states: {response.text}")

if __name__ == "__main__":
    api = BookingService()
    states = api.get_states()
    reservations = api.get_reservations()

    from pprint import pprint

    if states:
        print("\nReservation states:")
        pprint(states)
    else:
        print("No states available.")

    if reservations:
        print("\nFirst 10 reservations:")
        pprint(reservations[:10])
    else:
        print("No reservations found.")
