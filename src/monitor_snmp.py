import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import django
import asyncio

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from monitor.models import SwitchMetric, Switch
from monitor.alerts import send_anomaly_alert
from asgiref.sync import sync_to_async

from pysnmp.hlapi.v3arch.asyncio import *
import pickle
import numpy as np

OIDS = {
    'cpu': '1.3.6.1.4.1.8072.1.3.2.3.1.2.3.99.112.117',
    'memory': '1.3.6.1.4.1.8072.1.3.2.3.1.2.6.109.101.109.111.114.121',
    'temperature': '1.3.6.1.4.1.8072.1.3.2.3.1.2.11.116.101.109.112.101.114.97.116.117.114.101',
    'bandwidth': '1.3.6.1.4.1.8072.1.3.2.3.1.2.9.98.97.110.100.119.105.100.116.104',
}

async def get_snmp_value(ip, port, oid):
    try:
        snmpEngine = SnmpEngine()
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            snmpEngine,
            CommunityData('public'),
            await UdpTransportTarget.create((ip, port), timeout=2, retries=1),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        snmpEngine.close_dispatcher()

        if errorIndication or errorStatus:
            return None

        for varBind in varBinds:
            try:
                return int(str(varBind[1]).strip())
            except ValueError:
                return None
    except Exception as e:
        return None

async def poll_switch(switch):
    """Poll all metrics from one switch"""
    ip = switch.ip_address
    port = switch.port

    cpu = await get_snmp_value(ip, port, OIDS['cpu']) or 50
    memory = await get_snmp_value(ip, port, OIDS['memory']) or 60
    temp = await get_snmp_value(ip, port, OIDS['temperature']) or 45
    bandwidth = await get_snmp_value(ip, port, OIDS['bandwidth']) or 500

    return {
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

# Load ML model
try:
    with open('anomaly_model.pkl', 'rb') as f:
        ml_model = pickle.load(f)
    print("✓ ML model loaded\n")
    USE_ML = True
except FileNotFoundError:
    print("⚠ No ML model. Using threshold detection only.\n")
    USE_ML = False

THRESHOLDS = {"cpu_usage": 85, "temperature": 78, "bandwidth": 850}

def detect_anomaly(data):
    anomalies = []
    if USE_ML:
        features = np.array([[
            data['cpu_usage'], data['memory_usage'], data['temperature'],
            data['bandwidth'], data['crc_errors'], data['tx_rate'], data['rx_rate']
        ]])
        if ml_model.predict(features)[0] == -1:
            anomalies.append("ML DETECTED ANOMALY")

    if data["cpu_usage"] > THRESHOLDS["cpu_usage"]:
        anomalies.append(f"HIGH CPU: {data['cpu_usage']}%")
    if data["temperature"] > THRESHOLDS["temperature"]:
        anomalies.append(f"HIGH TEMP: {data['temperature']}C")
    if data["interface_status"] == 0:
        anomalies.append("PORT DOWN")
    return anomalies

@sync_to_async
def get_switches():
    return list(Switch.objects.filter(is_active=True))

@sync_to_async
def save_metric(switch, data, anomalies):
    from channels.layers import get_channel_layer
    from asgiref.sync import async_to_sync

    metric = SwitchMetric.objects.create(
        switch=switch,
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

    if anomalies and 'ML DETECTED' in ', '.join(anomalies):
        send_anomaly_alert(metric, anomalies)

    # Push to WebSocket
    try:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'metrics',
            {
                'type': 'metrics_update',
                'data': {
                    'switch': switch.name,
                    'cpu': data['cpu_usage'],
                    'memory': data['memory_usage'],
                    'temperature': data['temperature'],
                    'bandwidth': data['bandwidth'],
                    'anomalies': ', '.join(anomalies) if anomalies else None,
                    'timestamp': metric.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                }
            }
        )
        print(f"  📡 WebSocket push sent")
    except Exception as e:
        print(f"  ❌ WebSocket push failed: {e}")

    return metric

async def monitor_loop():
    print("Starting Multi-Switch SNMP Monitor...\n")

    while True:
        switches = await get_switches()

        tasks = [poll_switch(switch) for switch in switches]
        results = await asyncio.gather(*tasks) # polls all 3 switches simultaneously (faster and realistic)

        for switch, data in zip(switches, results):
            anomalies = detect_anomaly(data)
            metric = await save_metric(switch, data, anomalies)

            status = "⚠ " + ', '.join(anomalies) if anomalies else "✓ Normal"
            print(f"{switch.name} | CPU: {data['cpu_usage']}% | Temp: {data['temperature']}C | {status}")

        print("---")
        await asyncio.sleep(10)

if __name__ == "__main__":
    asyncio.run(monitor_loop())