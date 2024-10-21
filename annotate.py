import fitz  # PyMuPDF
import json
from pdf_reader_fr import extract_pdf_to_json
# from entity_identification import extract_entities
from flask import Flask, request, jsonify
from annotate import annotate_ner_words

def annotate_ner_words(annotation_data_list, input_pdf_path, output_pdf_path, entities):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf_path)

    # Iterate through all annotation data entries (assuming each one is for a different page)
    for this_page in annotation_data_list:
        for item in this_page:
            page_number = item["page"]
            page = pdf_document[page_number]

            for entity in entities:
                if item["chunk_text"]["eng"]["text"].lower().find(entity[0]) != -1:
                    for word in item["words"]:
                        this_word = word["text"].lower()
                        # Remove the last . or , from the word
                        if this_word[-1] == "." or this_word[-1] == ",":
                            this_word = this_word[:-1]

                        if this_word == entity[0]:
                            print(f"Word '{word['text']}' found on page {page_number + 1}")
                            word_rect = fitz.Rect(word["xmin"], word["ymin"], word["xmax"], word["ymax"])
                            page.add_highlight_annot(word_rect)
                            # page.add_text_annot((word["xmin"], word["ymin"]), entity[1])

    # Save the output PDF
    pdf_document.save(output_pdf_path)
    pdf_document.close()
    return

    for annotation_data in annotation_data_list:
        page_number = annotation_data["page"]
        page = pdf_document[page_number]

        # print(f"Annotating page {page_number + 1}...")

        # Checking the entities in the text
        for entity in entities:
            if annotation_data["chunk_text"]["eng"]["text"].lower().find(entity[0]) != -1:
                print(f"{entity[0]} found in the text on page {page_number + 1}")
                for word in annotation_data["words"]:
                    this_word = word["text"].lower()
                    # Remove the last . or , from the word
                    if this_word[-1] == "." or this_word[-1] == ",":
                        this_word = this_word[:-1]

                    if this_word == entity[0]:
                        print(f"Word '{word['text']}' found on page {page_number + 1}")
                        word_rect = fitz.Rect(word["xmin"], word["ymin"], word["xmax"], word["ymax"])
                        print(word["xmin"], word["ymin"], word["xmax"], word["ymax"])
                        page.add_highlight_annot(word_rect)
                        page.add_text_annot((word["xmin"], word["ymin"]), entity[1])

    # Save the output PDF
    pdf_document.save(output_pdf_path)
    pdf_document.close()


def annotate_pdf(annotation_data, input_pdf_path, output_pdf_path):
    # Open the PDF file
    pdf_document = fitz.open(input_pdf_path)

    # Get the specified page
    page = pdf_document[annotation_data["page"]]

    # Draw a rectangle around the bounding box
    bb = [annotation_data["bounding_box"][0], annotation_data["bounding_box"][1], annotation_data["bounding_box"][2], annotation_data["bounding_box"][7]]
    rect = fitz.Rect(*bb)
    highlight = page.add_highlight_annot(rect)

    # Add text annotation based on chunk_text
    page.add_text_annot((annotation_data["bounding_box"][0], annotation_data["bounding_box"][1]), annotation_data["chunk_text"]["eng"]["text"])

    # Draw rectangles around each word (optional, to highlight individual words)
    # for word in annotation_data["words"]:
    #     word_rect = fitz.Rect(word["xmin"], word["ymin"], word["xmax"], word["ymax"])
    #     page.add_rect_annot(word_rect)

    # Save the PDF with annotations
    pdf_document.save(output_pdf_path)
    pdf_document.close()


def get_annotation_data(json_file_path):
    with open(json_file_path, "r") as file:
        return json.load(file)

if __name__ == "__main__":
    input_pdf = "input_docs/Sample MSA.pdf"
    pdf_json = "output_docs/Sample MSA.json"
    annotated_pdf = "output_docs/Sample MSA_annotated.pdf"

    json_data = extract_pdf_to_json(input_pdf)
    with open(pdf_json, "w") as file:
        json.dump(json_data, file, indent=4)

    json_data = get_annotation_data(pdf_json)
    
    # firstdata = json_data[0][1]

    # annotate_pdf(firstdata, input_pdf, annotated_pdf)

    full_text = ""

    for i in range(len(json_data)):
        for data in json_data[i]:
            full_text += data["chunk_text"]["eng"]["text"] + " "


    full_text = full_text.lower()

    # entities = extract_entities(full_text)

    entities = [('cashier', 'ORG'), ('english', 'LANGUAGE'), ('addressee', 'GPE'), ('philippines', 'GPE'), ('ref', 'ORG'), ('oais', 'GPE'), ('oais', 'ORG'), ('contractor', 'PERSON'), ('manila', 'GPE'), ('addressee', 'NORP')]
 
    annotate_ner_words(json_data, input_pdf, annotated_pdf, entities)

