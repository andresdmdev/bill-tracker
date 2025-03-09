"""Lambda function for handling Telegram bot events and commands."""

import logging
import asyncio
import json
import os
import traceback
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from services.handlers import echo_document, echo_text, echo_voice, process_photo, start
from utils.utils import load_env, validate_event

logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_env()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

def lambda_handler(event, context):
    """Lambda handler for handling Telegram bot events and commands."""
    return asyncio.get_event_loop().run_until_complete(main(event, context))

async def main(event, context = None):
    """Main function for handling Telegram bot events and commands."""
    logging.info("Validating event...")

    try:
        validate_event(event)

        logging.info("Starting application")
        await application.initialize()
        await application.start()

        ## Add handlers
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT, echo_text))
        application.add_handler(MessageHandler(filters.PHOTO, process_photo))
        application.add_handler(MessageHandler(filters.Document.IMAGE, echo_document))
        application.add_handler(MessageHandler(filters.VOICE, echo_voice))

        update = Update.de_json(event, application.bot)

        logging.info("----> Event Data: %s", json.dumps(event))

        if not update:
            raise ValueError("Update inválido")

        await application.process_update(update)

        return { 'statusCode': 200, 'body': 'Success' }

    except Exception as exc:
        error_data = getattr(exc, "args", [{}])[0] if getattr(exc, "args", None) else {}

        logging.error("Error - Event structure: %s", json.dumps(event))
        logging.error("Error detallado: %s", traceback.format_exc())
        return {
          'statusCode': error_data.get("statusCode", 500),
          'body': error_data.get("message", "Error desconocido")
        }

    finally:
        if application.running:
            logging.info("Stopping application")
            await application.stop()
