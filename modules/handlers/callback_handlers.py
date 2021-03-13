from ContentBased import ContentBased
import random
import numpy as np
from modules.utils.subjects import Subjects
from modules.Logger.logger import Logger
from modules.utils.keyboard import create_keyboard
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.update import Update
import pandas as pd



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
    Subjects.getInstance().get_data().loc[context.user_data["username"]] = create_new_row(context)
    Logger.getInstance().info(Subjects.getInstance().get_data())
    cb = ContentBased("/home/gigi-g/Sistema di raccomandazione/Dati/subjects.csv", data=Subjects.getInstance().get_data())
    predict(cb, context)
    return (np.argsort(context.user_data["ratings"]).tolist()[::-1])[0:5]


def end(update: Update, context: CallbackContext) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over"""
    subjects: Subjects = Subjects.getInstance()
    query = update.callback_query
    query.answer()
    index = update.callback_query.data.split(" - ")[0]
    update_rating(index, context)
    subjects.delete_subject_name(subjects.get_subjects()[index], context)
    query.edit_message_text(text="Utilizzo i dati da te forniti per capire quali materie potrebbero essere interessanti per te!")
    recommender_subjects = recommender_system(context)
    message:str = "Le 5 materie che ti consiglio sono:\n\n"
    for index in recommender_subjects:
        message += "· " + subjects.get_subjects()[str(index)] + "\n\n"
    query.edit_message_text(text=
        message +
        "Ricorda che io sono solo un bot che cerca di migliorare le proprie capacità in base all'esperienza!\n" +
        "Per ricominciare usa il comando /start"
    )
    Logger.getInstance().info("Conversazione conclusa con l'utente " + context.user_data["username"])
    return ConversationHandler.END


def shift_menu_left(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(create_keyboard(context, -1, Subjects.getInstance().get_subjects()))
    query.edit_message_text(text=query.message.text, reply_markup=reply_markup)
    return 0


def shift_menu_right(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    reply_markup = InlineKeyboardMarkup(create_keyboard(context, 1, Subjects.getInstance().get_subjects()))
    query.edit_message_text(text=query.message.text, reply_markup=reply_markup)
    return 0

def rate_best_subject(update: Update, context: CallbackContext) -> int:
        context.user_data["rate"] = 5
        query = update.callback_query
        query.answer()
        context.user_data["index_list_subject"] = 0
        reply_markup = InlineKeyboardMarkup(create_keyboard(context, 1, Subjects.getInstance().get_subjects()))
        query.edit_message_text(
            text="In base ai programmi letti, qual è la materia che ha stimolato maggiormente la tua curiosità?", 
            reply_markup=reply_markup
        )
        return 0


def rate_subject(query, context: CallbackContext) -> int:
    context.user_data["rate"] = random.choices(range(5), weights=[0.24, 0.14, 0.24, 0.24, 0.14], k = 1)[0] + 1
    context.user_data["index_list_subject"] = 0
    reply_markup = InlineKeyboardMarkup(create_keyboard(context, 1, Subjects.getInstance().get_subjects()))
    query.edit_message_text(
        text="A quale materia daresti un voto pari a " + str(context.user_data["rate"]) + " in base al programma?", 
        reply_markup=reply_markup
    )
    if(np.count_nonzero(np.array(context.user_data["ratings"])) > 0):
        return 1
    return 0


def update_rating(index:str, context: CallbackContext) -> None:
    context.user_data["ratings"][int(index)] = context.user_data["rate"]
    Logger.getInstance().info("L'utente " + context.user_data["username"] + " ha dato un voto pari a " + str(context.user_data["rate"]) + 
    " a " + Subjects.getInstance().get_subjects()[index] + ".")


def update_info(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    index = update.callback_query.data.split(" - ")[0]
    update_rating(index, context)
    Subjects.getInstance().delete_subject_name(Subjects.getInstance().get_subjects()[index], context)
    return rate_subject(query, context)