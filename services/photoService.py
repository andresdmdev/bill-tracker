import json, os, requests, base64
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from io import BytesIO

class PhotoService:
    def __init__(self):
        self.token = os.getenv('TELEGRAM_TOKEN')
        self.base_url_telegram = f"https://api.telegram.org/bot{self.token}"
        self.file_url_telegram = f"https://api.telegram.org/file/bot{self.token}"
        self.photo_base64 = ""
        self.photo_data = ""

    def get_file_path_from_telegram(self, file_id) -> str:
        url = f"{self.base_url_telegram}/getFile"
        response = requests.get(url, params={'file_id': file_id})
        return response.json()['result']['file_path']

    def download_photo_from_telegram(self, file_path) -> bytes:
        url = f"{self.file_url_telegram}/{file_path}"
        response = requests.get(url)
        return response.content

    def get_data_photo(self, file_id) -> bool:
        file_path = self.get_file_path_from_telegram(file_id)

        if not file_path:
          return False

        self.photo_data = self.download_photo_from_telegram(file_path)

        if not self.photo_data:
          return False

        self.photo_base64 = base64.b64encode(self.photo_data).decode('utf-8')

        return True

    async def save_photo_to_google_drive(self, photo_data, folder_id, filename="photo.jpg", is_base64=True):
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
              'name': filename,
              'parents': [folder_id]
          }
          
          # Usar MediaIoBaseUpload en lugar de MediaFileUpload
          media = MediaIoBaseUpload(
              file_buffer,
              mimetype='image/jpeg',
              resumable=True
          )
          
          file = service.files().create(
              body=file_metadata,
              media_body=media,
              fields='id'
          ).execute()
          
          return file.get('id')
        
        except Exception as e:
          print(f"Error detallado: {str(e)}")
          raise Exception(f"Error al subir a Google Drive: {str(e)}")

