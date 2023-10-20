import json
import os

def extract_data(file_path):
    # Load the data from the JSON file
    with open(file_path, encoding='utf-8') as f:
        info = json.load(f)
    
    # Extract the desired data from the JSON structure
    data = {
        "Date": info.get("widgets").get('header').get('date'),
        "RENT": info.get("data").get("webengage").get("rent"),
        "CREDIT": info.get("data").get("webengage").get("credit"),
        "CITY": info.get("data").get("webengage").get("city"),
        "Meterage": info.get("widgets").get('list_data')[0].get("items")[0].get('value'),
        "Construction": info.get("widgets").get('list_data')[0].get("items")[1].get('value'),
        "ROOMS": info.get("widgets").get('list_data')[0].get("items")[2].get('value'),
        "floor": info.get("widgets").get('list_data')[6].get("value"),
        "Elevator": info.get("widgets").get('list_data')[7].get("items")[0].get("available"),
        "Parking": info.get("widgets").get('list_data')[7].get("items")[1].get("available"),
        "Warehouse": info.get("widgets").get('list_data')[7].get("items")[2].get("available"),
        "location": info.get("data").get("lacation")
    }
    
    return data

def create_new_dict(data):
    # Create a new dictionary with the desired key-value pairs
    new_dict = {
        "CITY": data["CITY"],
        "Date": data["Date"],
        "RENT": data["RENT"],
        "CREDIT": data["CREDIT"],
        "Meterage": int(data["Meterage"]),
        "Construction": int(data["Construction"]),
        "Parking": data["Parking"],
        "Elevator": data["Elevator"],
        "Warehouse": data["Warehouse"],
        "floor": data["floor"],
        "location": data["location"]
    }
    
    return new_dict


# Example usage
files_path = os.listdir("Results/apartment-rent/2/")

print(files_path)

# Extract the data from the JSON file
data = extract_data(file_path)

# Create a new dictionary with the selected key-value pairs
new_dict = create_new_dict(data)

# Print the new diction