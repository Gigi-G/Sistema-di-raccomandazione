import pdftotext

class FormatPDF:
    
    @staticmethod
    def format_pdf(pathname: str) -> None:
        with open(pathname, "rb") as f:
            pdf = pdftotext.PDF(f)
            f.close()
        formatted_lines = []
        text = ""
        for line in pdf:
            text += line
        split_text = text.split("\n")
        for line in split_text:
            formatted_lines.append(line.strip())
        return formatted_lines
