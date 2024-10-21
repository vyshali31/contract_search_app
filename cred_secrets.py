from openai import AzureOpenAI

## Azure OpenAI Pinky
AZURE_OPENAI_API_VERSION='2024-02-01' 
AZURE_OPENAI_API_KEY='33815ca4065e492c80d7cdc95e84e0a1'
AZURE_OPENAI_ENDPOINT='https://azure-openaitest-test-001.openai.azure.com/'
AZURE_OPENAI_IMAGE_MODEL = 'Testdall-e-3'
AZURE_OPENAI_DEPLOYMENT='Test001' 
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT='EmbeddingTest'

# Azure FR ENDPOINT Pinky
FR_ENDPOINT = "https://formrecognizer14.cognitiveservices.azure.com/"
FR_KEY = "d2448531d84f4ea8a591c5c6d11d5bf0"


def get_openai():
    return AzureOpenAI(
        azure_endpoint = AZURE_OPENAI_ENDPOINT, 
        api_key= AZURE_OPENAI_API_KEY,  
        api_version=AZURE_OPENAI_API_VERSION
    )

prompt_risk1 = '''
    I have a contract agreement, and I need help identifying risk-related statements. A risk statement in a contract typically refers to clauses or sections that outline potential problems, liabilities, or uncertainties that may affect one or more parties involved. These risks may include, but are not limited to:
    Give the output in a json format with each risk statement, risk type, and explanation. Dont give any other information in the output, I need to use this in another python program.
    
    text to analyze: 
    '''
prompt_risk = '''
    I have a contract agreement, and I need help identifying risk-related statements. A risk statement in a contract typically refers to clauses or sections that outline potential problems, liabilities, or uncertainties that may affect one or more parties involved. These risks may include, but are not limited to:

    Please analyze the below text and idenitify all statements that reflect potential risks. 
    For each risk statement, provide the following information:
    statement:
        That are specific sentence or clause that presents a risk from the given text. Dont change it.
    type: 
        means Whether it is a financial risk, legal risk, operational risk, etc. Its defition is as follows:
        Financial risks: Statements that mention potential loss of money, financial penalties, refunds, cost overruns, or payment issues.
        Legal liabilities: Clauses that assign responsibility or blame for potential legal action, non-compliance with regulations, breach of contract, or intellectual property issues.
        Operational risks: Risks related to delays, failures in service delivery, or inability to meet obligations.
        Third-party risks: Statements that mention the involvement of subcontractors, vendors, or other external parties, and the potential risks associated with their involvement.
        Force majeure risks: Clauses that describe unexpected events or circumstances (e.g., natural disasters, pandemics, strikes, or acts of God) that might prevent either party from fulfilling their contractual obligations.
        Confidentiality and data security risks: Sections that outline potential risks related to breaches of confidentiality, data leaks, or failure to protect sensitive information.
        Termination clauses: Statements that outline under what circumstances the contract can be terminated and the consequences of early termination.
        Dispute resolution: Clauses that explain how disputes will be resolved and the risks associated with arbitration, litigation, or other conflict resolution mechanisms.

    explanation: 
        A brief explanation of why this clause represents a risk to either party.

    Sample output. Each findings should be enclose in {}, I need to use it as json.  strictly Dont change the format of the output.:
     {
         "statement": "The CONTRACTOR may fail to perform its obligations satisfactorily and may be subject to deductions from the Contract Price.",
         "type": "Performance Risk",
         "explanation": "Clause 14 sets out the Performance Standards that the CONTRACTOR must meet and the deductions that ADB may apply if the CONTRACTOR falls below these standards."
      },
      {
         "statement": "The CONTRACTOR may not disclose conflicts of interest and may be subject to termination of the Contract.",
         "type": "Ethical Risk",
         "explanation": "Clause 7 requires the CONTRACTOR to take appropriate steps to avoid conflicts of interest and to disclose any such conflicts to ADB. Failure to do so may result in termination of the Contract."
      }

    Text to analyze: '''



