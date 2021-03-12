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
import random
import numpy as np
import pandas as pd
import logging
from os import name
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    ConversationHandler,
    CallbackContext,
)
# data
from modules.data.data_reader import config_map
from ContentBased import ContentBased

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Stages
FIRST, SECOND = range(2)
# Callback data
ONE = 0
# Subjects
subjects = {}

## COSE DA FARE
# Aggiungere messaggio per ricominciare, aggiornare il file CSV e migliorare i bottoni nella selezione delle materie


def delete_subject_name(name: str, context: CallbackContext) -> None:
    context.user_data["subject_names"].remove(name)


def load_subjects() -> None:
    global subjects
    global names
    global ratings
    subjects = {}
    names = []
    ratings = []
    with open("./Dati/subjects.csv") as subject:
        for s in subject:
            split:str = s.split(',')
            if(split[0] != "id"):
                name:str = split[1].split(" - ")[0]
                if name[0] == "\"":
                    name = name[1:]
                subjects[split[0]] = name
                names.append(name)
                ratings.append(0)

def init_array(ratings: list, subject_names: list) -> None:
    global subjects
    for key in subjects:
        subject_names.append(subjects[key])
        ratings.append(0)


def create_keyboard(context: CallbackContext, direction: int) -> list:
    keyboard_subject = []
    context.user_data["index_list_subject"] += (3 * direction)
    if(context.user_data["index_list_subject"] >= len(subjects)):
        context.user_data["index_list_subject"] = len(subjects) - 1
    i:int = 3 * direction
    j:int = 0
    for key, value in list(subjects.items())[(context.user_data["index_list_subject"] * direction):]:
        if(j == i):
            break
        if(value in context.user_data["subject_names"]):
            keyboard_subject.append([InlineKeyboardButton(value, callback_data=key + " - delete")])
            j += direction
    if(context.user_data["index_list_subject"] == 0):
        keyboard_subject.append([InlineKeyboardButton("⏩", callback_data="RIGHT")])
    elif(context.user_data["index_list_subject"] >= len(context.user_data["subject_names"]) - 3):
        keyboard_subject.append([InlineKeyboardButton("⏪", callback_data="LEFT")])
    else:
        keyboard_subject.append([InlineKeyboardButton("⏪", callback_data="LEFT"), InlineKeyboardButton("⏩", callback_data="RIGHT")])
    return keyboard_subject


def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    context.user_data["username"] = user.username
    logger.info("L'utente %s ha iniziato la conversazione.", user.username)
    keyboard = [
        [
            InlineKeyboardButton("LINK", url="http://web.dmi.unict.it/corsi/l-31/programmi"),
            InlineKeyboardButton("Iniziamo!", callback_data=str(ONE))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data["ratings"] = []
    context.user_data["subject_names"] = []
    init_array(context.user_data["ratings"], context.user_data["subject_names"])
    logger.info(context.user_data["ratings"])
    update.message.reply_text(
        text="Prima di iniziare è necessario che tu legga i programmi delle varie materie del 3° anno.\n" +
        "Questo è un passo fondamentale perché dopo ti verrà chiesto di valutarne alcuni!\n" +
        "Puoi cliccare nel bottone sottostante per raggiungere la pagina dei programmi.\n" +
        "Dopo aver letto tutto attentamente clicca su \"Iniziamo!\"",
        reply_markup=reply_markup
    )
    return FIRST


def rate_best_subject(update: Update, context: CallbackContext) -> None:
    context.user_data["rate"] = 5
    query = update.callback_query
    query.answer()
    context.user_data["index_list_subject"] = 0
    reply_markup = InlineKeyboardMarkup(create_keyboard(context, 1))
    query.edit_message_text(
        text="In base ai programmi letti, qual è la materia che ha stimolato maggiormente la tua curiosità?", 
        reply_markup=reply_markup
    )
    return FIRST


def rate_subject(query, context: CallbackContext) -> None:
    context.user_data["rate"] = random.choices(range(5), weights=[0.24, 0.14, 0.24, 0.24, 0.14], k = 1)[0] + 1
    context.user_data["index_list_subject"] = 0
    reply_markup = InlineKeyboardMarkup(create_keyboard(context, 1))
    query.edit_message_text(
        text="A quale materia daresti un voto pari a " + str(context.user_data["rate"]) + " in base al programma?", 
        reply_markup=reply_markup
    )
    if(np.count_nonzero(np.array(context.user_data["ratings"])) > 0):
        return SECOND
    return FIRST


def update_rating(index:str, context: CallbackContext) -> None:
    context.user_data["ratings"][int(index)] = context.user_data["rate"]
    logger.info("L'utente %s ha dato un voto pari a " + str(context.user_data["rate"]) + " a " + subjects[index] + ".", context.user_data["username"])


def update_info(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    index = update.callback_query.data.split(" - ")[0]
    update_rating(index, context)
    delete_subject_name(subjects[index], context)
    return rate_subject(query, context)


def predict(cb: ContentBased, context: CallbackContext) -> None:
    i:int = 0
    while(i < len(context.user_data["ratings"])):
        if(context.user_data["ratings"][i] == 0):
            context.user_data["ratings"][i] = cb.predict(14, i)
        i += 1


def create_new_row(context: CallbackContext) -> list:
    row = np.array(context.user_data["ratings"])
    row = row.astype('float')
    row[row == 0] = np.NaN
    return row.tolist()


def recommender_system(context: CallbackContext) -> list:
    data = pd.read_csv("/home/gigi-g/Sistema di raccomandazione/Dati/Dati.csv")
    data = data.pivot_table(index='user_id', columns='subject_id', values='rating')
    data.loc[context.user_data["username"]] = create_new_row(context)
    logger.info(data)
    cb = ContentBased("/home/gigi-g/Sistema di raccomandazione/Dati/subjects.csv", data=data)
    predict(cb, context)
    return (np.argsort(context.user_data["ratings"]).tolist()[::-1])[0:5]


def end(update: Update, context: CallbackContext) -> None:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    query = update.callback_query
    query.answer()
    index = update.callback_query.data.split(" - ")[0]
    update_rating(index, context)
    delete_subject_name(subjects[index], context)
    query.edit_message_text(text="Utilizzo i dati da te forniti per capire quali materie potrebbero essere interessanti per te!")
    recommender_subjects = recommender_system(context)
    message:str = "Le 5 materie che ti consiglio sono:\n\n"
    for index in recommender_subjects:
        message += "· " + subjects[str(index)] + "\n\n"
    query.edit_message_text(text=
        message +
        "Ricorda che io sono solo un bot che cerca di migliorare le proprie capacità in base all'esperienza!\n" +
        "Per ricominciare usa il comando /start"
    )
    logger.info("Conversazione conclusa con l'utente %s", context.user_data["username"])
    return ConversationHandler.END


def shift_menu_left(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(create_keyboard(context, -1))
    query.edit_message_text(text=query.message.text, reply_markup=reply_markup)
    return FIRST


def shift_menu_right(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(create_keyboard(context, 1))
    query.edit_message_text(text=query.message.text, reply_markup=reply_markup)
    return FIRST


def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(config_map['token'], request_kwargs={'read_timeout': 20, 'connect_timeout': 20}, use_context=True)

    # Load subjects from ./Dati/Dati.csv
    load_subjects()

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
