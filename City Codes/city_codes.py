import requests
import pandas as pd
city_codes = []

for city_code in range(1,40):
    url = f'https://api.divar.ir/v8/search/{city_code}/apartment-sell'

    last_post_date = 0
    headers = {
        "Content-Type": "application/json"
    }

    page_count = 0

    json_payload = {
        "json_schema": {
            "category": {"value": "apartment-sell"}
        },
        "last-post-date": last_post_date
    }
    res = requests.post(url, json=json_payload, headers=headers)
    data = res.json()
    if not data.get('web_widgets', {}).get('post_list'):
        break
    post_list = data['web_widgets']['post_list']

    for post in post_list:
        if 'data' in post and 'action' in post['data'] and 'payload' in post['data']['action']:
            if 'token' in post['data']['action']['payload'] and 'title' in post['data'] and 'top_description_text' in post['data'] and 'middle_description_text' in post['data'] and 'bottom_description_text' in post['data'] and 'web_info' in post['data']['action']['payload']:  
                city = post['data']['action']['payload']['web_info']['city_persian']
                print(city_code, city)
                city_codes.append([city_code, city])
                break

excel_filename = 'city_codes.xlsx'
df = pd.DataFrame(city_codes, columns=["city_code", "city"])
df.to_excel(excel_filename, index=False)
print(f'Data has been saved to {excel_filename}')
