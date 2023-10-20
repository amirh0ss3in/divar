import json
import os
import logging
from json.decoder import JSONDecodeError


def extract_data(file_path):
    """Extracts the desired data from the JSON file."""

    with open(file_path, encoding='utf-8') as f:
        info = json.load(f)

    data = {
        "Date": info.get("widgets").get("header").get("date"),
        "RENT": info.get("data").get("webengage").get("rent"),
        "CREDIT": info.get("data").get("webengage").get("credit"),
        "CITY": info.get("data").get("webengage").get("city"),
        "Meterage": info.get("widgets").get("list_data")[0].get("items")[0].get("value"),
        "Construction": info.get("widgets").get("list_data")[0].get("items")[1].get("value"),
        "ROOMS": info.get("widgets").get("list_data")[0].get("items")[2].get("value"),
        "floor": info.get("widgets").get("list_data")[6].get("value"),
        "Elevator": info.get("widgets").get("list_data")[7].get("items")[0].get("available"),
        "Parking": info.get("widgets").get("list_data")[7].get("items")[1].get("available"),
        "Warehouse": info.get("widgets").get("list_data")[7].get("items")[2].get("available"),
        "location": info.get("data").get("lacation")
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
        "location": data["location"]
    }

    return new_dict

def main():
    """Main function."""

    files_path = "Results/apartment-rent/1/"
    files_names = os.listdir(files_path)
    logging.basicConfig(filename="errors.log", level=logging.INFO)

    success = 0 
    for file_name in files_names:
        try:
            data = extract_data(files_path + file_name)
            new_dict = create_new_dict(data)
            # print(new_dict)
            success += 1
        except FileNotFoundError:
            logging.error(f"File not found: {file_name}")
            print(f"File not found: {file_name}")
        except JSONDecodeError:
            logging.error(f"Invalid JSON file: {file_name}")
            print(f"Invalid JSON file: {file_name}")
        except:
            logging.error(f"Unexpected error: {file_name}")
            print(f"Unexpected error: {file_name}")
    fail = len(files_names) - success
    print("failed:",fail)
    print("success:",success)

if __name__ == "__main__":
    main()
