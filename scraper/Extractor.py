from WebScraping import WebScraping
from FormatPDF import FormatPDF
import os
import pandas as pd

class Extractor:
    def __init__(self, subjects:list):
        self.subjects = subjects

    def __extract_subject_description(self, text:list) -> str:
        i:int = 0
        while(text[i].upper() != "CONTENUTI DEL CORSO"):
            i += 1
        i += 1
        description:str = ""
        while(text[i].upper() != "TESTI DI RIFERIMENTO"):
            description += text[i] + " "
            i += 1
        while(text[i].upper() != "PROGRAMMAZIONE DEL CORSO"):
            i += 1
        i += 3
        while(text[i].upper() != "VERIFICA DELL'APPRENDIMENTO"):
            #print(text[i][1:].strip())
            if text[i] != None:
                description += text[i][3:].strip() + " "
            i += 1
        return description

    def extract_data_frame(self) -> any:
        ids:list = []
        descriptions:list = []
        i:int = 0
        print("Please Wait... It will take some time\n")
        for subject in self.subjects:
            print(subject[0] + "\n")
            web_page:WebScraping = WebScraping(subject[1])
            web_page.create_pdf(subject[0])
            description:str = self.__extract_subject_description(FormatPDF.format_pdf(subject[0] + ".pdf"))
            descriptions.append(
                subject[0] + 
                " - " + 
                description
            )
            ids.append(i)
            i += 1
            os.remove(subject[0] + ".pdf")
        return pd.DataFrame({'id': ids, 'description': descriptions})