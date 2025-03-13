"""Telegram bot handlers for processing different types of messages and commands."""

import logging
import os
from datetime import datetime
from telegram import Update
from telegram.ext import ContextTypes

from services.photo_service import PhotoService
date_now = datetime.now()

logger = logging.getLogger()
logger.setLevel(logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a welcome message when the command /start is issued."""
    response = "I'm a bot, please talk to me! - Hosted in AWS Lambda"
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message text."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")

async def process_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Process and store photos sent by users."""
    start_time = date_now
    logger.info("Procesando foto...")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Procesando foto...")

    photo_service = PhotoService()
    last_photo = update.message.photo[len(update.message.photo) - 1]
    response = { "msg": "Procesando foto...", "error": False, "error_msg": None }

    if not photo_service.get_data_photo_from_telegram(last_photo.file_id):
        response["error"] = True
        response["error_msg"] = "No se pudo obtener la foto desde telegram 😭"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response["error_msg"])
        return

    file_id = await photo_service.save_photo_to_google_drive(
            photo_service.photo_base64,
            os.getenv('GOOGLE_DRIVE_FOLDER_ID'),
            is_base64=True
        )

    if not file_id:
        response["error"] = True
        response["error_msg"] = "No se pudo guardar la foto en google drive 😭"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response["error_msg"])

    photo_service.upload_image_in_bucket()

    logger.info("🔍 Analizando foto...")
    await context.bot.send_message(chat_id=update.effective_chat.id, text="🔍 Analizando foto...")
    content = photo_service.get_analysis_photo(photo_service.create_thread_with_image())
    logger.info(content)

    try:
        photo_service.save_analysis_photo(content)
        photo_service.insert_bill_data_in_sheet_row()
    except Exception as e:
        execution_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        logger.error("Error al guardar la factura: %s | %s", str(e), execution_time_ms)
        response["error"] = True
        response["error_msg"] = "No se pudo guardar la factura 😭"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response["error_msg"])
        return

    response["msg"] = "Ya guardamos la foto!! 🥳"

    execution_time_ms = (datetime.now() - start_time).total_seconds() * 1000
    logger.info("Ya guardamos la foto!! 🥳 | Execution time: %.2f ms", execution_time_ms)

    await context.bot.send_message(chat_id=update.effective_chat.id, text=response["msg"])

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle voice messages sent by users."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")

async def echo_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process document files sent by users."""
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Not implemented")
