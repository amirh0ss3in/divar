import requests
import pandas as pd
from requests.exceptions import RequestException
from urllib3.exceptions import MaxRetryError
from time import sleep
import datetime

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

    scraped_data = []
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
                if "data" in post and "action" in post["data"] and "payload" in post["data"]["action"]:
                    if "token" in post["data"]["action"]["payload"] and "title" in post["data"] and "top_description_text" in post["data"] and "middle_description_text" in post["data"] and "bottom_description_text" in post["data"] and "web_info" in post["data"]["action"]["payload"]:
        
                        token = post["data"]["action"]["payload"]["token"]
                        title = post["data"]["title"]
                        middle_description = post["data"]["middle_description_text"]
                        bottom_description = post["data"]["bottom_description_text"]
                        top_description = post['data']['top_description_text']

                        district = post["data"]["action"]["payload"]["web_info"]["district_persian"]
                        city = post["data"]["action"]["payload"]["web_info"]["city_persian"]
                        category_slug = post["data"]["action"]["payload"]["web_info"]["category_slug_persian"]

                        scraped_data.append([token, title, top_description, middle_description, bottom_description, district, city, category_slug, last_post_date])

            last_post_date = data["last_post_date"]
            print(page_count, end="\r")
            if page_count == MAX_PAGES:
                break
            page_count += 1

    except KeyboardInterrupt:
        print("Scraping interrupted by user.")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

    excel_filename = f"category_{category}__city_{city_code}.xlsx"
    df = pd.DataFrame(scraped_data, columns=["Token", "Title", "Top Description", "Middle Description", "Bottom Description", "District", "City", "Category Slug", "Last Post Date"])
    df.to_excel("Results/"+excel_filename, index=False)
    print(f"Data has been saved to {excel_filename}")



categories = {"real-estate":{"buy": ["apartment-sell", "house-villa-sell", "plot-old"],
                            "rent": ["apartment-rent", "house-villa-rent"]}
                }

scrape( city_code = 1,
        category = "apartment-rent",
        date_time_str = "2023-09-06 21:00:00",
        MAX_PAGES = 2000,
        MAX_RETRY_ATTEMPTS = 5
    )
