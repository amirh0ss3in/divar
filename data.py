import pandas as pd
import matplotlib.pyplot as plt
import json

def process_data(info):
    data = pd.DataFrame.from_dict(info, orient='index', columns=['PRICE', 'longitude', 'latitude','Meterage','District', "Construction","Parking","Elevator","Warehouse"])

    districts = set(data['District'])

    data['PRICE'] /= 1_000_000
    data['longitude'], data['latitude'] = data['longitude'].astype(float), data['latitude'].astype(float)
    # mask_prices = (data['PRICE'] < 100) | (data['PRICE'] > 2000)
    # data = data.loc[~mask_prices].dropna(subset=['PRICE'])


    return data, districts

files_path = "Results/apartment-sell/1/"
 
with open(files_path+"table.json" , encoding='utf-8') as f:
    info = json.load(f)


print("Data read complete.")
data, districts = process_data(info=info)
print("Data process complete.")

# data_all_true = data[(data["Parking"] == True) & (data["Elevator"] == True) & (data["Warehouse"] == True)]
data_all_true = data

print(data_all_true["District"].describe())

data_all_true_poonak = data_all_true[data_all_true["District"] == "سعادت‌آباد"]


plt.scatter(data_all_true_poonak['Meterage'], data_all_true_poonak['PRICE'])
plt.show()
