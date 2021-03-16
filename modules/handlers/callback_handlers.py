from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from modules.recommender_system.recommender_system import recommender_system
import random
import numpy as np
from modules.utils.subject_ratings import Subjects
from modules.Logger.logger import Logger
from modules.utils.keyboard import create_keyboard
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.conversationhandler import ConversationHandler
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.update import Update


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
        context.user_data["rate_number"] = random.randint(0, 2)
        context.user_data["rate"] = 5
        query = update.callback_query
        query.answer()
        context.user_data["index_list_subject"] = -context.user_data["index_list_subject_length"]
        reply_markup = InlineKeyboardMarkup(create_keyboard(context, 1, Subjects.getInstance().get_subjects()))
        query.edit_message_text(
            text="In base ai programmi letti, qual è la materia che ha stimolato maggiormente la tua curiosità?", 
            reply_markup=reply_markup
        )
        return 0


def rate_subject(query, context: CallbackContext) -> int:
    context.user_data["rate"] = random.choices(range(5), weights=[0.24, 0.34, 0.22, 0.10, 0.10], k = 1)[0] + 1
    context.user_data["index_list_subject"] = -context.user_data["index_list_subject_length"]
    reply_markup = InlineKeyboardMarkup(create_keyboard(context, 1, Subjects.getInstance().get_subjects()))
    query.edit_message_text(
        text="A quale materia daresti un voto pari a " + str(context.user_data["rate"]) + " in base al programma?", 
        reply_markup=reply_markup
    )
    if(np.count_nonzero(np.array(context.user_data["ratings"])) > context.user_data["rate_number"]):
        return 1
    return 0


def update_rating(index: str, context: CallbackContext) -> None:
    context.user_data["ratings"][int(index)] = context.user_data["rate"]
    Logger.getInstance().info("L'utente " + context.user_data["username"] + " ha dato un voto pari a " + str(context.user_data["rate"]) + 
    " a " + Subjects.getInstance().get_subjects()[index] + ".")


def update_info(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    index = update.callback_query.data.split(" - ")[0]
    update_rating(index, context)
    Subjects.getInstance().delete_subject_name(index, context)
    return rate_subject(query, context)


def end(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    index = update.callback_query.data.split(" - ")[0]
    update_rating(index, context)
    Subjects.getInstance().delete_subject_name(index, context)
    query.edit_message_text(text="Utilizzo i dati da te forniti per capire quali materie potrebbero essere interessanti per te!")
    recommender_subjects = recommender_system(context)
    message:str = "Le 5 materie che ti consiglio sono:\n\n"
    for index in recommender_subjects:
        message += "· " + Subjects.getInstance().get_subjects()[str(index)] + "\n\n"
    query.edit_message_text(text=
        message +
        "Ricorda che io sono solo un bot che cerca di migliorare le proprie capacità in base all'esperienza!\n" +
        "Per ricominciare usa il comando /start"
    )
    Logger.getInstance().info("Conversazione conclusa con l'utente " + context.user_data["username"])
    return ConversationHandler.END


def start_over(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    query.answer()
    Logger.getInstance().info("L'utente " + context.user_data["username"] + " ha ricominciato la conversazione.")
    keyboard = [
        [
            InlineKeyboardButton("LINK", url="http://web.dmi.unict.it/corsi/l-31/programmi"),
            InlineKeyboardButton("Iniziamo!", callback_data=str(0))
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.user_data["index_list_subject_length"] = 4
    context.user_data["ratings"] = []
    context.user_data["subject_names"] = []
    Subjects.getInstance().init_array(context.user_data["ratings"], context.user_data["subject_names"])
    query.edit_message_text(
        text="Prima di iniziare è necessario che tu legga i programmi delle varie materie del 3° anno.\n" +
        "Questo è un passo fondamentale perché dopo ti verrà chiesto di valutarne alcuni!\n" +
        "Puoi cliccare nel bottone sottostante per raggiungere la pagina dei programmi.\n" +
        "Dopo aver letto tutto attentamente clicca su \"Iniziamo!\"",
        reply_markup=reply_markup
    )
    return 0
