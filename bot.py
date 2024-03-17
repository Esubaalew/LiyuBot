import asyncio
import logging
import os

from dotenv import load_dotenv

from telegram.ext import CommandHandler, Updater

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=f"ሰላም, {update.effective_chat.first_name}  እንዴት ነዎ 🤗! እኔ ልዩ እባላለሁ ።")



def main():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()