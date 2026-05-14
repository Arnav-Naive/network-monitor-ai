import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import django
import time
from datetime import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from monitor.alerts import send_anomaly_alert

from monitor.models import SwitchMetric

# pysnmp v7 imports (new API)
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.smi import builder, view, compiler
import asyncio
from asgiref.sync import sync_to_async

import pickle
import numpy as np

# Extended OIDs for custom metrics
OIDS = {
    'cpu': '1.3.6.1.4.1.8072.1.3.2.3.1.2.3.99.112.117',
    'memory': '1.3.6.1.4.1.8072.1.3.2.3.1.2.6.109.101.109.111.114.121',
    'temperature': '1.3.6.1.4.1.8072.1.3.2.3.1.2.11.116.101.109.112.101.114.97.116.117.114.101',
    'bandwidth': '1.3.6.1.4.1.8072.1.3.2.3.1.2.9.98.97.110.100.119.105.100.116.104',
}

async def get_snmp_value(oid):
    """Poll single OID from Docker SNMP container"""
    try:
        snmpEngine = SnmpEngine()
        
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            snmpEngine,
            CommunityData('public'),
            await UdpTransportTarget.create(('127.0.0.1', 161), timeout=2, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        
        snmpEngine.close_dispatcher()
        
        if errorIndication:
            print(f"SNMP Error: {errorIndication}")
            return None
        if errorStatus:
            print(f"SNMP Status Error: {errorStatus.prettyPrint()}")
            return None
        
        for varBind in varBinds:
            value = str(varBind[1]).strip()
            try:
                return int(value)
            except ValueError:
                return None
    except Exception as e:
        print(f"Exception polling {oid}: {e}")
        return None

async def get_snmp_data():
    """Collect all metrics from Docker SNMP switch"""
    cpu = await get_snmp_value(OIDS['cpu']) or 50
    memory = await get_snmp_value(OIDS['memory']) or 60
    temp = await get_snmp_value(OIDS['temperature']) or 45
    bandwidth = await get_snmp_value(OIDS['bandwidth']) or 500
    
    data = {
        "cpu_usage": cpu,
        "memory_usage": memory,
        "temperature": temp,
        "bandwidth": bandwidth,
        "interface_status": 1,
        "crc_errors": 0,
        "reliability": "255/255",
        "tx_rate": bandwidth,
        "rx_rate": bandwidth - 50,
    }
    return data

# Load ML model
try:
    with open('anomaly_model.pkl', 'rb') as f:
        ml_model = pickle.load(f)
    print("✓ ML model loaded\n")
    USE_ML = True
except FileNotFoundError:
    print("⚠ No ML model found. Using threshold detection only.\n")
    USE_ML = False

THRESHOLDS = {
    "cpu_usage": 80,
    "temperature": 75,
    "bandwidth": 800,
}

def detect_anomaly(data):
    anomalies = []
    
    if USE_ML:
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
        if prediction == -1:
            anomalies.append("ML DETECTED ANOMALY")
    
    if data["cpu_usage"] > THRESHOLDS["cpu_usage"]:
        anomalies.append(f"HIGH CPU: {data['cpu_usage']}%")
    if data["temperature"] > THRESHOLDS["temperature"]:
        anomalies.append(f"HIGH TEMP: {data['temperature']}C")
    if data["interface_status"] == 0:
        anomalies.append("PORT DOWN")
    
    return anomalies

async def save_to_database(data, anomalies):
    @sync_to_async
    def create_metric():
        from monitor.alerts import send_anomaly_alert
        
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
        
        # Send email only for ML detections (not every threshold alert)
        if anomalies and 'ML DETECTED' in ', '.join(anomalies):
            send_anomaly_alert(metric, anomalies)
        
        return metric
    
    return await create_metric()

async def monitor_loop():
    print("Starting SNMP Network Monitor (Docker Edition)...\n")
    print("Polling Docker SNMP switch at 127.0.0.1:161\n")
    
    try:
        while True:
            data = await get_snmp_data()
            anomalies = detect_anomaly(data)
            
            # Save to database (async wrapped)
            metric = await save_to_database(data, anomalies)
            
            print(f"{metric.timestamp.strftime('%Y-%m-%d %H:%M:%S')} | CPU: {data['cpu_usage']}% | Temp: {data['temperature']}C | Mem: {data['memory_usage']}%")
            
            if anomalies:
                print(f"  ⚠ ANOMALY: {', '.join(anomalies)}")
            else:
                print(f"  ✓ Normal")
            
            await asyncio.sleep(10)
            
    except KeyboardInterrupt:
        print("\n\nMonitor stopped. Data saved to database.")

if __name__ == "__main__":
    asyncio.run(monitor_loop())