import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from monitor.models import SwitchMetric
from sklearn.ensemble import IsolationForest
import pickle
import numpy as np

print("Training anomaly detection model...\n")

# Get all data from database
data = SwitchMetric.objects.all().values_list(
    'cpu_usage', 
    'memory_usage', 
    'temperature', 
    'bandwidth',
    'crc_errors',
    'tx_rate',
    'rx_rate'
)

if len(data) < 50:
    print(f"Not enough data yet. Have {len(data)} records, need at least 50.")
    print("Run monitor_db.py for a few more minutes, then try again.")
    exit()

# Convert to numpy array
X = np.array(data)

print(f"Training on {len(X)} data points...")

# Train Isolation Forest
model = IsolationForest(
    contamination=0.1,  # expect 10% of data to be anomalies
    random_state=42
)
model.fit(X)

# Save model to file
with open('anomaly_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✓ Model trained and saved to anomaly_model.pkl")
print(f"✓ Model learned patterns from {len(X)} samples")