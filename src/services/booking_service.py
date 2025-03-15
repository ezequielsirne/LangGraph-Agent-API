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
        
        print("🔵 Payload enviado:", payload)
        print("🔵 Respuesta de la API:", response.json())  # Verifica el JSON completo

        if response.status_code == 200 and response.json().get("isSuccess"):
            self.token = response.json()["result"]["token"]  # Extrae el token correctamente
            print(f"✅ Autenticación exitosa. Token recibido: {self.token[:10]}...")  # Muestra solo parte del token
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
        
    def get_states(self):
        """Obtiene el catálogo de estados."""
        if not self.token:  # Si no hay token, intentamos autenticarnos de nuevo
            self.authenticate()

        url = f"{self.base_url}/api/estados"
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.session.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:  # Token expirado o inválido
            print("⚠️ Token expirado. Obteniendo uno nuevo...")
            self.authenticate()
            return self.get_reservations()  # Reintentar con nuevo token
        else:
            raise Exception(f"❌ Error al obtener estados: {response.text}")

# Test rápido si se ejecuta directamente
if __name__ == "__main__":
    api = BookingService()
    states = api.get_states()
    reservations = api.get_reservations()

    # Mostrar todos los estados para analizar su estructura
    if states:
        from pprint import pprint
        pprint(states)  # Muestra todos los estados
    else:
        print("No hay estados disponibles.")
        
    # Mostrar solo la primera reserva para analizar su estructura
    if reservations:
        from pprint import pprint
        pprint(reservations[:10])  # Muestra solo la primera reserva
    else:
        print("No hay reservas disponibles.")