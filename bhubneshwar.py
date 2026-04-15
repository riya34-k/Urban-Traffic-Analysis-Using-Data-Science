import pandas as pd
df = pd.read_csv("traffic_bhubaneswar.csv")
print(df.columns)
print(df.head())
print(df.info())
df = df.dropna(subset=['speed_ratio', 'congestion_level'])
import matplotlib.pyplot as plt
top_segments = df.groupby('segment_id')['speed_ratio'].mean().nsmallest(5).index
filtered = df[df['segment_id'].isin(top_segments)]
pivot = filtered.pivot_table(
    values='speed_ratio',
    index='hour_of_day',
    columns='segment_id',
    aggfunc='mean')
pivot.plot(figsize=(10,6))
plt.title("Traffic by Hour (Top Segments - Bhubaneswar)")
plt.show()
import seaborn as sns
pivot = df.pivot_table(
    values='speed_ratio',
    index='day_of_week',
    columns='hour_of_day',
    aggfunc='mean')
plt.figure(figsize=(10,6))
sns.heatmap(pivot, cmap='coolwarm')
plt.title("Traffic Heatmap (Day vs Hour) - Bhubaneswar")
plt.xlabel("Hour")
plt.ylabel("Day (0=Mon, 6=Sun)")
plt.show()