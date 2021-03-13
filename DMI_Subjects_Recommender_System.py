#!/usr/bin/env python
# pylint: disable=W0613, C0116
# type: ignore[union-attr]

"""Simple inline keyboard bot with multiple CallbackQueryHandlers.
This Bot uses the Updater class to handle the bot.
First, a few callback functions are defined as callback query handler. Then, those functions are
passed to the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot that uses inline keyboard that has multiple CallbackQueryHandlers arranged in a
ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line to stop the bot.
"""
from logging import Logger
import numpy as np
import pandas as pd
from os import name
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
from modules.data.data_reader import config_map
from ContentBased import ContentBased
from modules.Logger.logger import Logger
from modules.utils.subjects import Subjects
from modules.handlers.callback_handlers import (end, rate_best_subject, update_info, shift_menu_right, shift_menu_left)
from modules.handlers.command_handler import start

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE = 0
# Subjects
subjects: Subjects = Subjects.getInstance()
# Dataset
data = []

## COSE DA FARE
# Aggiornare il file CSV


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(config_map['token'], request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)

    # Load subjects from ./Dati/Dati.csv
    subjects.load_subjects()

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Setup conversation handler with the states FIRST and SECOND
    # Use the pattern parameter to pass CallbackQueries with specific
    # data pattern to the corresponding handlers.
    # ^ means "start of line/string"
    # $ means "end of line/string"
    # So ^ABC$ will only allow 'ABC'
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIRST: [
                CallbackQueryHandler(rate_best_subject, pattern='^' + str(ONE) + '$'),
                CallbackQueryHandler(update_info, pattern='^[0-9][0-9]?\s-\sdelete$'),
                CallbackQueryHandler(shift_menu_left, pattern='^LEFT$'),
                CallbackQueryHandler(shift_menu_right, pattern='^RIGHT$'),
            ],
            SECOND: [
                CallbackQueryHandler(end, pattern='^[0-9][0-9]?\s-\sdelete$'),
            ],
        },
        fallbacks=[CommandHandler('start', start)],
    )

    # Add ConversationHandler to dispatcher that will be used for handling
    # updates
    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()