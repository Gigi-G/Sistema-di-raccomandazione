import logging

class Logger:
   
    __instance = None


    @staticmethod 
    def getInstance():
        if Logger.__instance == None:
            Logger()
        return Logger.__instance


    def __init__(self):
        if Logger.__instance == None:
            logging.basicConfig(
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
            )
            self.__logger = logging.getLogger(__name__)
            Logger.__instance = self


    def info(self, message: str) -> None:
        self.__logger.info(message)