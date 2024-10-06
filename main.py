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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends explanation on how to use the bot."""
    await update.message.reply_text("Utiliza /profits para comenzar y /stop para dejar de recibir informacion")

def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

async def profit(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send the alarm message."""
    job = context.job
    for lista in list_of_arb_sym:
        try:
            a = getPrice(lista[0])
            b = getPrice(lista[1])
            c = getPrice(lista[2])

            profit = 1 / float(a) * 1 / float(b) * float(c)

            await context.bot.send_message(job.chat_id, text=f"|{lista[0]} -> {lista[1]} -> {lista[2]}| = {profit}")
        except:
            continue

async def send_profits(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Add a job to the queue."""
    chat_id = update.effective_message.chat_id

    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_once(profit, 86400, chat_id=chat_id, name=str(chat_id))



async def unset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Remove the job if the user changed their mind."""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "Timer successfully cancelled!" if job_removed else "You have no active timer."
    await update.message.reply_text(text)

if __name__ == '__main__':
    load_dotenv()

    token = os.getenv("TOKEN")

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler(["start", "help"], start))
    application.add_handler(CommandHandler("profits", send_profits))
    application.add_handler(CommandHandler("stop", unset))

    application.run_polling(allowed_updates=Update.ALL_TYPES)
