import config
from bot import *
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

app = ApplicationBuilder().token(config.TOKEN).build()

app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.TEXT, text))

print('Server start')
app.run_polling()