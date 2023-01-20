from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import sqlaccess
import re
import time
# Define the states for the conversation
CAR_INPUT, HUMAN_INPUT, START_REGISTRATION = range(3)

def startConvo():
    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler(['car','human','start'], isreg)],

        states={
            CAR_INPUT: [MessageHandler(Filters.text, car_input)],
            HUMAN_INPUT: [MessageHandler(Filters.text, human_input)],
            START_REGISTRATION: [MessageHandler(Filters.text, surname_input)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler


def isreg(update, context):
    """Start the conversation."""
    records = sqlaccess.get_records(
        f"SELECT * FROM People WHERE `Telegram ID`= {update.effective_user.id}",
        )
    # print(records[0][9])

    command = update.message.text.split()[0][1:]

    if(len(records) != 0):
        if(command == "car"):
            update.message.reply_text('Введите ПОЛНЫЙ номер авто.')
            return CAR_INPUT
            # return ConversationHandler.END
        elif(command == "human"):
            update.message.reply_text('Введите полный ФИО гостя.')
            return HUMAN_INPUT
            # return ConversationHandler.END
        elif(command == "start"):
            update.message.reply_text('Приветствую, я бот для запроса пропуска на территорию, используйте команды в меню слева снизу.')
            return ConversationHandler.END
    else:
        update.message.reply_text("Вы не зарегестрированы. Введите Ваши ФИО, адрес и номер телефона и ждите подтверждения регистрации.")
        return START_REGISTRATION

def car_input(update, context):
    myregex = re.compile(r"^(([АВЕКМНОРСТУХ]\d{3}(?<!000)[АВЕКМНОРСТУХ]{1,2})(\d{2,3})|(\d{4}(?<!0000)[АВЕКМНОРСТУХ]{2})(\d{2})|(\d{3}(?<!000)(C?D|[ТНМВКЕ])\d{3}(?<!000))(\d{2}(?<!00))|([ТСК][АВЕКМНОРСТУХ]{2}\d{3}(?<!000))(\d{2})|([АВЕКМНОРСТУХ]{2}\d{3}(?<!000)[АВЕКМНОРСТУХ])(\d{2})|([АВЕКМНОРСТУХ]\d{4}(?<!0000))(\d{2})|(\d{3}(?<!000)[АВЕКМНОРСТУХ])(\d{2})|(\d{4}(?<!0000)[АВЕКМНОРСТУХ])(\d{2})|([АВЕКМНОРСТУХ]{2}\d{4}(?<!0000))(\d{2})|([АВЕКМНОРСТУХ]{2}\d{3}(?<!000))(\d{2,3})|(^Т[АВЕКМНОРСТУХ]{2}\d{3}(?<!000)\d{2,3}))")
    # А123ВЕ77
    if myregex.match(update.message.text):
        current_timestamp = round(time.time())

        sqlaccess.insert_records(
            f"INSERT INTO Passes (`Car Number`, `People ID`, `Request Time`, `Expiration Time`, `Access ID`) VALUES ('{update.message.text}', (select `People ID` from People where `Telegram ID`='{update.effective_user.id}'), FROM_UNIXTIME({current_timestamp}), FROM_UNIXTIME({current_timestamp + (60*60*24)}), 1)",
        )
        update.message.reply_text('Пропуск авто оформлен.')
        return ConversationHandler.END
    else:
        update.message.reply_text('Неверный номер авто.')
        return ConversationHandler.END
    
    
    # user = update.message.from_user
    # context.user_data['destination'] = update.message.text
    # # button1 = InlineKeyboardButton("Да", callback_data="Yes")
    # # button2 = InlineKeyboardButton("Нет", callback_data="No")
    # keyboard = ReplyKeyboardMarkup([["Yes"], ["no"]], one_time_keyboard=True)
    # # keyboard = InlineKeyboardMarkup([[button1, button2]])
    # update.message.reply_text('Do you want to fly to {}?'.format(update.message.text),
    #                           reply_markup=keyboard)
    # return CONFIRM_DESTINATION
    

def human_input(update, context):
    current_timestamp = round(time.time())
    myregex = re.compile(r"[^А-Яа-яЁё\s]+")    
    result_string = re.sub(myregex, "", update.message.text)
    if(result_string != ''):
        sqlaccess.insert_records(
                f"INSERT INTO Passes (`Surname`, `People ID`, `Request Time`, `Expiration Time`, `Access ID`) VALUES ('{result_string}', (select `People ID` from People where `Telegram ID`='{update.effective_user.id}'), FROM_UNIXTIME({current_timestamp}), FROM_UNIXTIME({current_timestamp + (60*60*24)}), 2)",
            )
        update.message.reply_text(f"Пропуск на {result_string} оформлен")
    else:
        update.message.reply_text(f"Неверный формат ФИО.")
    return ConversationHandler.END

# def confirm_destination(update, context):
#     """Confirm the selected destination."""
#     user = update.message.from_user
#     if update.message.text == 'Yes':
#         update.message.reply_text('Great, we will fly to {}!'.format(context.user_data['destination']),
#                               reply_markup=ReplyKeyboardRemove())
#         return ConversationHandler.END
#     else:
#         update.message.reply_text('Okay, let\'s try again.',
#                               reply_markup=ReplyKeyboardRemove())
#         return SELECT_DESTINATION

def surname_input(update, context):
    
    sqlaccess.updaterRegister.bot.send_message(chat_id=f"{sqlaccess.args.admin}", text=f"Тест:{update.message.text}\n id пользователя:{update.effective_user.id}")
    return ConversationHandler.END

def cancel(update, context):
    """End the conversation."""
    # user = update.message.from_user
    # update.message.reply_text('Bye!',
    #                           reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

