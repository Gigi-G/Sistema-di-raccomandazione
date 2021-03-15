from urllib.request import urlopen as uRequest
from bs4 import BeautifulSoup as soup

class WebScraping:
    
    def __init__(self, url:str):
        self.url = url
        u_client = uRequest(url)
        self.page_html = u_client.read()
        self.page_soup = soup(self.page_html, features="lxml")
    
    def __get_base_path(self) -> str:
        result:str = ""
        for k in self.url.split("/")[0:-3]:
            result += (k + "/")
        return result[0:-1]

    def __create_link(self, link) -> str:
        result:str = ""
        split:list = link.split("/")
        for k in split[0:-1]:
            result += (k + "/")
        return ("http://syllabus.unict.it/insegnamento.php?id=" + split[len(split)-1][5:] + "&pdf")

    def extract_subjects(self) -> list:
        excluded:list = ['ALGORITMI RANDOMIZZATI ED APPROSSIMATI', 'FISICA', 'METODI MATEMATICI E STATISTICI']
        td = self.page_soup.findAll('td')
        i:int = 0
        while("3° anno" not in td[i].text):
            td.remove(td[i])
        subjects:list = []
        for elem in td:
            result = elem.findAll('a')
            subject:list = []
            if len(result) > 0 and result[0].text not in excluded:
                subject.append(result[0].text)
                subject.append(self.__create_link(result[0]["href"]))
                subjects.append(subject)
        return subjects

    def create_pdf(self, name) -> None:
        open(name + ".pdf", 'wb').write(self.page_html)