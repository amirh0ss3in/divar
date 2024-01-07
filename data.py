import pandas as pd
import matplotlib.pyplot as plt
import json

def process_data(info):
    data = pd.DataFrame.from_dict(info, orient='index', columns=['PRICE', 'longitude', 'latitude','Meterage','District', "Construction","Parking","Elevator","Warehouse"])

    districts = set(data['District'])

    data['PRICE'] /= 1_000_000
    data['longitude'], data['latitude'] = data['longitude'].astype(float), data['latitude'].astype(float)

    return data, districts

files_path = "Results/apartment-sell/1/"
 
with open(files_path+"table.json" , encoding='utf-8') as f:
    info = json.load(f)


print("Data read complete.")
data, districts = process_data(info=info)
print("Data process complete.")

data_district = data[data["District"] == "پونک"]

plt.scatter(data_district['Meterage'], data_district['PRICE'], c=data_district['Construction'])
plt.colorbar()
plt.show()

# import itertools

# # Define the features and their possible values
# features = ["Parking", "Elevator", "Warehouse"]
# values = [True, False]

# # Generate all permutations of True and False for the three features
# permutations = list(itertools.product(values, repeat=len(features)))

# # Create a color map
# colors = ['r', 'g', 'b', 'm', 'y', 'k', 'orange']


# plt.figure(figsize=(10, 5))

# for i, permutation in enumerate(permutations):
#     # Filter the data based on the current permutation
#     data_permutation = data[(data["Parking"] == permutation[0]) & 
#                             (data["Elevator"] == permutation[1]) & 
#                             (data["Warehouse"] == permutation[2])]
    
#     data_permutation_district = data_permutation[data_permutation["District"] == "سعادت‌آباد"]
    
#     # Create a scatter plot for the current permutation
#     plt.scatter(data_permutation_district['Meterage'], data_permutation_district['PRICE'], color=colors[i % len(colors)], label=f'Parking: {permutation[0]}, Elevator: {permutation[1]}, Warehouse: {permutation[2]}')

# plt.title('Meterage vs PRICE for different feature permutations')
# plt.xlabel('Meterage')
# plt.ylabel('PRICE')
# plt.legend()
# plt.tight_layout()
# plt.show()

