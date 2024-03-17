import logging
import os
import time
import random

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ChatAction
from telegram.ext import CallbackContext, CommandHandler, ConversationHandler, Filters, MessageHandler, Updater, CallbackQueryHandler

from liyu import convert_amharic_number

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

ASK_FOR_NUMBER, ASK_FOR_CHOICE = range(2)


EMOJI_THUMBS_UP = "👍"
EMOJI_SMILE = "😊"
EMOJI_LAUGH = "😄"
EMOJI_ERROR = "❌"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a Liyu bot! Please use commands to proceed. " + EMOJI_SMILE)

def tools(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("A Number to Amharic", callback_data='number_to_amharic')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Choose what you want me to do:', reply_markup=reply_markup)
    return ASK_FOR_NUMBER

def receive_number(update: Update, context: CallbackContext):
    number = update.message.text

    if not number.isdigit():
        update.message.reply_text("Please enter a valid number. " + EMOJI_ERROR)
        return ASK_FOR_NUMBER

    context.user_data['number'] = number
    
    GENERAL_BUTTON = "General🔄"
    BIRR_BUTTON = "Birr💵"

    keyboard = [
        [KeyboardButton(GENERAL_BUTTON), KeyboardButton(BIRR_BUTTON)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    update.message.reply_text("Choose one option:", reply_markup=reply_markup)
    return ASK_FOR_CHOICE

def receive_choice(update: Update, context: CallbackContext):
    choice = update.message.text
    number = context.user_data.get('number')  

    GENERAL_BUTTON = "General🔄"
    BIRR_BUTTON = "Birr💵"

    if choice not in (GENERAL_BUTTON, BIRR_BUTTON):
        
        update.message.reply_text("Oops! That's not a valid option. Let's try again! " + EMOJI_ERROR)
        return ASK_FOR_CHOICE

    if not number:
    
        update.message.reply_text("Don't forget to enter a number first! " + EMOJI_SMILE)
        return ASK_FOR_NUMBER


    context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)
    

    
    fun_responses = ["Here you go! ", "Ta-da! ", "Voilà! ", "And here's your result! "]
    response = random.choice(fun_responses)

    result = convert_amharic_number(number, choice[:-1])
    
    update.message.reply_text(response  + EMOJI_THUMBS_UP)
    update.message.reply_text(f"{result} ", reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END

def number_to_amharic(update: Update, context: CallbackContext):
    update.callback_query.answer()
    update.callback_query.edit_message_text(text="Please send me the number you want me to convert to Amharic. " + EMOJI_SMILE)
    return ASK_FOR_NUMBER

def main():
    load_dotenv()
    TOKEN = os.getenv('TOKEN')
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("tools", tools)],
        states={
            ASK_FOR_NUMBER: [MessageHandler(Filters.text & ~Filters.command, receive_number)],
            ASK_FOR_CHOICE: [MessageHandler(Filters.text & ~Filters.command, receive_choice)],
        },
        fallbacks=[],
    )
    dp.add_handler(conv_handler)
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(number_to_amharic, pattern='number_to_amharic'))
    dp.add_handler(CommandHandler("tools", tools))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()