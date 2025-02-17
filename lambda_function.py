import logging, asyncio, json, os, traceback
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from utils import load_env

logger = logging.getLogger()
logger.setLevel(logging.INFO)

load_env()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

def lambda_handler(event, context):
  return asyncio.get_event_loop().run_until_complete(main(event, context))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! - Hosted in AWS Lambda")

async def echo_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
  response = "local - Tests - Text"
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def echo_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  response = "local - Tests - Photo"
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def echo_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
  response = "local - Tests - Voice"
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def echo_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
  response = "local - Tests - Document"
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response)

async def main(event, context):
  try:
    logging.info("Starting application")
    await application.initialize()
    await application.start()

    ## Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, echo_text))
    application.add_handler(MessageHandler(filters.PHOTO, echo_photo))
    application.add_handler(MessageHandler(filters.Document.IMAGE, echo_document))
    application.add_handler(MessageHandler(filters.VOICE, echo_voice))

    update = Update.de_json(event, application.bot)

    logging.info(f"----> Event Data: {json.dumps(event)}")

    if not update:
      raise ValueError("Update inválido")

    await application.process_update(update)

    return { 'statusCode': 200, 'body': 'Success' }

  except Exception as exc:
    logging.error(f"Error - Event structure: {json.dumps(event)}")
    logging.error(f"Error detallado: {traceback.format_exc()}")
    return {
      'statusCode': 500,
      'body': 'Failure'
    }
  
  finally:
    logging.info("Stopping application")
    await application.stop()