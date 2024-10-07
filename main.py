import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
from dotenv import load_dotenv
import requests
import json
from symbols import list_of_arb_sym

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

def getPrice (symbol):
    response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
    return json.loads(response.text)["price"]


async def profit(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    for lista in list_of_arb_sym:
        try:
            a = getPrice(lista[0])
            c = getPrice(lista[2])

            profit = float(a) * float(c)

            await context.bot.send_message(job.chat_id, text=f"|{lista[0]} -> {lista[1]} -> {lista[2]}| = {profit}")
        except:
            print("error")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id

    context.job_queue.run_once(profit, 1, chat_id=chat_id, name=str(chat_id))



if __name__ == '__main__':
    load_dotenv()

    token = os.getenv("TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
