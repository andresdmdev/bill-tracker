import os
from dotenv import load_dotenv, find_dotenv

def load_env():
  _ = load_dotenv(find_dotenv())

def validate_event(event):
  load_env()
  if not event:
    raise ValueError({ "message": "Event is required", "statusCode": 400 })
  
  if not event.get("update_id"):
    raise ValueError({ "message": "Update ID is required", "statusCode": 400 })
  
  if not event.get("message"):
    raise ValueError({ "message": "Message is required", "statusCode": 400 })
  
  if not event.get("message").get("chat"):
    raise ValueError({ "message": "Chat is required", "statusCode": 400 })
  
  event_chat_id = event.get("message").get("chat").get("id")

  if not event_chat_id:
    raise ValueError({ "message": "Chat ID is required", "statusCode": 401 })
  
  chat_ids = os.getenv("CHAT_IDS", {})

  if str(event_chat_id) not in chat_ids:
    raise Exception({ "message": "Chat ID is not allowed", "statusCode": 401 })

  return