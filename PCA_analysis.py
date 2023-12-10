from sklearn.decomposition import PCA
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
from bidi.algorithm import get_display
from arabic_reshaper import reshape
import matplotlib.ticker as mtick
import os
import numpy as np
import geopandas as gpd
import contextily as cx

def process_data(info):
    data = pd.DataFrame.from_dict(info, orient='index', columns=['CREDIT', 'RENT', 'longitude', 'latitude','Meterage','District'])

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

from scipy.spatial import cKDTree


def location_grid(data_location):
    
    hist, xedges, yedges = np.histogram2d(data_location['longitude'], data_location['latitude'], bins=20)
    x, y = np.meshgrid(xedges[:-1], yedges[:-1])
    coords = np.stack([x.ravel(), y.ravel()], axis=1)
    tree = cKDTree(coords)
    dist, idx = tree.query(data_location[['longitude', 'latitude']].values)
    
    grouped_data = data_location[['RENT', 'CREDIT']].groupby(idx)

    counts = grouped_data.size()
    sorted_groups = counts.sort_values(ascending=False)
    # plot the grouped datas together with their coords:
    colors = np.zeros(coords.shape[0])

    # Set the color for each group based on its count
    for i, count in enumerate(counts):
        colors[i] = count

    # Plot the grouped data together with their coordinates
    plt.figure(figsize=(10, 10))
    plt.scatter(coords[:, 0], coords[:, 1], c=colors, cmap='viridis')
    plt.colorbar(label='Number of data points')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Grouped Data')
    plt.show()
    return grouped_data


def plot_data_location(data_location):
    data_location['geometry'] = gpd.points_from_xy(data_location['longitude'], data_location['latitude'])
    data_location = gpd.GeoDataFrame(data_location, geometry='geometry', crs='EPSG:4326')
    data_location = data_location.to_crs(epsg=3857)
    ax = data_location.plot(figsize=(10, 10), alpha=0.5, edgecolor="k",column='RENT')
    cx.add_basemap(ax, zoom=12, source=cx.providers.OpenStreetMap.Mapnik)
    plt.show()

def compute_PCA_districts(files_path, treshhold, plot_map = False):
    with open(files_path+"table.json" , encoding='utf-8') as f:
        info = json.load(f)
    print("Data read complete.")
    data, data_location, districts = process_data(info=info)
    print("Data process complete.")

    if plot_map:
        # grouped_data = location_grid(data_location=data_location)
        plot_data_location(data_location=data_location)
    
    conversion_rates = {}
    pca = PCA()
    pca.fit_transform(data[['CREDIT', 'RENT']])
    conversion_rate_all = abs(pca.components_[0,1])
    
    PCA_path = files_path.replace("Results", "PCA_Results")
    if not os.path.isdir(PCA_path):
        os.makedirs(PCA_path)
    district_scatter_path = PCA_path+"/district_scatters"
    if not os.path.isdir(district_scatter_path):
            os.makedirs(district_scatter_path)

    for district in districts:
        data_district = data.loc[data['District'] == district]

        if len(data_district) > treshhold:
            pca = PCA()
            pca.fit_transform(data_district[['CREDIT', 'RENT']])
            d = data_district[['CREDIT', 'RENT']]
            conversion_rate = abs(pca.components_[0,1])
            conversion_rates[district] = conversion_rate

            plt.scatter(d['CREDIT'], d['RENT'])
            plt.title(f"{get_display(reshape(district))} , {conversion_rate*100 :.2f}%")
            plt.savefig(district_scatter_path+f"/{district}.png")
            plt.close()

    # Sort the conversion_rates dictionary by values in ascending order
    sorted_rates = sorted(conversion_rates.items(), key=lambda x: x[1])
    # Create two lists for the sorted district names and conversion rates
    sorted_districts = [x[0] for x in sorted_rates]
    sorted_rates = [x[1] for x in sorted_rates]
    
    fig = plt.figure(figsize=(16, 8))
    
    with open(PCA_path+'conversion_rates.json', 'w', encoding='utf-8') as f:
        json.dump(conversion_rates, f, ensure_ascii=False, indent=4)
        
    persian_labels = [get_display(reshape(label)) for label in sorted_districts]
    plt.bar(persian_labels, sorted_rates)
    plt.xticks(rotation=90, ha='right', fontsize = 8)
    plt.xlabel('District')
    plt.ylabel('Conversion Rate')
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    plt.title(f"Conversion Rate All: {conversion_rate_all * 100 :.2f}%")
    plt.tight_layout()
    plt.savefig(PCA_path+"bar_plot.png")
    # plt.show()

compute_PCA_districts(files_path = "Results/apartment-rent/1/",
                      treshhold=10,
                      plot_map=True)

