import numpy as np
from sklearn.decomposition import PCA
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json

with open("Results/apartment-rent/1/table.json" , encoding='utf-8') as f:
    info = json.load(f)

data = pd.DataFrame.from_dict(info, orient='index', columns=['CREDIT', 'RENT', 'longitude', 'latitude','Meterage'])
data['CREDIT'] /= 1000000
data['RENT'] /= 1000000
data['longitude'], data['latitude'] = data['longitude'].astype(float), data['latitude'].astype(float)

locs = data[['longitude', 'latitude']].dropna()
mask_locs = (locs['latitude'] > 36) | (locs['latitude'] < 35.55) | (locs['longitude'] < 51.10) | (locs['longitude'] > 51.60)
locs = locs.loc[~mask_locs]


# hist, xedges, yedges = np.histogram2d(locs['longitude'], locs['latitude'], bins=20)
# plt.imshow(hist.T, origin='lower', extent=[xedges[0], xedges[-1], yedges[0], yedges[-1]], cmap='viridis')
# plt.colorbar()
# plt.xlabel('longitude')
# plt.ylabel('latitude')
# plt.title('Heatmap of Credit and Rent Data')
# plt.show()

df = pd.DataFrame(data, columns=['CREDIT', 'RENT'])

mask_prices = (df['CREDIT'] < 100) | (df['CREDIT'] > 2000) | (df['RENT'] < 1) | (df['RENT'] > 100)
df = df.loc[~mask_prices]
df = df.dropna()

print(data.dropna(), '\n',data.loc[~(mask_locs|mask_prices)].dropna())

pca = PCA()
# pca_fit = pca.fit_transform(data.loc[~(mask_locs|mask_prices)].dropna())
pca_fit = pca.fit_transform(df)

conversion_rate = pca.components_[0,1]

print(f'Conversion Rate: {conversion_rate*100 :.2f}%')