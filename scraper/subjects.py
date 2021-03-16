import sys
from WebScraping import WebScraping
from Extractor import Extractor

def __check_error_input(args: str) -> str:
    if len(args) != 2:
        __print_help()
    i:int = 0
    url:str = ""
    while(i < len(args)):
        if args[i] == "-url":
            i += 1
            url = args[i]
        else:
            __print_help()
        i += 1
    return url

def __print_help() -> None:
    h:str = "\nUsage: python3 subjects.py -url <url>\n\n"
    h += "-url:\tIt is the site where we want to get the subjects\n"
    print(h)
    exit(-1)

def main(args: str) -> None:
    url:str = __check_error_input(args)
    print("Extracting subjects...")
    Extractor(WebScraping(url).extract_subjects()).extract_data_frame().to_csv("./Dati/subjects.csv", index = False)
    print("DONE!\n")

if __name__ == "__main__":
    args:str = sys.argv[1:]
    main(args)
