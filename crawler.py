import concurrent.futures
import datetime
import json
import logging
import os
from time import sleep

import requests
from requests.exceptions import ConnectionError, HTTPError, RequestException
from urllib3.exceptions import MaxRetryError


def fetch_json_data(token):
    url = f'{BASE_URL}/posts/{token}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        logging.error(f"Failed to fetch data for token {token}: {str(e)}")
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON for token {token}: {str(e)}")

def fetch_and_save_post(token, category, city_code):
    j = fetch_json_data(token)
    if j:
        save_json(j, category, city_code, token)
        
def save_json(j, category, city_code, token):
    json_path = f"{RESULTS_DIR}/{category}/{city_code}/"
    with open(f'{json_path}/{token}.json', 'w', encoding='utf-8') as f:
        json.dump(j, f, ensure_ascii=False, indent=4)
        logging.info(f"Saved: {token}")
        print(f"saved {token}", end="\r")

def retrieve_page(url, json_payload, headers, MAX_RETRY_ATTEMPTS):
    for _ in range(MAX_RETRY_ATTEMPTS):
        try:
            start_time = datetime.datetime.now()
            res = requests.post(url, json=json_payload, headers=headers)
            res.raise_for_status()
            response_time = (datetime.datetime.now() - start_time).total_seconds()
            
            # Adjust sleep time dynamically based on response time
            sleep_time = max(0.6, 2 - response_time)
            sleep(sleep_time)
            return res.json()
        except (RequestException, MaxRetryError, ConnectionError, HTTPError) as e:
            logging.error(f"An error occurred: {str(e)}")
            sleep(2)

def date_to_unix(DTS): 
    return int(datetime.datetime.strptime(DTS, "%Y-%m-%d %H:%M:%S").timestamp()) * 1_000_000

def scrape(city_code, category, date_time_str, MAX_PAGES, MAX_RETRY_ATTEMPTS):
    unix_timestamp = date_to_unix(date_time_str)
    last_post_date = unix_timestamp

    headers = {
        "Content-Type": "application/json"
    }
    url = f"{BASE_URL}/search/{city_code}/{category}"

    page_count = 1

    try:
        while page_count <= MAX_PAGES:
            json_payload = {
                "json_schema": {
                    "category": {"value": category}
                },
                "last-post-date": last_post_date,
                "page": page_count
            }

            data = retrieve_page(url, json_payload, headers, MAX_RETRY_ATTEMPTS)

            if data is None:
                break

            if not data.get("web_widgets", {}).get("post_list"):
                break

            post_list = data["web_widgets"]["post_list"]
            
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = []

                for post in post_list:
                    if "action" in post["data"]:
                        if "token" in post["data"]["action"]["payload"]:
                            token = post["data"]["action"]["payload"]["token"]
                            futures.append(executor.submit(fetch_and_save_post, token, category, city_code))

                for future in concurrent.futures.as_completed(futures):
                    pass  # TODO I can add any post-level processing here if needed

            last_post_date = data["last_post_date"]
            logging.info(f"Page {page_count} scraped. Last post date = {last_post_date}")
            page_count += 1

    except KeyboardInterrupt:
        logging.info("Scraping interrupted by user.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {str(e)}")


if __name__ == "__main__":

    BASE_URL = "https://api.divar.ir/v8"
    RESULTS_DIR = "Results"
    category="apartment-rent"
    city_code=1
    
    # Configure logging
    json_path = f"{RESULTS_DIR}/{category}/{city_code}/"
    if not os.path.exists(json_path):
        os.makedirs(json_path)
    logging.basicConfig(filename=json_path+"scrape_log.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
    
    scrape(city_code=city_code, category=category, date_time_str="2023-09-11 11:30:00", MAX_PAGES=4, MAX_RETRY_ATTEMPTS=5)
