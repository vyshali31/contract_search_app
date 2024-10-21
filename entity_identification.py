import spacy
import fitz  # PyMuPDF
import re

import nltk
from nltk import word_tokenize, pos_tag

from extraction import get_json_from_pdf, get_text_from_pdf
from summarize_ai import split_text_into_chunks

nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger_eng')

# Load the spaCy model for English NER
nlp = spacy.load("en_core_web_sm")


def is_valid_date(entity_text):
    # This regex checks for valid date patterns (e.g., "January 1, 2023" or "2023")
    valid_date_patterns = [
        r'^\d{1,2}[/-]\d{1,2}[/-]\d{2,4}$',  # e.g., 12-25-2023 or 12/25/23
        r'^\d{4}$',                           # e.g., 2023
        r'^[A-Za-z]+\s\d{1,2},\s\d{4}$',      # e.g., December 25, 2023
        r'^[A-Za-z]+\s\d{4}$',                # e.g., December 2023
        r'^[A-Za-z]+$'                        # e.g., December
    ]
    for pattern in valid_date_patterns:
        if re.match(pattern, entity_text):
            return True
    return False

def extract_entity_pos(text):

    tokens = word_tokenize(text)
    tags = pos_tag(tokens)
    return tags

def extract_entities(text):
    doc = nlp(text)  # Process the text using spaCy's NER model
    entities = []
    
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    entities = [ent for ent in entities if ent[1] != "CARDINAL"]
    entities = [ent for ent in entities if ent[1] != "ORDINAL"]
    # entities = [ent for ent in entities if ent[1] != "DATE" and is_valid_date(ent[0])]
    #remove duplicates
    entities = list(set(entities))

    return entities


def extract_entities_from_pdf(filename):
    text = get_text_from_pdf(filename)

    chunks = split_text_into_chunks(text, max_tokens=7000)
    entities = []
    for chunk in chunks:
        entities += extract_entities(chunk)

    return entities


if __name__ == "__main__":
    

    text = '''
            CENTRAL ELECTRICITY RE GULATORY COMMISSION NEW DELHI 
            Coram:  Dr. Pramod Deo, Chairperson Shri S.Jayaraman, Member Shri V.S.Verma, Member
            Shri M.Deena Dayalan, Member. Approval of Transmission Service Agreement,  
            Revenue Sharing Agreement, Billing, 
            Collection and Disbursement Procedure under  Central Electricity Regulatory Commission 
            (Sharing of Transmission Charge s and Losses), Regulations, 2010. 
            
            And  In the matter of Power Grid Corporation of India Ltd. (PGCIL) 
        '''
    
    # Extract entities from the text
    entities = extract_entities(text)
    # entities = extract_entity_pos(text)
    
    print(entities)
    