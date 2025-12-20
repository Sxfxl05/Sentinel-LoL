import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

# 1. Load your existing data
df = pd.read_csv("data/process_logs.csv")

# 2. Extract features (using the same logic as your detector)
df['length'] = df['command_line'].apply(len)
df['entropy'] = df['command_line'].apply(lambda x: -sum([float(x.count(c))/len(x) * 0.5 for c in set(x)])) # Simplified for plotting

# 3. Re-run the model for the plot
model = IsolationForest(contamination=0.2)
df['anomaly'] = model.fit_predict(df[['length', 'entropy']])

# 4. Create the Plot
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x='length', y='entropy', hue='anomaly', palette={1: 'blue', -1: 'red'}, s=100)

plt.title("Sentinel-LoL: Behavioral Anomaly Detection", fontsize=15)
plt.xlabel("Command Length", fontsize=12)
plt.ylabel("Shannon Entropy (Randomness)", fontsize=12)
plt.legend(title='Detection', labels=['Threat (Anomaly)', 'Normal'])
plt.grid(True, linestyle='--', alpha=0.6)

# 5. Save the image to your project folder
plt.savefig("detection_graph.png")
print("✅ Success! Graph saved as 'detection_graph.png'.")