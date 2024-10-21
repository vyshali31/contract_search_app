### Contract Search Engine - Detailed README
The Contract Search Engine is a sophisticated tool designed to assist legal professionals in searching, retrieving, and analyzing contract data efficiently. By leveraging Natural Language Processing (NLP), Machine Learning (ML), Optical Character Recognition (OCR), and advanced transformer models, the engine allows users to quickly access key information within lengthy legal contracts.

The system is capable of:

1. Summarizing documents automatically.
2. Extracting and highlighting key entities such as names, organizations, dates, and monetary values.
3. Detecting high-risk clauses in contracts.
4. Enabling semantic searches that focus on the meaning behind queries.

### Table of Contents
- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)


## Installation
Prerequisites:
Python 3.8+ should be installed on your system.
It is recommended to use a virtual environment for managing dependencies.
Git should be installed to clone the repository.
Tesseract OCR for text extraction from scanned PDFs (ensure this is installed).
Steps:
Clone the repository using Git:
    git clone https://github.com/username/contract-search-engine.git
    cd contract-search-engine

(Optional) Create a virtual environment:
    python -m venv venv
    source venv/bin/activate  # For Linux/Mac
    .\venv\Scripts\activate   # For Windows

Install dependencies:
    pip install -r requirements.txt

Run the application:
    python app.py

Access the web interface by opening your browser and going to http://localhost:5000.

## Features 
- Document Summarization:
Automatically generate summaries of lengthy contracts to highlight key clauses and points.
Uses NLP-based summarization algorithms, including transformers, to extract the most important sentences.
- Entity Identification:
Detects and highlights important entities within a document.
Entities include organizations, people, dates, and monetary amounts.
Uses Named Entity Recognition (NER) models from SpaCy and transformer-based models.
- Risk Identification:
Identifies clauses in a contract that pose legal risks.
Examples of risky clauses include termination, penalties, and liability clauses.
Includes both rule-based and ML-based methods for detecting risky clauses.
- Semantic Search:
Allows users to search for clauses and terms based on their meaning rather than exact matches.
The system uses Sentence Transformers or BERT to convert text and queries into vectors and then performs a cosine similarity comparison to find relevant sections of the contract.

## Usage 
Uploading Contracts:
Navigate to the Contract Search Engine interface.
Click on the "Select PDF" button to upload a contract document in PDF format.
The document can either be a text-based PDF or a scanned PDF (where OCR will be applied).
Viewing Results:
Once the document is uploaded, you can select various options like Summarize, Entity Identification, and Risk Identification.
The results will be displayed on the right side of the interface, with key entities and risky clauses highlighted.
Downloading Annotated Documents:
After identifying entities and risks, the annotated document can be downloaded using the provided link.
The document will contain highlights and annotations for easier navigation.

## Acknowledgements
### Technical Details
Libraries and Technologies Used:
Backend: Flask (for web server), PyPDF2 (for PDF parsing), PyTesseract (for OCR).
Frontend: HTML, CSS, JavaScript for the web interface.
NLP: SpaCy for Named Entity Recognition, OpenAI GPT for summarization.
OCR: pdf2image for converting PDF pages to images, PyTesseract for OCR.
Search: Sentence Transformers/BERT for semantic search.

### Workflow and How It Works
- Data Ingestion and Preprocessing:
    Normal PDFs: The text is extracted using PyPDF2.
    Scanned PDFs: OCR is applied using pdf2image and PyTesseract.
- Text Summarization:
    Preprocess the text by converting to lowercase, removing stopwords, and tokenizing.
    Use frequency-based methods and transformer models to extract important sentences.
- Entity Identification:
    Pre-trained models like SpaCy's NER are used to identify entities.
    Entities such as ORG (organization), PERSON (individual), MONEY (monetary amounts), and DATE (dates) are detected.
- Risk Identification:
    Rule-based: Use regex patterns to find terms related to risk (e.g., "termination", "liability").
    ML-based: Fine-tuned BERT models to detect risky clauses based on context.
- Semantic Search:
    Vectorization: Sentences and queries are converted into vectors using models like Sentence Transformers.
    Cosine Similarity: The system compares query vectors to document vectors and returns the most relevant sections.
