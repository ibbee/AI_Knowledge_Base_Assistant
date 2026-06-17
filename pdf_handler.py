from pypdf import PdfReader

def read_pdf(file):
    reader = PdfReader(file.file)

    text = ''

    for page in reader.pages:
        text += page.extract_text() + '\n\n'

    return text