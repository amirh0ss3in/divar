import json
import os
import logging
from json.decoder import JSONDecodeError
import pandas as pd
from tqdm import tqdm

import json

def extract_data(file_path):
    # Load the data from the JSON file
    with open(file_path, encoding='utf-8') as f:
        info = json.load(f)
    
    # Extract the desired data from the JSON structure
    try:
        elevator_available = info.get("widgets").get('list_data')[7].get("items")[0].get("available")
    except (AttributeError, IndexError, KeyError):
        elevator_available = info.get("widgets").get('list_data')[6].get("items")[0].get("available")
    
    try:
        parking_available = info.get("widgets").get('list_data')[7].get("items")[1].get("available")
    except (AttributeError, IndexError, KeyError):
        parking_available = info.get("widgets").get('list_data')[6].get("items")[1].get("available")
    
    try:
        warehouse_available = info.get("widgets").get('list_data')[7].get("items")[2].get("available")
    except (AttributeError, IndexError, KeyError):
        warehouse_available = info.get("widgets").get('list_data')[6].get("items")[2].get("available")
    
    data = {
        "Date": info.get("widgets").get('header').get('date'),
        "RENT": info.get("data").get("webengage").get("rent"),
        "CREDIT": info.get("data").get("webengage").get("credit"),
        "CITY": info.get("data").get("webengage").get("city"),
        "Meterage": info.get("widgets").get('list_data')[0].get("items")[0].get('value'),
        "Construction": info.get("widgets").get('list_data')[0].get("items")[1].get('value'),
        "ROOMS": info.get("widgets").get('list_data')[0].get("items")[2].get('value'),
        "floor": info.get("widgets").get('list_data')[6].get("value"),
        "Elevator": elevator_available,
        "Parking": parking_available,
        "Warehouse": warehouse_available,
        "district" : info.get("data").get("district"),
        "latitude": info.get("widgets").get("location").get("latitude"),
        "longitude": info.get("widgets").get("location").get("longitude")
    }
    return data

def create_new_dict(data):
    """Creates a new dictionary with the desired key-value pairs."""

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
        "latitude": data["latitude"],
        "longitude": data["longitude"],
        "District": data['district']
    }

    return new_dict

def main(files_path):
    """Main function."""
    files_names = os.listdir(files_path)
    logging.basicConfig(filename="errors.log", level=logging.INFO)
    table = {}
    success = 0
    for file_name in tqdm(files_names):
        try:
            data = extract_data(files_path + file_name)
            new_dict = create_new_dict(data)
            success += 1
            table[file_name.removesuffix(".json")] = new_dict

        except FileNotFoundError:
            logging.error(f"File not found: {file_name}")
        except JSONDecodeError:
            logging.error(f"Invalid JSON file: {file_name}")
        except:
            logging.error(f"Unexpected error: {file_name}")

    with open(files_path+'table.json', 'w', encoding='utf-8') as f:
        json.dump(table, f, ensure_ascii=False, indent=4)
        
    print(f"success ratio: {100*success/len(files_names) :.2f}%")
    
if __name__ == "__main__":
    main(files_path = "Results/apartment-rent/1/")
