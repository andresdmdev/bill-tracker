import os
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from services.photoService import PhotoService

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! - Hosted in AWS Lambda")

async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")

async def echo_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  photo_service = PhotoService()

  if not photo_service.get_data_photo(update.message.photo[len(update.message.photo) - 1].file_id):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="No se pudo obtener la foto desde telegram 😭")
    return

  folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')

  date_now = datetime.now()

  file_id = await photo_service.save_photo_to_google_drive(
    photo_service.photo_base64, 
    folder_id,
    filename=date_now.strftime("%Y-%m-%d"), 
    is_base64=True
  )

  if not file_id:
    await context.bot.send_message(chat_id=update.effective_chat.id, text="No se pudo guardar la foto en google drive 😭")
    return

  response = f"Ya guardamos la foto!! 🥳"
  ## Obtener la imagen en base64 -- Listo
  ## Guardar en google drive
  ## Analizar con AI
  ## Obtener los valores que vamos a guardar en dbfile_id
  ## Guardar en base de datos
  ## Enviar notificacion por correo - opcional
  ## Devolver respuesta al usuario
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")

async def echo_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")