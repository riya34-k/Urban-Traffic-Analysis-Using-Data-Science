import pandas as pd
df = pd.read_csv("Banglore_traffic_Dataset.csv")
print(df.columns)
print(df.head())
print(df.info())
df['Date'] = pd.to_datetime(df['Date'])
print(df['Date'].head())
top_areas = df.groupby('Area Name')['Traffic Volume'].sum().sort_values(ascending=False)
print(top_areas.head())
import matplotlib.pyplot as plt
top_areas.head().plot(kind='bar')
plt.title("Top Congested Areas in Bengaluru")
plt.xlabel("Area")
plt.ylabel("Traffic Volume")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
df['Date'] = pd.to_datetime(df['Date'])
df['Day'] = df['Date'].dt.day_name()
pivot = df.pivot_table(
    values='Traffic Volume',
    index='Area Name',
    columns='Day',
    aggfunc='sum')
order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
pivot = pivot[order]
import seaborn as sns
plt.figure(figsize=(10,6))
sns.heatmap(pivot, cmap='coolwarm')
plt.title("Traffic Heatmap (Area vs Day)")
plt.xlabel("Day")
plt.ylabel("Area")
plt.show()
plt.figure(figsize=(10,6))
plt.hexbin(
    df['Traffic Volume'],
    df['Average Speed'],
    gridsize=40)
plt.xlabel("Traffic Volume")
plt.ylabel("Average Speed")
plt.title("Traffic Volume vs Average Speed (Density View)")
plt.colorbar(label='Number of Points')
plt.show()