import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, InlineQueryHandler, MessageHandler, filters
from functions import handle_voice, handle_tts

load_dotenv()

apiKey = os.getenv("API_KEY")

application = Application.builder().token(apiKey).build()

application.add_handler(MessageHandler(filters.VOICE, handle_voice))
application.add_handler(InlineQueryHandler(handle_tts))

print("Bot running")
application.run_polling()