import PyPDF2
from pdf2image import convert_from_path
import pytesseract
import os
from pdf_reader_fr import extract_pdf_to_json
import json
from consts import *

def is_scanned_pdf(pdf_path, text_threshold=50):
    try:
        # Open and read the PDF
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ""
            # Attempt to extract text from all pages
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
            
            # If extracted text is below a threshold, it's likely a scanned PDF
            if len(text.strip()) < text_threshold:
                print("Scanned PDF detected.")
                return True  # Scanned PDF (image-based)
            else:
                print("Normal PDF detected.")
                return False  # Normal PDF (text-based)
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


def extract_text_from_normal_pdf(pdf_path):
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()
    except Exception as e:
        print(f"Error while reading PDF: {e}")
    return text


def extract_text_from_scanned_pdf(pdf_path):
    text = ""
    try:
        # Convert PDF pages to images
        images = convert_from_path(pdf_path)
        for image in images:
            # Perform OCR on each image
            text += pytesseract.image_to_string(image)
    except Exception as e:
        print(f"Error during OCR process: {e}")
    return text


def get_text_from_pdf(filename):
    
    filepath = os.path.join(INPUT_LOCATION, filename)
    txt_output = os.path.join(OUTPUT_LOCATION, filename + ".txt")

    #checking if the file is already present.
    if os.path.exists(txt_output):
        print(f"{txt_output} already exists")
        with open(txt_output, "r", encoding="utf-8") as file:
            return file.read()

    if filepath.endswith(".pdf"):
        if is_scanned_pdf(filepath):
            text = extract_text_from_scanned_pdf(filepath)
        else:
            text = extract_text_from_normal_pdf(filepath)

        with open(txt_output, "w") as file:
            file.write(text)

    return text


def get_json_from_pdf(filename):
    
    filepath = os.path.join(INPUT_LOCATION, filename)
    json_output = os.path.join(OUTPUT_LOCATION, filename + ".json")

    #checking if the file is already present.
    if os.path.exists(json_output):
        print(f"{json_output} already exists")
        with open(json_output, "r") as file:
            return file.read()
    
    if filename.endswith(".pdf"):
        text = extract_pdf_to_json(filepath)
        with open(json_output, "w") as file:
            json.dump(text, file, indent=4)
        return text


if __name__ == "__main__":

    print("Extracting text from PDF files...")
    text = get_text_from_pdf("sample MSA.pdf")
    print(text[:1000])
    text = get_json_from_pdf("sample MSA.pdf")
    print(text[:1000])
    print("Text extraction completed.")


