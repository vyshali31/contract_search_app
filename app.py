from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from extraction import get_text_from_pdf, get_json_from_pdf
from summarize import generate_custom_summary
from summarize_ai import generate_summary_llm
from risk_identifier import identify_risk_in_document
from semantic_search import search_clauses_in_text
from entity_identification import extract_entities_from_pdf

app = Flask(__name__)
UPLOAD_FOLDER = 'input_docs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def get_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return files

@app.route('/')
def index():
    # Get the list of files in the upload folder
    files = get_files()
    return render_template('index.html', files=files)
  
@app.route('/summarize_page')
def summarize_page():
    files = get_files()
    return render_template('summarize.html', files=files)

@app.route('/semantic_search_page') 
def semantic_search_page():
    files = get_files()
    return render_template('semantic_search.html', files=files)

@app.route('/search', methods=['POST'])
def search():
    data = request.get_json()  # Get data from JSON body
    search_term = data.get('search_term')
    filename = data.get('filename')

    text = get_text_from_pdf(filename)
    matching_sentences = search_clauses_in_text(text, search_term)
    return jsonify({'results': matching_sentences})

@app.route('/get-file/<filename>', methods=['GET'])
def get_file_content(filename):
    print("Getting file content for ", filename)
    text = get_text_from_pdf(filename)
    return jsonify({'text': text})

@app.route('/summarize', methods=['POST'])
def summarize():
    data = request.get_json()
    text = data.get('text', '')
    usellm = int(data.get('llm',1))
    print("usellm = ", usellm)
    num_sentences = int(data.get('num_sentences', 5))
    if usellm == 1:
        print("Using LLM for summarization")
        summary = generate_summary_llm(text)
    else:
        print("Using custom summarization")
        summary = generate_custom_summary(text, num_sentences=num_sentences)
    return jsonify({'summary': summary})

#ENTITY IDENTIFIER

@app.route('/entity_identifier')
def entity_identifier():
    files = get_files()
    return render_template('entity_identifier.html', files=files)

@app.route('/identify_entities', methods=['POST'])
def identify_entities():
    data = request.json
    filename = data.get('filename')

    if filename:
        entities = extract_entities_from_pdf(filename)
        return jsonify({'entities': entities})
    else:
        return jsonify({'error': 'No filename provided'}), 400


# Route to serve the selected PDF file
@app.route('/pdf/<filename>')
def get_pdf(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# RISK IDENTIFIER

@app.route('/identify_risks', methods=['POST'])
def identify_risks():
    data = request.get_json()
    filename = data.get('filename')
    
    if filename:
        risks = identify_risk_in_document(filename)  # Get risks as tuples
        print("Risks:--->",risks[:10])
        return jsonify({'risks': risks})
    return jsonify({'error': 'No file selected'}), 400


@app.route('/risk_identifier')
def risk_identifier():
    
    files = get_files()    
    return render_template('risk_identifier.html', risks="", files=files)

if __name__ == '__main__':
    app.run(debug=True, port=5000)

  