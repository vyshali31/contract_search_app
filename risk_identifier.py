import openai
from openai import AzureOpenAI
import textwrap
import json
from cred_secrets import get_openai, AZURE_OPENAI_DEPLOYMENT, prompt_risk
from extraction import get_text_from_pdf
from summarize_ai import split_text_into_chunks
import re

def identify_risk(text):
    try:
        openai = get_openai()
        prompt = prompt_risk + text
        response = openai.chat.completions.create(
            model=AZURE_OPENAI_DEPLOYMENT,
            messages=[{"role": "user", "content": prompt}],
        )
        summary = response.choices[0].message.content
        return summary
    except Exception as e:
        print(f"Error while summarizing: {e}")
        return None



# Define a function to summarize the entire document
def identify_risk_in_document(filename, max_tokens=7000):

    text = get_text_from_pdf(filename)
    # Step 1: Split the large text into manageable chunks
    chunks = split_text_into_chunks(text, max_tokens)

    # Step 2: Summarize each chunk
    risks = " "
    for chunk in chunks:
        risk = identify_risk(chunk)
        # risks.append(risk)
        risks += risk
    
    risks = re.sub(r'}\s*,\s*{', '\n------------------------------------------------\n', risks)
    risks = re.sub(r'}{', '\n------------------------------------------------\n', risks)
    risks = re.sub(r'}\s*]{', '\n------------------------------------------------\n', risks)

    # risks = risks.split('--------------------')


    # Step 3: Combine the summaries into a single document
    # risks = "\n".join(risks)
    return risks


if __name__ == "__main__":
    
    filename = "GCC MSA.pdf"

    risk_json = identify_risk_in_document(filename)
    print(risk_json)


