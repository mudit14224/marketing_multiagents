# Imports
import json
import re
import pandas as pd

# Extract json from string for contact
def extract_json_from_string(input_string):
    # Regular expression to find JSON within triple backticks
    pattern = r"```json(.*?)```"
    match = re.search(pattern, input_string, re.DOTALL)
    if match:
        json_string = match.group(1).strip()
        try:
            # Parse the JSON string
            json_data = json.loads(json_string)
            
            # Function to ensure all fields have values
            def ensure_fields(entry):
                if "LinkedIn" not in entry:
                    entry["LinkedIn"] = ""
                if "Phone no." not in entry:
                    entry["Phone no."] = ""
                if "Email address" not in entry:
                    entry["Email address"] = ""
                return entry
            
            # If json_data is a dictionary, convert it to a list of one dictionary
            if isinstance(json_data, dict):
                json_data = [ensure_fields(json_data)]
            elif isinstance(json_data, list):
                json_data = [ensure_fields(entry) for entry in json_data]
            else:
                return "Unexpected JSON format. Expected a dictionary or list of dictionaries."

            return json_data
        except json.JSONDecodeError as e:
            return f"Error decoding JSON: {e}"
    else:
        return "No JSON found within triple backticks."

# json to df    
def json_to_dataframe(json_data):
    # Check if the JSON data is a list of dictionaries
    if isinstance(json_data, list) and all(isinstance(item, dict) for item in json_data):
        # Convert the list of dictionaries to a pandas DataFrame
        df = pd.DataFrame(json_data)
        return df
    else:
        raise ValueError("Invalid JSON data format. Expected a list of dictionaries.")
    
