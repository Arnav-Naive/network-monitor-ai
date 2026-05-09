import sys
from pathlib import Path

# Added project root to Python path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import django
import random
import time
from datetime import datetime

# Django setup
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from monitor.models import SwitchMetric

import pickle
import numpy as np

# Load trained model
try:
    with open('anomaly_model.pkl', 'rb') as f:
        ml_model = pickle.load(f)
    print("✓ ML model loaded\n")
    USE_ML = True
except FileNotFoundError:
    print("⚠ No ML model found. Run train_model.py first.")
    print("Using threshold-based detection for now.\n")
    USE_ML = False

def get_snmp_data():
    return {
        "cpu_usage": random.randint(10, 95),
        "memory_usage": random.randint(20, 90),
        "temperature": random.randint(30, 85),
        "bandwidth": random.randint(100, 900),
        "interface_status": random.choice([1, 1, 1, 0]),
        "crc_errors": random.randint(0, 5),
        "reliability": f"{random.randint(250, 255)}/255",
        "tx_rate": random.randint(100, 1000),
        "rx_rate": random.randint(100, 1000),
    }

THRESHOLDS = {
    "cpu_usage": 80,
    "temperature": 75,
    "bandwidth": 800,
}

def detect_anomaly(data):
    anomalies = []
    
    if USE_ML:
        # ML-based detection
        features = np.array([[
            data['cpu_usage'],
            data['memory_usage'],
            data['temperature'],
            data['bandwidth'],
            data['crc_errors'],
            data['tx_rate'],
            data['rx_rate']
        ]])
        
        prediction = ml_model.predict(features)[0]
        
        if prediction == -1:  # -1 = anomaly
            anomalies.append("ML DETECTED ANOMALY")
    
    # Keep threshold checks too (backup)
    if data["cpu_usage"] > THRESHOLDS["cpu_usage"]:
        anomalies.append(f"HIGH CPU: {data['cpu_usage']}%")
    if data["temperature"] > THRESHOLDS["temperature"]:
        anomalies.append(f"HIGH TEMP: {data['temperature']}C")
    if data["interface_status"] == 0:
        anomalies.append("PORT DOWN")
    
    return anomalies

print("Starting Network Monitor (Database mode)...\n")

try:
    while True:
        data = get_snmp_data()
        anomalies = detect_anomaly(data)
        
        # Save to database
        metric = SwitchMetric.objects.create(
            cpu_usage=data['cpu_usage'],
            memory_usage=data['memory_usage'],
            temperature=data['temperature'],
            bandwidth=data['bandwidth'],
            interface_status=data['interface_status'],
            crc_errors=data['crc_errors'],
            reliability=data['reliability'],
            tx_rate=data['tx_rate'],
            rx_rate=data['rx_rate'],
            anomalies=', '.join(anomalies) if anomalies else None
        )
        
        print(f"{metric.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | CPU: {data['cpu_usage']}% | Temp: {data['temperature']}C | Status: {'UP' if data['interface_status'] else 'DOWN'}")
        
        if anomalies:
            print(f"  ⚠ ANOMALY: {', '.join(anomalies)}")
        else:
            print(f"  ✓ Normal")
        
        time.sleep(5)
        
except KeyboardInterrupt:
    print("\n\nMonitor stopped. Data saved to database.")