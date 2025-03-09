"""Repository for interacting with the bill tracking database through Supabase API."""

import os
import logging
from supabase import create_client, Client
from models.bill import Bill

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class BillTrackerRepository:
    """Repository for interacting with the bill tracking database through Supabase API."""

    def __init__(self):
        url: str = os.getenv("SUPABASE_URL")
        key: str = os.getenv("SUPABASE_KEY")

        if not url or not key:
            logger.error("Error: SUPABASE_URL o SUPABASE_KEY no están configurados en las variables de entorno")
            return

        logger.info("Conectando a Supabase: URL=%s... KEY=%s...", url[:10], key[:5])
        self.supabase: Client = create_client(url, key)

    def register_user(self, email: str, password: str):
        """Registers a new user in Supabase"""
        try:
            logger.info("Intentando registrar usuario: %s", email)
            response = self.supabase.auth.sign_up({
              "email": email,
              "password": password
            })
            logger.info("Usuario registrado exitosamente")
            return response
        except Exception as e:
            logger.error("Error al registrar el usuario: %s", str(e))
            # Mostrar más detalles del error si están disponibles
            if hasattr(e, 'message'):
                logger.error("Mensaje de error: %s", e.message)
            return None

    def authenticate_user(self, email: str, password: str):
        """Autentica un usuario existente en Supabase"""
        try:
            logger.info("Intentando autenticar usuario: %s", email)
            # Verificar que los datos no estén vacíos
            if not email or not password:
                logger.error("Error: Email o contraseña vacíos")
                return None

            response = self.supabase.auth.sign_in_with_password({
              "email": email,
              "password": password
            })
            logger.info("Usuario autenticado exitosamente")
            return response
        except Exception as e:
            logger.error("Error al autenticar el usuario: %s", str(e))
            # Mostrar más detalles del error si están disponibles
            if hasattr(e, 'message'):
                logger.error("Mensaje de error: %s", e.message)
            return None

    def insert_bill(self, bill: Bill):
        """Inserta una factura en la tabla BillTracker"""
        try:
            # Verificar si el usuario está autenticado
            user = self.supabase.auth.get_user()
            if not user:
                logger.error("Error: Usuario no autenticado. Debes iniciar sesión primero.")
                return None

            bill = bill.to_json_db()

            logger.info("Insertando factura: %s", bill)
            response = self.supabase.table("BillTracker").insert(bill).execute()
            logger.info("Factura insertada exitosamente")
            return response.data
        except Exception as e:
            logger.error("Error al insertar la factura: %s", str(e))
            if hasattr(e, 'message'):
                logger.error("Mensaje de error: %s", e.message)
            return None

    def upload_image_in_bucket(self, bucket_name, image_data, file_path):
        """Upload an image to a bucket in Supabase"""
        try:
            # Especificar el tipo MIME como image/jpeg
            file_options = {
                "content-type": "image/jpeg"  # O "image/png" dependiendo del tipo de imagen
            }
            self.supabase.storage.from_(bucket_name).upload(file_path, image_data, file_options=file_options)
        except Exception as e:
            logger.error("Error al subir imagen a Supabase: %s", str(e))
            return None

    def get_public_url_image(self, bucket_name, file_path):
        """Get the public URL of an image from a bucket in Supabase"""
        try:
            return self.supabase.storage.from_(bucket_name).get_public_url(file_path)
        except Exception as e:
            logger.error("Error al obtener URL pública de la imagen: %s", str(e))
            return None
