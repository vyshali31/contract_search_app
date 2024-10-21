from fuzzywuzzy import fuzz
import json

import re
from difflib import get_close_matches


def find_clause_group(search_term, clauses):
    for clause_group, terms in clauses.items():
        print(f"Checking clause group: {clause_group} in {terms}")
        # Use get_close_matches to check for similar terms
        if get_close_matches(search_term.lower(), [term.lower() for term in terms], n=1, cutoff=0.8):
            print(f"Found clause group: {clause_group}")
            return clause_group

    return None

def search_clauses_in_text1(text, search_term):

    # Load your clauses
    with open("clauses.json") as f:
        clauses = json.load(f)

    # Find which clause group contains the search term
    clause_group = find_clause_group(search_term, clauses)

    if clause_group is None:
        return f"No clause group found for '{search_term}'"

    print(f"Searching in clause group: {clause_group}")

    # Now, search the text for terms in the identified clause group
    matching_sentences = []
    sentences = re.split(r'(?<=\.)\s', text)  # Split the text into sentences
    for sentence in sentences:
        if any(term.lower() in sentence.lower() for term in clauses[clause_group]):
            matching_sentences.append(sentence)

    return matching_sentences


def search_clauses_in_text(text, search_term):

        # Load your clauses
    with open("clauses.json") as f:
        clauses = json.load(f)

    # Find which clause group contains the search term
    clause_group_identified = find_clause_group(search_term, clauses)

    if clause_group_identified is None:
        return f"No clause group found for '{search_term}'"

    print(f"Fuzzy Searching in clause group: {clause_group_identified}")

    matching_sentences = []
    
    # Split text into sentences
    sentences = text.split('. ')

    
    for clause_group, terms in clauses.items():
        if clause_group == clause_group_identified:
            # print(f"---->>> Checking clause group: {clause_group} in {terms}")

            for term in terms:
                for sentence in sentences:
                    # Perform fuzzy matching
                    if fuzz.partial_ratio(search_term.lower(), sentence.lower()) > 70 or \
                    any(fuzz.partial_ratio(term.lower(), sentence.lower()) > 70 for term in terms):
                        matching_sentences.append((clause_group_identified, sentence))
        
    return matching_sentences


if __name__ == "__main__":
    text = '''
    "PCI",
    CENTRAL ELECTRICITY RE GULATORY COMMISSION NEW DELHI PCI.
    Coramis Chairperson GDPR  Shri S.Jayaraman, Member. In the matter of Approval of Transmission Service Agreement.
    Revenue Sharing Agreement, Billing, Collection and Disbursement. Procedure under  Central Electricity Regulatory Commission of GDPR.
    Sharing of Transmission Charge s and Losses EU Law Regulations 2010. 
    Payment Card industry Data Security Standard.

'''
    
    search_query = "PCI"
    # result = search_clauses(text, search_query)
    result = search_clauses_in_text(text, search_query)
    print(result)

