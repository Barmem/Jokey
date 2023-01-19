import argparse
import logging
import sqlaccess 
import convo
from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import time

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# Parse command line arguments
parser = argparse.ArgumentParser(description='Телеграм бот для обработки запросов проезда на территорию')
parser.add_argument('userbot_token', help='Токен бота')
parser.add_argument('security_token', help='Токен бота')
parser.add_argument('Register_token', help='Токен бота')
parser.add_argument('--host', help='Хост БД')
parser.add_argument('--user', help='Имя пользователя БД')
parser.add_argument('--password', help='пароль БД')
parser.add_argument('--database', help='Имя БД')
parser.add_argument('--admin', help='TelegramID администратора')
args = parser.parse_args()
updaterRegister = Updater(args.Register_token, use_context=True)
# def start(update, context):
#     """Send a message when the command /start is issued."""
#     update.message.reply_text('Приветствую, я бот для запроса пропуска на территорию, используйте команды в меню слева снизу.')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def sql(update, context, host, user, password, database,  param = ""):
    records = sqlaccess.get_records(
        f"SELECT * FROM People WHERE `Telegram ID`= {update.effective_user.id}"
        )
    update.message.reply_text(f"{records}")

def searchDB(update, context):
    current_timestamp = round(time.time())
    records = sqlaccess.get_records(
        f"SELECT * FROM Passes WHERE (`Request Time` < FROM_UNIXTIME({current_timestamp}) AND `Expiration Time` > FROM_UNIXTIME({current_timestamp})) AND (`Car Number` LIKE '{update.message.text}' OR `Surname` LIKE '{update.message.text}')"
        )
    result = []
    for record in records:
        print(record)
        if(record[8] == 1):
            result.append(record[1])
        if(record[8] == 2):
            result.append(record[2])
    
    update.message.reply_text(f"{result}")

def registerDB(update, context):
    list = update.message.text.split('+')
    sqlaccess.insert_records(
        f"INSERT INTO People (Surname, Name, `Father Name`, `Telegram ID`, `Phone Number`, Street, Building, Apartment, `Role ID`) VALUES ('{list[0]}', '{list[1]}', '{list[2]}', '{list[3]}', '{list[4]}', '{list[5]}', '{list[6]}', '{list[7]}', '{list[8]}')",
    )

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Telegram Userbot error: "%s"',  context.error)

def errorSec(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Telegram SecurityBot error: "%s"',  context.error)

def main():
    
    #---------------------------- User Bot ----------------------------
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updaterUser = Updater(args.userbot_token, use_context=True)

    # Get the dispatcher to register handlers
    dp = updaterUser.dispatcher

    passRequestConvo_handler = convo.startConvo()

    # Add the conversation handler to the dispatcher
    dp.add_handler(passRequestConvo_handler)

    # on different commands - answer in Telegram
    # dp.add_handler(CommandHandler("help", help))

    # log all errors
    dp.add_error_handler(error)
    #---------------------------- User Bot END ------------------------


    #---------------------------- Security Bot ------------------------
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updaterSecurity = Updater(args.security_token, use_context=True)

    # Get the dispatcher to register handlers
    dp2 = updaterSecurity.dispatcher

    # Add the conversation handler to the dispatcher
    # dp2.add_handler(passRequestConvo_handler)

    # on different commands - answer in Telegram
    dp2.add_handler(MessageHandler(Filters.text, searchDB))
    # dp.add_handler(CommandHandler("help", help))
    # dp.add_handler(CommandHandler("sql", lambda update, context: sql(update, context, args.host, args.user, args.password, args.database) ))

    # log all errors
    dp2.add_error_handler(errorSec)
    #---------------------------- Security Bot  END -------------------
    

    #---------------------------- Register Bot ------------------------
    dp3 = updaterRegister.dispatcher
    dp3.add_handler(MessageHandler(Filters.text, registerDB))


    # Get the dispatcher to register handlers
    # dp3 = updaterRegister.dispatcher
    # updaterRegister.bot.send_message(chat_id=f"{args.admin}", text="test")
    #---------------------------- Register Bot  END -------------------


    # Start the Bot
    updaterSecurity.start_polling()
    updaterUser.start_polling()
    updaterRegister.start_polling()


    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updaterSecurity.idle()
    updaterUser.idle()
    updaterRegister.idle()

if __name__ == '__main__':
    main()
