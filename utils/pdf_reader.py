from pypdf import PdfReader
from pdf2image import convert_from_path
import pytesseract
import re

def extract_email(text):
    emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", text)
    return emails[0] if emails else None


def read_pdf(file_path):
    reader = PdfReader(file_path)

    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    # If normal extraction fails → fallback to OCR
    if len(text.strip()) < 50:
        images = convert_from_path(file_path)

        ocr_text = ""
        for img in images:
            ocr_text += pytesseract.image_to_string(img)

        text = ocr_text

    return text