import pandas as pd
import matplotlib.pyplot as plt
import json

def process_data(info):
    data = pd.DataFrame.from_dict(info, orient='index', columns=['CREDIT', 'RENT', 'longitude', 'latitude','Meterage','District', "Construction","Parking","Elevator","Warehouse"])

    districts = set(data['District'])

    data['CREDIT'] /= 1_000_000
    data['RENT'] /= 1_000_000
    data['longitude'], data['latitude'] = data['longitude'].astype(float), data['latitude'].astype(float)
    mask_prices = (data['CREDIT'] < 100) | (data['CREDIT'] > 2000) | (data['RENT'] < 1) | (data['RENT'] > 100)
    data = data.loc[~mask_prices].dropna(subset=['CREDIT', 'RENT'])

    locs = data[['longitude', 'latitude']].dropna()
    mask_locs = (locs['latitude'] > 36) | (locs['latitude'] < 35.55) | (locs['longitude'] < 51.10) | (locs['longitude'] > 51.60)
    data_location = data.loc[~(mask_locs|mask_prices)].dropna()
    return data, data_location, districts

files_path = "Results/apartment-rent/1/"
 
with open(files_path+"table.json" , encoding='utf-8') as f:
    info = json.load(f)

print("Data read complete.")
data, data_location, districts = process_data(info=info)
print("Data process complete.")

data_all_true = data[(data["Parking"] == True) & (data["Elevator"] == True) & (data["Warehouse"] == True)]

data_all_true_poonak = data_all_true[data_all_true["District"] == "پونک"]
print(data_all_true_poonak)


plt.scatter(data_all_true_poonak['Meterage'],data_all_true_poonak['CREDIT'])
plt.show()
