from telegram.ext.callbackcontext import CallbackContext
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton

def create_keyboard(context: CallbackContext, direction: int, subjects: dict) -> list:
    keyboard_subject: list = []
    list_length = context.user_data["index_list_subject_length"]
    context.user_data["index_list_subject"] += (list_length * direction)
    if(context.user_data["index_list_subject"] >= len(context.user_data["subject_names"]) or context.user_data["index_list_subject"] <= -4):
        context.user_data["index_list_subject"] -= (list_length * direction)
    start_index = context.user_data["index_list_subject"]
    end_index = start_index + list_length

    for key in context.user_data["subject_names"][start_index:end_index]:
        keyboard_subject.append([InlineKeyboardButton(subjects[key], callback_data=key + " - delete")])
    
    button: list = []
    if start_index > 0:
        button.append(InlineKeyboardButton("⏪", callback_data="LEFT"))
    if end_index < len(context.user_data["subject_names"]):
        button.append(InlineKeyboardButton("⏩", callback_data="RIGHT"))
    keyboard_subject.append(button)
    keyboard_subject.append([InlineKeyboardButton("🔁 RESTART 🔁", callback_data="restart")])
    return keyboard_subject