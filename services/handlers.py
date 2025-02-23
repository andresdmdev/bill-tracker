import os
from telegram import Update
from telegram.ext import ContextTypes

from services.photoService import PhotoService

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! - Hosted in AWS Lambda")

async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")

async def echo_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  photo_service = PhotoService()
  photo_service.save_photo(update.message.photo[len(update.message.photo) - 1].file_id, "photoBase64.txt", "photo.jpg")
  print(f"Photo saved to photo.jpg")

  folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

  file_id = await photo_service.save_photo_to_google_drive(
    photo_service.photo_base64, 
    folder_id,
    filename="photo.jpg", 
    is_base64=True
  )
  print(f"Photo saved to Google Drive with ID: {file_id}")

  ## Obtener la imagen en base64 -- Listo
  ## Guardar en google drive
  ## Analizar con AI
  ## Obtener los valores que vamos a guardar en dbfile_id
  ## Guardar en base de datos
  ## Enviar notificacion por correo - opcional
  ## Devolver respuesta al usuario
  await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Photo saved to Google Drive with ID: {file_id}")

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")

async def echo_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")