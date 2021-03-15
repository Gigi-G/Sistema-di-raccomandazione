from telegram.ext.callbackcontext import CallbackContext
from modules.recommender_system.ContentBased import ContentBased
from modules.utils.subject_ratings import Subjects
import numpy as np


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


def save_user_ratings(context: CallbackContext) -> None:
    s: str = ""
    for key in Subjects.getInstance().get_subjects():
        s += (
            context.user_data["username"] + "," +
            key + "," +
            Subjects.getInstance().get_subjects()[key] + "," +
            str(context.user_data["ratings"][int(key)]) + "\n"
        )
    with open("./Dati/users/" + context.user_data["username"] + ".csv", "w+") as file:
        file.write(s)


def recommender_system(context: CallbackContext) -> list:
    Subjects.getInstance().get_data().loc[context.user_data["username"]] = create_new_row(context)
    cb = ContentBased("./Dati/subjects.csv", data=Subjects.getInstance().get_data())
    predict(cb, context)
    save_user_ratings(context)
    return (np.argsort(context.user_data["ratings"]).tolist()[::-1])[0:5]