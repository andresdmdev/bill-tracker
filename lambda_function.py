import logging, asyncio, json, os, base64
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import traceback

logging.basicConfig(
  format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
  level=logging.INFO
)

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')
application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

def lambda_handler(event, context):
  return asyncio.get_event_loop().run_until_complete(main(event, context))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
  await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me! - Hosted in AWS Lambda")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
  response = "chao"
  await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def main(event, context):
  try:
    logging.info("Starting application")
    await application.initialize()
    await application.start()

    ## Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT, echo))

    ## Process update
    body = event.get('body', '{}')
    
    if event.get('isBase64Encoded', False):
      body = base64.b64decode(body).decode('utf-8')
    
    logging.info(f"---- Body: {body}")

    update = Update.de_json(event, application.bot)

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