"""Repository for interacting with the bill tracking database through Supabase API."""

import os
import sys

from supabase import create_client, Client
from models.bill import Bill
from utils.utils import load_env

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class BillTrackerRepository:
    """Repository for interacting with the bill tracking database through Supabase API."""

    def __init__(self):
        load_env()  # Asegurarse de cargar las variables de entorno
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")

        if not url or not key:
            print("Error: SUPABASE_URL o SUPABASE_KEY no están configurados en las variables de entorno")
            return

        print(f"Conectando a Supabase: URL={url[:10]}... KEY={key[:5]}...")
        self.supabase: Client = create_client(url, key)

    def register_user(self, email: str, password: str):
        """Registers a new user in Supabase"""
        try:
            print(f"Intentando registrar usuario: {email}")
            response = self.supabase.auth.sign_up({
              "email": email,
              "password": password
            })
            print("Usuario registrado exitosamente")
            return response
        except Exception as e:
            print(f"Error al registrar el usuario: {e}")
            # Mostrar más detalles del error si están disponibles
            if hasattr(e, 'message'):
                print(f"Mensaje de error: {e.message}")
            return None

    def authenticate_user(self, email: str, password: str):
        """Autentica un usuario existente en Supabase"""
        try:
            print(f"Intentando autenticar usuario: {email}")
            # Verificar que los datos no estén vacíos
            if not email or not password:
                print("Error: Email o contraseña vacíos")
                return None

            response = self.supabase.auth.sign_in_with_password({
              "email": email,
              "password": password
            })
            print("Usuario autenticado exitosamente")
            return response
        except Exception as e:
            print(f"Error al autenticar el usuario: {e}")
            # Mostrar más detalles del error si están disponibles
            if hasattr(e, 'message'):
                print(f"Mensaje de error: {e.message}")
            return None

    def insert_bill(self, bill: Bill):
        """Inserta una factura en la tabla BillTracker"""
        try:
            # Verificar si el usuario está autenticado
            user = self.supabase.auth.get_user()
            if not user:
                print("Error: Usuario no autenticado. Debes iniciar sesión primero.")
                return None

            bill = bill.to_json_db()

            print(f"Insertando factura: {bill}")
            response = self.supabase.table("BillTracker").insert(bill).execute()
            print("Factura insertada exitosamente")
            return response.data
        except Exception as e:
            print(f"Error al insertar la factura: {e}")
            if hasattr(e, 'message'):
                print(f"Mensaje de error: {e.message}")
            return None
