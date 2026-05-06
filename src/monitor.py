import random
import time
import csv
import os
from datetime import datetime

# Create data folder if it doesn't exist
os.makedirs("data", exist_ok=True)


# Simulated SNMP data
def get_snmp_data():
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "cpu_usage": random.randint(10, 95),
        "temperature": random.randint(30, 85),
        "bandwidth": random.randint(100, 900),
        "port_status": random.choice([1, 1, 1, 0]),
    }


# Thresholds
THRESHOLDS = {"cpu_usage": 80, "temperature": 75, "bandwidth": 800, "port_status": 1}


def detect_anomaly(data):
    anomalies = []
    if data["cpu_usage"] > THRESHOLDS["cpu_usage"]:
        anomalies.append(f"HIGH CPU: {data['cpu_usage']}%")
    if data["temperature"] > THRESHOLDS["temperature"]:
        anomalies.append(f"HIGH TEMP: {data['temperature']}C")
    if data["bandwidth"] > THRESHOLDS["bandwidth"]:
        anomalies.append(f"HIGH BANDWIDTH: {data['bandwidth']} Mbps")
    if data["port_status"] == 0:
        anomalies.append("PORT DOWN")
    return anomalies


def save_to_csv(data, anomalies):
    file_exists = os.path.isfile("data/logs.csv")
    with open("data/logs.csv", "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(
                [
                    "timestamp",
                    "cpu_usage",
                    "temperature",
                    "bandwidth",
                    "port_status",
                    "anomalies",
                ]
            )
        writer.writerow(
            [
                data["timestamp"],
                data["cpu_usage"],
                data["temperature"],
                data["bandwidth"],
                data["port_status"],
                ", ".join(anomalies) if anomalies else "None",
            ]
        )


# Main loop
print("Starting Network Monitor...\n")
try:
    while True:
        data = get_snmp_data()
        anomalies = detect_anomaly(data)

        print(
            f"{data['timestamp']} | CPU: {data['cpu_usage']}% | Temp: {data['temperature']}C | Bandwidth: {data['bandwidth']}Mbps | Port: {'UP' if data['port_status'] else 'DOWN'}"
        )

        if anomalies:
            print(f"  ⚠ ANOMALY: {', '.join(anomalies)}")
        else:
            print(f"  ✓ Normal")

        save_to_csv(data, anomalies)
        time.sleep(5)
except KeyboardInterrupt:
    print("\n\nMonitor stopped. Data saved to data/logs.csv")
