from telegram import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters

# Define the states for the conversation
SELECT_DESTINATION, CONFIRM_DESTINATION = range(2)

def fly(update, context):
    """Start the conversation to select a destination to fly to."""
    update.message.reply_text('Where do you want to fly?',)
    return SELECT_DESTINATION

def select_destination(update, context):
    """Store the selected destination."""
    user = update.message.from_user
    context.user_data['destination'] = update.message.text
    # button1 = InlineKeyboardButton("Да", callback_data="Yes")
    # button2 = InlineKeyboardButton("Нет", callback_data="No")
    keyboard = ReplyKeyboardMarkup([["Yes"], ["no"]], one_time_keyboard=True)
    # keyboard = InlineKeyboardMarkup([[button1, button2]])
    update.message.reply_text('Do you want to fly to {}?'.format(update.message.text),
                              reply_markup=keyboard)
    return CONFIRM_DESTINATION

def confirm_destination(update, context):
    """Confirm the selected destination."""
    user = update.message.from_user
    if update.message.text == 'Yes':
        update.message.reply_text('Great, we will fly to {}!'.format(context.user_data['destination']),
                              reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END
    else:
        update.message.reply_text('Okay, let\'s try again.',
                              reply_markup=ReplyKeyboardRemove())
        return SELECT_DESTINATION

def cancel(update, context):
    """End the conversation."""
    user = update.message.from_user
    update.message.reply_text('Bye!',
                              reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

def convoStart():
    # Define the conversation handler
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('fly', fly)],

        states={
            SELECT_DESTINATION: [MessageHandler(Filters.text, select_destination)],
            CONFIRM_DESTINATION: [MessageHandler(Filters.text, confirm_destination)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    return conv_handler