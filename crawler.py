import requests
import pandas as pd
from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError
from time import sleep
import datetime
import json
import os
  

def fetch_json_data(token):
    url = f'https://api.divar.ir/v8/posts/{token}'

    response = requests.get(url)

    if response.status_code == 200:
        j = response.json()
        return j
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return None
    
def save_json(j, category, city_code, token):
    json_path = f"Results/ category_{category}__city_{city_code}"
    if not os.path.exists(json_path):    
        os.makedirs(json_path)
    with open(f'{json_path}/{token}.json', 'w', encoding='utf-8') as f:
        json.dump(j, f, ensure_ascii=False, indent=4)
        print(f"saved: {token}", end="\r")

def retrieve_page(url, json_payload, headers, MAX_RETRY_ATTEMPTS):
    for _ in range(MAX_RETRY_ATTEMPTS):
        try:
            res = requests.post(url, json=json_payload, headers=headers)
            sleep(0.6)
            res.raise_for_status()
            return res.json()
        except (RequestException, MaxRetryError) as e:
            print(f"An error occurred: {str(e)}")
            sleep(30)
    return None

def date_to_unix(DTS): 
    return int(datetime.datetime.strptime(DTS, "%Y-%m-%d %H:%M:%S").timestamp()) * 1_000_000

def scrape(city_code, category, date_time_str, MAX_PAGES, MAX_RETRY_ATTEMPTS):
    unix_timestamp = date_to_unix(date_time_str)
    last_post_date = unix_timestamp

    headers = {
        "Content-Type": "application/json"
    }
    url = f"https://api.divar.ir/v8/search/{city_code}/{category}"

    page_count = 1

    try:
        while True:
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

            for post in post_list:
                if "token" in post["data"]["action"]["payload"]:
                    token = post["data"]["action"]["payload"]["token"]
                    j = fetch_json_data(token)
                    save_json(j, category, city_code, token)

            last_post_date = data["last_post_date"]
            print(page_count, end="\r")
            if page_count == MAX_PAGES:
                break
            page_count += 1

    except KeyboardInterrupt:
        print("Scraping interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


# categories = {"real-estate":{"buy": ["apartment-sell", "house-villa-sell", "plot-old"],
#                             "rent": ["apartment-rent", "house-villa-rent"]}
#                 }

scrape( city_code = 5,
        category = "plot-old",
        date_time_str = "2023-09-08 00:00:00",
        MAX_PAGES = 2000,
        MAX_RETRY_ATTEMPTS = 5
    )

