"""Telegram bot handlers for processing different types of messages and commands."""

import os
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from models.bill import Bill, BillStatus
from repository.bill_tracker_repository import BillTrackerRepository
from services.photo_service import PhotoService

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    response = "I'm a bot, please talk to me! - Hosted in AWS Lambda"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message text."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")

async def echo_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process and store photos sent by users."""
    photo_service = PhotoService()
    last_photo = update.message.photo[len(update.message.photo) - 1]

    if not photo_service.get_data_photo_from_telegram(last_photo.file_id):
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

    bill_tracker_repository = BillTrackerRepository()
    bill_tracker_repository.authenticate_user(os.getenv('USER_EMAIL'), os.getenv('USER_PASSWORD'))

    bill = Bill(
        date=date_now,
        category=None, ## TODO: Obtener el valor de la foto
        medium=None, ## TODO: Obtener el valor de la foto
        amount=0, ## TODO: Obtener el valor de la foto
        status=BillStatus.Unpaid
    )

    bill_tracker_repository.insert_bill(bill)

    response = "Ya guardamos la foto!! 🥳"
    ## Analizar con AI
    ## Obtener los valores que vamos a guardar en dbfile_id
    ## Guardar en base de datos
    ## Enviar notificacion por correo - opcional
    ## Devolver respuesta al usuario
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages sent by users."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")

async def echo_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process document files sent by users."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")
