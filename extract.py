import fitz

def extract_from(filepath):

    text = ""

    docs = fitz.open(filepath)

    for page in docs:
        text += page.get_text()

    return text
