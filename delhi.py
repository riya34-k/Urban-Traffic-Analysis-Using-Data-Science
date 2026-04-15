import geopandas as gpd
import os
import pandas as pd
base_folder = r"C:\Users\DELL\Downloads\new delhi traffic\new_delhi_traffic_dataset\probe_counts"
all_gdfs = []
for subfolder in os.listdir(base_folder):
    subfolder_path = os.path.join(base_folder, subfolder)
    if os.path.isdir(subfolder_path): 
        for file in os.listdir(subfolder_path):
            if file.endswith('.geojson'):  
                file_path = os.path.join(subfolder_path, file)
                gdf = gpd.read_file(file_path)
                all_gdfs.append(gdf)
merged_gdf = gpd.GeoDataFrame(pd.concat(all_gdfs, ignore_index=True))
print("Total rows after merge:", len(merged_gdf))
print(merged_gdf.head())
print(merged_gdf.columns)
print(merged_gdf.info())
print(merged_gdf.isnull().sum())
print(merged_gdf.geometry.head())  
print(merged_gdf.geometry.type.value_counts())
columns_to_keep = ['segmentId', 'newSegmentId', 'streetName', 'speedLimit', 'distance', 'frc', 'segmentProbeCounts', 'geometry']
cleaned_gdf = merged_gdf[columns_to_keep]
print("Missing values per column:")
print(cleaned_gdf.isnull().sum())
cleaned_gdf['streetName'] = cleaned_gdf['streetName'].fillna('Unknown')
print(cleaned_gdf.head())
print(cleaned_gdf['segmentProbeCounts'].iloc[1])
cleaned_gdf['total_probe_count'] = cleaned_gdf['segmentProbeCounts'].apply(
    lambda x: sum(item['probeCount'] for item in x) if isinstance(x, list) else 0)
print(cleaned_gdf[['segmentId', 'total_probe_count']].head())
print("Total rows:", len(cleaned_gdf))
print("Unique segments:", cleaned_gdf['segmentId'].nunique())
cleaned_gdf['segmentId'] = cleaned_gdf['segmentId'].astype(str)
final_delhi = cleaned_gdf.groupby('segmentId', as_index=False).agg({
    'total_probe_count': 'sum',
    'geometry': 'first',
    'streetName': 'first',
    'speedLimit': 'first',
    'distance': 'first',
    'frc': 'first'})
print("Unique segments after grouping:", len(final_delhi))
print(final_delhi.head())
final_delhi['traffic_density'] = final_delhi['total_probe_count'] / final_delhi['distance']
print(final_delhi[['segmentId', 'traffic_density']].head())
top_congested = final_delhi.sort_values(by='traffic_density', ascending=False)
print(top_congested[['streetName', 'traffic_density']].head(10))
print(top_congested[['streetName', 'total_probe_count', 'distance', 'traffic_density']].head(5))
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("whitegrid")
top_roads = final_delhi.nlargest(10, "traffic_density") #Top 10 Most Congested Roads
plt.figure(figsize=(10,6))
sns.barplot(
    x="traffic_density",
    y="streetName",
    data=top_roads,)
plt.title("Top 10 Most Congested Roads in Delhi", fontsize=14)
plt.xlabel("Traffic Density")
plt.ylabel("Road Name")
plt.tight_layout()
plt.show()
plt.figure(figsize=(10,6)) #Traffic Density Distribution
plt.hist(final_delhi["traffic_density"], bins=50)
plt.xscale("log")  
plt.title("Distribution of Traffic Density in Delhi", fontsize=14)
plt.xlabel("Traffic Density (Log Scale)")
plt.ylabel("Number of Road Segments")
plt.tight_layout()
plt.show()
plt.figure(figsize=(10,6)) #Traffic Density vs Road Distance
plt.scatter(
    final_delhi["distance"],
    final_delhi["traffic_density"],
    alpha=0.3)
plt.yscale("log")  
plt.title("Traffic Density vs Road Distance", fontsize=14)
plt.xlabel("Road Distance")
plt.ylabel("Traffic Density (Log Scale)")
plt.tight_layout()
plt.show()
import geopandas as gpd #Delhi Traffic Map
gdf = gpd.GeoDataFrame(final_delhi, geometry='geometry')
fig, ax = plt.subplots(figsize=(12, 10))
gdf.plot(
    column="traffic_density",
    cmap="Reds",
    linewidth=2,
    legend=True,
    vmin=gdf['traffic_density'].quantile(0.2),
    vmax=gdf['traffic_density'].quantile(0.95),
    figsize=(12,10))
ax.set_title("Delhi Traffic Density Map")
plt.show()
