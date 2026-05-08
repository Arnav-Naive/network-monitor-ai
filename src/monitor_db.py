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
    if data["cpu_usage"] > THRESHOLDS["cpu_usage"]:
        anomalies.append(f"HIGH CPU: {data['cpu_usage']}%")
    if data["temperature"] > THRESHOLDS["temperature"]:
        anomalies.append(f"HIGH TEMP: {data['temperature']}C")
    if data["bandwidth"] > THRESHOLDS["bandwidth"]:
        anomalies.append(f"HIGH BANDWIDTH: {data['bandwidth']} Mbps")
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