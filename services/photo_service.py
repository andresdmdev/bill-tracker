"""Service for handling photo operations."""
from datetime import datetime
import json
import os
import base64
import uuid
import logging
from io import BytesIO
import time
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from openai import OpenAI
from models.bill import Bill, BillStatus
from repository.bill_tracker_repository import BillTrackerRepository

logger = logging.getLogger()
logger.setLevel(logging.INFO)

date_now = datetime.now()

class PhotoService:
    """Service for handling photo operations."""
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.base_url_telegram = f"https://api.telegram.org/bot{self.token}"
        self.file_url_telegram = f"https://api.telegram.org/file/bot{self.token}"
        self.photo_base64 = ""
        self.photo_data = ""
        self.photo_name = ""
        self.photo_url = ""
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.bill_tracker_repository = BillTrackerRepository()
        self.bill_tracker_repository.authenticate_user(os.getenv('USER_EMAIL'), os.getenv('USER_PASSWORD'))

    def get_file_path_from_telegram(self, file_id) -> str:
        """Get the file path from Telegram."""
        url = f"{self.base_url_telegram}/getFile"
        response = requests.get(url, params={'file_id': file_id}, timeout=10)
        return response.json()['result']['file_path']

    def download_photo_from_telegram(self, file_path) -> bytes:
        """Download the photo from Telegram."""
        url = f"{self.file_url_telegram}/{file_path}"
        response = requests.get(url, timeout=10)
        return response.content

    def get_data_photo_from_telegram(self, file_id) -> bool:
        """Get the data photo from Telegram."""
        file_path = self.get_file_path_from_telegram(file_id)

        if not file_path:
            return False

        self.photo_data = self.download_photo_from_telegram(file_path)

        if not self.photo_data:
            return False

        self.photo_base64 = base64.b64encode(self.photo_data).decode('utf-8')

        self.photo_name = f"{uuid.uuid4()}.jpeg"

        return True

    async def save_photo_to_google_drive(self, photo_data, folder_id, is_base64=True):
        """Save the photo to Google Drive."""
        try:
            credentials_json = json.loads(os.getenv('GOOGLE_CREDENTIALS'))
            credentials = service_account.Credentials.from_service_account_info(
                credentials_json,
                scopes=['https://www.googleapis.com/auth/drive.file']
            )

            service = build('drive', 'v3', credentials=credentials)

            # Preparar los datos según el formato
            if is_base64:
                photo_bytes = base64.b64decode(photo_data)
            else:
                photo_bytes = photo_data

            # Crear archivo temporal en memoria
            file_buffer = BytesIO(photo_bytes)

            # Agregar el ID de la carpeta donde se guardará
            file_metadata = {
                'name': self.photo_name,
                'parents': [folder_id]
            }

            # Usar MediaIoBaseUpload en lugar de MediaFileUpload
            media = MediaIoBaseUpload(
                file_buffer,
                mimetype='image/jpeg',
                resumable=True
            )

            # pylint: disable=no-member
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            # pylint: enable=no-member

            return file.get('id')

        except Exception as e:
            logger.error("Error al subir a Google Drive: %s", str(e))
            raise IOError(f"Error al subir a Google Drive: {str(e)}") from e

    def upload_image_in_bucket(self):
        """Upload the image to the bucket."""
        try:
            self.bill_tracker_repository.upload_image_in_bucket(os.getenv('BUCKET_NAME'), self.photo_data, self.photo_name)
            self.photo_url = self.bill_tracker_repository.get_public_url_image(os.getenv('BUCKET_NAME'), self.photo_name)
        except Exception as e:
            logger.error("Error al subir la imagen al bucket: %s", str(e))
            raise ValueError(f"Error al subir la imagen al bucket: {str(e)}") from e

    def create_thread_with_image(self):
        """Create a thread with the image."""

        # Ensure we have image data
        if not self.photo_url:
            raise ValueError("No image data available. Call get_data_photo_from_telegram first.")

        try:
            # Crear el thread
            thread = self.client.beta.threads.create()

            # Intentar crear el mensaje con la imagen
            self.client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=[
                    {
                        "type": "text",
                        "text": "Por favor, analiza la imagen"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": self.photo_url
                        }
                    }
                ]
            )
            return thread.id

        except Exception as e:
            logger.error("Error al crear thread con imagen: %s", str(e))
            raise RuntimeError(f"Error al crear thread con imagen: {str(e)}") from e

    def get_analysis_photo(self, thread_id):
        """Get the analysis of the photo."""

        run = self.client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=os.getenv("OPENAI_ASSISTANT_ID")
        )

        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id
            )

            if run_status.status == "completed":
                break

            if run_status.status == "failed":
                logger.error("Error: %s", str(run_status.last_error))
                return None

            # Esperar antes de verificar de nuevo
            time.sleep(1)

        messages = self.client.beta.threads.messages.list(
            thread_id=thread_id
        )

        for message in messages.data:
            if message.role == "assistant":
                content = ""
                for content_part in message.content:
                    if content_part.type == "text":
                        content += content_part.text.value
                return content

        return "No se recibió respuesta del asistente."

    def save_analysis_photo(self, content):
        """Save the analysis of the photo."""

        if not content:
            logger.error("No se recibió respuesta del asistente.")
            raise ValueError("No se recibió respuesta del asistente.")

        try:
            content = json.loads(content)

            bill = Bill(
                date=date_now.strftime("%Y-%m-%d %H:%M:%S"),
                category=content.get("CATEGORY").lower().capitalize(),
                medium=content.get("MEDIUM").lower().capitalize(),
                amount="0",
                status=BillStatus.Unpaid,
                notes=content.get("NOTES")
            )

            self.bill_tracker_repository.insert_bill(bill)

        except Exception as e:
            logger.error("Error al guardar la factura: %s", str(e))
            raise ValueError(f"Error al guardar la factura: {str(e)}") from e
