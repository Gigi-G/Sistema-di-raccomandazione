from telegram.ext.callbackcontext import CallbackContext
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton


def create_keyboard(context: CallbackContext, direction: int, subjects: dict) -> list:
    keyboard_subject = []
    context.user_data["index_list_subject"] += (3 * direction)
    if(context.user_data["index_list_subject"] >= len(subjects)):
        context.user_data["index_list_subject"] = len(subjects) - 1
    i:int = 3 * direction
    j:int = 0
    for key, value in list(subjects.items())[context.user_data["index_list_subject"]:]:
        if(j == i):
            break
        if(value in context.user_data["subject_names"]):
            keyboard_subject.append([InlineKeyboardButton(value, callback_data=key + " - delete")])
            j += direction
    if(context.user_data["index_list_subject"] - 3 == 0):
        keyboard_subject.append([InlineKeyboardButton("⏩", callback_data="RIGHT")])
    elif(context.user_data["index_list_subject"] >= len(context.user_data["subject_names"]) - 3):
        keyboard_subject.append([InlineKeyboardButton("⏪", callback_data="LEFT")])
    else:
        keyboard_subject.append([InlineKeyboardButton("⏪", callback_data="LEFT"), InlineKeyboardButton("⏩", callback_data="RIGHT")])
    return keyboard_subject