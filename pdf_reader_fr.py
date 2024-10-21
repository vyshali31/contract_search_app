import os
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient, AnalysisFeature
from pdf_post_proc import convert_to_chunk_list
from cred_secrets import FR_ENDPOINT, FR_KEY


def extract_pdf_to_json(file_path):
    try:
        document_analysis_client = DocumentAnalysisClient(FR_ENDPOINT, AzureKeyCredential(FR_KEY))

        file_byte = open(file_path, "rb").read()
        if file_byte is None:
            return "Error reading PDF file. Either an empty file or file not selected."
        poller = document_analysis_client.begin_analyze_document("prebuilt-layout", file_byte,
                                                                features=[AnalysisFeature.OCR_HIGH_RESOLUTION,
                                                                        AnalysisFeature.STYLE_FONT])
        result = poller.result()
        chunk_list = convert_to_chunk_list(result.to_dict(), "eng")
        return chunk_list
    except Exception as e:
        print(f"Error while extracting PDF to JSON: {e}")
        return f"Error while extracting PDF to JSON: {e}"



