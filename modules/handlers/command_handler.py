from logging import error
from telegram.ext.callbackcontext import CallbackContext
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.inline.inlinekeyboardmarkup import InlineKeyboardMarkup
from telegram.update import Update
from modules.Logger.logger import Logger
from modules.utils.subject_ratings import Subjects


def start(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    context.user_data["username"] = user.username
    Logger.getInstance().info("L'utente " + user.username + " ha iniziato la conversazione.")
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
    update.message.reply_text(
        text="Prima di iniziare è necessario che tu legga i programmi delle varie materie del 3° anno.\n" +
        "Questo è un passo fondamentale perché dopo ti verrà chiesto di valutarne alcuni!\n" +
        "Puoi cliccare nel bottone sottostante per raggiungere la pagina dei programmi.\n" +
        "Dopo aver letto tutto attentamente clicca su \"Iniziamo!\", ricorda che il range dei voti va da 1 (pessimo) a 5 (fantastico).",
        reply_markup=reply_markup
    )
    return 0