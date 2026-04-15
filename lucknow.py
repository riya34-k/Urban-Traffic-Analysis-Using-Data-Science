import pandas as pd
df = pd.read_csv("lucknow_traffic_cleaned.csv")
print(df.columns)
print(df.head())
print(df.info())
df['Date'] = pd.to_datetime(df['Date'])
peak_hour = df.groupby('Hour')['Queue_Density'].mean()
import matplotlib.pyplot as plt
pivot = df.pivot_table(
    values='Queue_Density',
    index='Hour',
    columns='Location',
    aggfunc='mean').fillna(0)
pivot.plot(figsize=(10,6))
plt.title("Traffic by Hour for Different Areas")
plt.ylabel("Queue Density")
plt.show()
loc = df.groupby('Location')['Queue_Density'].mean()
loc.plot(kind='bar')
plt.title("Average Traffic by Location")
plt.ylabel("Queue Density")
plt.show()
import seaborn as sns
pivot = df.pivot_table(
    values='Queue_Density',
    index='Location',
    columns='Hour',
    aggfunc='mean')
plt.figure(figsize=(10,6))
sns.heatmap(pivot, cmap='coolwarm')
plt.title("Traffic Heatmap (Location vs Hour)")
plt.xlabel("Hour")
plt.ylabel("Location")
plt.show()

