import openai
from openai import AzureOpenAI
import textwrap
from cred_secrets import get_openai, AZURE_OPENAI_DEPLOYMENT
import re

# Import a tokenizer to accurately count tokens (assuming GPT models)
from transformers import GPT2TokenizerFast

# Initialize a tokenizer (adjust this based on your actual model)
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")

def summarize_text(text, number_sentence = 5):
    try:
        openai = get_openai()
        prompt = f"Summarize the following text in {number_sentence} sentences: {text}"
        response = openai.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"Error while summarizing: {e}")
        return None

# Define a function to split the document into chunks
 ##def split_text_into_chunks(text, max_tokens):
    """
    Split the input text into chunks, where each chunk is no longer than max_tokens.
    """
    # Adjust max_tokens to characters limit (approx. assuming 1 token ≈ 4 characters)
  ##   max_characters = max_tokens * 4

    # Use textwrap to split into chunks of approximately max_characters
  ##   chunks = textwrap.wrap(text, max_characters)

 ##   return chunks

# Define a function to split the document into chunks based on tokens
def split_text_into_chunks(text, max_tokens):
    """
    Split the input text into chunks, where each chunk is no longer than max_tokens.
    """
    tokens = tokenizer.tokenize(text)

    # Split tokens into chunks
    chunks = []
    current_chunk = []
    current_token_count = 0

    for token in tokens:
        current_token_count += 1
        current_chunk.append(token)

        if current_token_count >= max_tokens:
            chunks.append(tokenizer.convert_tokens_to_string(current_chunk))
            current_chunk = []
            current_token_count = 0

    # Add any remaining tokens in the last chunk
    if current_chunk:
        chunks.append(tokenizer.convert_tokens_to_string(current_chunk))

    return chunks


# Define a function to summarize the entire document
def generate_summary_llm(text, max_tokens=6000):
    """
    Split the document into chunks, summarize each chunk, and return a combined summary.
    """

    # Split the large text into manageable chunks
    chunks = split_text_into_chunks(text, max_tokens)

    #Summarize each chunk
    chunk_summaries = []
    for chunk in chunks:
        summary = summarize_text(chunk)
        chunk_summaries.append(summary)

    # Combine all chunk summaries into a final summary
    final_summary = "\n".join(chunk_summaries)

    return final_summary

def clean_text(text):
    """
    Clean the input text to remove sensitive or policy-violating content.
    """
    blacklist = ['violence', 'self-harm', 'sexual', 'jailbreak']
    
    for word in blacklist:
        text = re.sub(rf'\b{word}\b', '[REDACTED]', text, flags=re.IGNORECASE)

    return text

# Example usage
if __name__ == "__main__":
    

    with open("output_docs/GCC MSA.pdf.txt", "r") as file:
        extracted_text = file.read()
    
     # Clean the extracted text
    cleaned_text = clean_text(extracted_text)

    # Define the max token size (e.g., 2048 tokens)
    max_tokens = 6000

    # Get the combined summary of the large document
    final_summary = generate_summary_llm(extracted_text, max_tokens)

    print("Final Summary:\n", final_summary)

