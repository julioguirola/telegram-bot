import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
import os
from dotenv import load_dotenv
import requests
import json
from symbols import list_of_arb_sym

user_states = {}

def getPrice (symbol):
    response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    return json.loads(response.text)["price"]

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = True

    for lista in list_of_arb_sym:
        try:
            a = getPrice(lista[0])
            b = getPrice(lista[1])
            c = getPrice(lista[2])

            profit = 1 / float(a) * 1 / float(b) * float(c)

            if user_states.get(user_id, False): await context.bot.send_message(chat_id=update.effective_chat.id, text=f"|{lista[0]} -> {lista[1]} -> {lista[2]}| = {profit}")
        except:
            continue

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_states[user_id] = False
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Deteniendo actualizaciones. Usa /start para reanudar.")

if __name__ == '__main__':
    load_dotenv()

    token = os.getenv("TOKEN")

    application = ApplicationBuilder().token(token).build()

    start_handler = CommandHandler('start', start)
    stop_handler = CommandHandler('stop', stop)

    application.add_handler(start_handler)
    application.add_handler(stop_handler)

    application.run_polling()
