import re
import json
from risk_identifier import identify_risk_in_document

def extract_risk_tuples(text):
    # Clean the text to make sure it can be properly parsed as JSON
    text = re.sub(r"(\w+):", r'"\1":', text)  # Ensure keys are properly quoted for JSON parsing
    text = re.sub(r"(\d+):", r'"\1":', text)  # Ensure numbers as keys are quoted too
    text = text.replace("'", '"')  # Replace single quotes with double quotes to make it valid JSON
    text = text.replace("\\n", ' ')
    text = re.sub(r'\\(?=")', '', text)
    text = re.sub(r'(?<!\\)"', r'\"', text)
    text = re.sub(r'(\w+):', r'"\1":', text)



    risk_tuples = []

    # Extract all JSON-like objects from the text
    json_objects = re.findall(r'{.*?}', text, re.DOTALL)

    for json_obj in json_objects:
        try:
            # Try loading the JSON object
            data = json.loads(json_obj)

            # Process if it's a dictionary containing risk statements
            if "statements" in data:
                for item in data["statements"]:
                    risk_tuples.append((item.get("type"), item.get("explanation")))
            elif isinstance(data, list):
                # Process list items
                for item in data:
                    risk_tuples.append((item.get("statement"), item.get("type"), item.get("explanation")))
            elif "risks" in data:
                # Process risks in risks key
                for item in data["risks"]:
                    risk_tuples.append((item.get("statement"), item.get("type"), item.get("explanation")))
            else:
                # Process numbered keys in dictionaries
                for key in data:
                    risk = data[key]
                    risk_tuples.append((risk.get("statement"), risk.get("type"), risk.get("explanation")))
        except json.JSONDecodeError:
            # If parsing fails, continue to next object
            print(f"Error parsing JSON: {json_obj}")
            continue

    return risk_tuples


if __name__ == "__main__":
    # Sample text to test the function
    filename = "GCC MSA.pdf"

    text = identify_risk_in_document(filename)
    text = json.dumps(text)

    # Call the function with the given text
    risk_tuples = extract_risk_tuples(text)

    print("Extracted risk tuples:")
    # Display the extracted tuples
    for risk in risk_tuples:
        print(risk)
