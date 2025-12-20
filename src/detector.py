import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

# 1. Feature Engineering: Turning text into numbers for the AI
def extract_features(cmd):
    return {
        'length': len(cmd),
        'entropy': -sum([float(cmd.count(c))/len(cmd) * np.log2(float(cmd.count(c))/len(cmd)) for c in set(cmd)]),
        'spec_char_count': len([c for c in cmd if c in '-/\\$()[]" ']),
        'is_encoded': 1 if '-enc' in cmd.lower() or 'base64' in cmd.lower() else 0
    }

# 2. Loading the Data
df = pd.read_csv("data/process_logs.csv")
features_list = [extract_features(cmd) for cmd in df['command_line']]
X = pd.DataFrame(features_list)

# 3. Initializing the AI Model
# 'contamination' is the % of data we expect to be malicious
model = IsolationForest(contamination=0.1, random_state=42)

# 4. Training and Predicting
df['anomaly_score'] = model.fit_predict(X) 
# Note: -1 = Anomaly (Threat), 1 = Normal

# 5. Output results
print("\n--- SENTINEL-LOL DETECTION REPORT ---")
for idx, row in df.iterrows():
    status = "🚨 THREAT DETECTED" if row['anomaly_score'] == -1 else "✅ NORMAL"
    print(f"{status} | Command: {row['command_line'][:60]}...")