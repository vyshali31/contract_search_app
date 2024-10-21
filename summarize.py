# from transformers import pipeline
import nltk
import string
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.data import find
from nltk.probability import FreqDist
from transformers import pipeline
import re

def download_nltk_resources():
    resources = ['punkt','punkt_tab', 'stopwords', 'averaged_perceptron_tagger']  # List of required resources

    for resource in resources:
        try:
            # Try to find the resource
            if resource == 'punkt':
                find('tokenizers/punkt')
            elif resource == 'punkt_tab':
                find('tokenizers/punkt_tab')
            elif resource == 'stopwords':
                find('corpora/stopwords')
            elif resource == 'averaged_perceptron_tagger':
                find('taggers/averaged_perceptron_tagger')
        except LookupError:
            # If the resource is not found, download it
            print(f"Downloading NLTK resource: {resource}")
            nltk.download(resource)

def generate_summary(text, num_sentences=5):
    """
    Summarizes the given text using a transformer-based model (BART).
    
    Parameters:
        text (str): The input text to summarize.
        num_sentences (int): Approximate number of sentences in the summary (this parameter is flexible for transformers).
    
    Returns:
        summary (str): The summarized text.
    """
    try:
        # Load a pre-trained summarization pipeline
        summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        # Summarize the text; max_length controls the length of the summary
        summary = summarizer(text, max_length=num_sentences * 20, min_length=num_sentences * 10, do_sample=False)
        
        print("summary:: " , summary)
        # Extract the summarized text from the result
        return summary[0]['summary_text']
    
    except Exception as e:
        return f"Error during summarization: {e}"


def preprocess_text(text):
    """
    Preprocesses the input text by performing tokenization, case normalization, punctuation removal, 
    and stopword removal.
    
    Parameters:
        text (str): The input text to preprocess.
    
    Returns:
        clean_tokens (list): A list of cleaned, tokenized words.
    """
    
    # Tokenization: Split text into sentences and words
    sentences = sent_tokenize(text)  # Tokenize into sentences
    words = word_tokenize(text)      # Tokenize into words
    
    # Case Normalization: Convert all words to lowercase
    words_lower = [word.lower() for word in words]
    
    #Punctuation Removal: Remove all punctuation marks
    words_no_punct = [word for word in words_lower if word not in string.punctuation]
    
    #Stopword Removal: Remove common stopwords like "the", "is", etc.
    
    stop_words = {}
    # stop_words = set(stopwords.words("english"))

    clean_tokens = [word for word in words_no_punct if word not in stop_words]
    clean_tokens = [word.replace('_', '') for word in clean_tokens]
    clean_tokens = [word.replace('.', '') for word in clean_tokens]
    clean_tokens = [word for word in clean_tokens if not re.search(r'\d', word)]
    clean_tokens = [word for word in clean_tokens if len(word) > 2]

    clean_tokens = set(clean_tokens)
    
    return clean_tokens

# Frequency distribution function
def get_frequency_distribution(tokens):
    """
    Computes the frequency distribution of the given tokens.
    """
    return FreqDist(tokens)

# Sentence scoring function
def score_sentences(text, freq_dist):
    """
    Scores sentences based on word frequency.
    
    Parameters:
        text (str): The original text.
        freq_dist (FreqDist): The frequency distribution of words.
    
    Returns:
        sentence_scores (dict): A dictionary where keys are sentences and values are their scores.
    """
    sentence_scores = {}
    
    # Tokenize the text into sentences
    sentences = sent_tokenize(text)
    
    for sentence in sentences:
        # Tokenize sentence into words
        sentence_words = word_tokenize(sentence.lower())
        
        # Calculate sentence score based on word frequencies
        sentence_score = sum(freq_dist[word] for word in sentence_words if word in freq_dist)
        sentence_scores[sentence] = sentence_score
    
    return sentence_scores


def generate_custom_summary(text, num_sentences=5):
    """
    Generates a summary of the given text by selecting the most important sentences.
    
    Parameters:
        text (str): The original text to summarize.
        num_sentences (int): The number of top sentences to include in the summary.
    
    Returns:
        summary (str): The generated summary.
    """
    # Preprocess the text to get cleaned tokens
    tokens = preprocess_text(text)


    # Get the frequency distribution of the words
    freq_dist = get_frequency_distribution(tokens)
    
    # Score the sentences based on word frequencies
    sentence_scores = score_sentences(text, freq_dist)
    
    # Sort the sentences by their score in descending order
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)
    
    # SSelect the top 'num_sentences' sentences for the summary
    selected_sentences = sorted_sentences[:num_sentences]
    
    # Returnr the summary by joining the selected sentences
    summary = ' \n\n\n'.join(selected_sentences)
    
    return summary


if __name__ == "__main__":

    download_nltk_resources()

    with open("output_docs/Contract 1 (1).pdf.txt", "r") as file:
        extracted_text = file.read()

    # Generate a summary of the extracted text
    # summary = generate_summary(extracted_text)
    # print(summary)

    print("--------------------------------\n")

    # Generate a summary using custom summarization method
    custom_summary = generate_custom_summary(extracted_text, num_sentences=3)
    print(custom_summary)


