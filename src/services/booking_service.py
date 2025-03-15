import os
import requests
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de la API
API_BASE_URL = "http://sdtsoftware-001-site14.atempurl.com"
USERNAME = os.getenv("BOOKING_API_USER")
PASSWORD = os.getenv("BOOKING_API_PASS")

class BookingService:
    def __init__(self):
        self.base_url = API_BASE_URL
        self.session = requests.Session()
        self.token = None  # Se inicializa vacío para evitar errores en los headers
        self.authenticate()  # Se obtiene el token al inicializar el servicio

    def authenticate(self):
        """Autentica al usuario y obtiene un token de sesión."""
        url = f"{self.base_url}/api/users/login"
        payload = {"nick": USERNAME, "password": PASSWORD}
        response = self.session.post(url, json=payload)
        print("Payload:", payload)

        if response.status_code == 200:
            self.token = response.json().get("token")  # Guardamos el token en la instancia
            print("✅ Autenticación exitosa.")
        else:
            raise Exception(f"❌ Error de autenticación: {response.text}")

    def get_reservations(self):
        """Obtiene la lista de reservas."""
        if not self.token:  # Si no hay token, intentamos autenticarnos de nuevo
            self.authenticate()

        url = f"{self.base_url}/api/reservas"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:  # Token expirado o inválido
            print("⚠️ Token expirado. Obteniendo uno nuevo...")
            self.authenticate()
            return self.get_reservations()  # Reintentar con nuevo token
        else:
            raise Exception(f"❌ Error al obtener reservas: {response.text}")

# Test rápido si se ejecuta directamente
if __name__ == "__main__":
    api = BookingService()
    print("Reservas existentes:", api.get_reservations())
