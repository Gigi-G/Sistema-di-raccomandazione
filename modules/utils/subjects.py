from telegram.ext.callbackcontext import CallbackContext
import pandas as pd


class Subjects:

    __instance = None


    @staticmethod
    def getInstance():
        """ Static access method. """
        if Subjects.__instance == None:
            Subjects()
        return Subjects.__instance


    def __init__(self) -> None:
        """ Virtually private constructor. """
        if Subjects.__instance == None:
            Subjects.__instance = self


    def get_subjects(self) -> dict:
        return self.__subjects

    
    def get_data(self):
        return self.__data


    def load_subjects(self) -> None:
        self.__data = pd.read_csv("./Dati/Dati.csv")
        self.__data = self.__data.pivot_table(index='user_id', columns='subject_id', values='rating')
        self.__subjects = {}
        with open("./Dati/subjects.csv", 'r') as subject:
            for s in subject:
                split:str = s.split(',')
                if(split[0] != "id"):
                    name:str = split[1].split(" - ")[0]
                    if name[0] == "\"":
                        name = name[1:]
                    self.__subjects[split[0]] = name


    def init_array(self, ratings: list, subject_names: list) -> None:
        for key in self.__subjects:
            subject_names.append(self.__subjects[key])
            ratings.append(0)


    def delete_subject_name(self, name: str, context: CallbackContext) -> None:
        context.user_data["subject_names"].remove(name)