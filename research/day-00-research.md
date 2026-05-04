# Day 00 — Pre-Internship Research
**Date:** 2025-05-04  
**Project:** AI-Powered Network Switch Monitoring System  
**Source:** Self-study (NetworkChuck, Gate Smashers, networklessons.com)

---

## 1. What is a Network?

A network is a system of connected devices that share data with each other.

**Basic flow (home example):**
```
My PC → Switch → Router → Firewall → Modem → ISP → Internet
```

| Device | Role |
|---|---|
| **Switch** | Connects multiple devices within a local network |
| **Router** | Connects different networks together |
| **Firewall** | Filters traffic — blocks bad, allows good |
| **Modem** | Connects your home network to the ISP |

---

## 2. Network Switch — Deep Dive

### Hub vs Switch
| Hub | Switch |
|---|---|
| Sends message to ALL devices | Sends message only to the intended device |
| Dumb — no memory | Smart — remembers MAC addresses |
| Creates collisions | Zero collision domain |

### How a Switch Works
- Switch operates at **Layer 2 (Data Link Layer)** of the OSI model
- It does NOT see Layer 3 (IP addresses)
- It only works with **MAC addresses**
- Stores MAC addresses in a **CAM Table (Content Addressable Memory)**

**Two key rules:**
- CAM table is populated using → **Source MAC address**
- Forwarding decisions are made using → **Destination MAC address**

### Switch vs Bridge
- Bridge = connects two LANs, Layer 2 device
- Switch = **multiport bridge** (24, 48 ports)
- Switch is better because it supports many devices: computers, laptops, printers, wireless devices

### Switch Advantages
- Full duplex link (send and receive simultaneously)
- Minimum traffic
- Zero collision domain

### Wireless Access Points
- Do the same job as a switch but wirelessly
- Behave more like a hub (broadcasts to everyone) — which is why wired ethernet is faster and more reliable

---

## 3. SNMP — Simple Network Management Protocol

### What is SNMP?
A protocol created to monitor and manage network devices (switches, routers, servers) from one central place.

- **Layer:** Application Layer
- **Protocol:** UDP
- **Port 161** → General queries (GET, SET)
- **Port 162** → Trap messages (alerts)
- **Latest version:** SNMPv3 (most secure, encrypted)

### Three Core Components

| Component | What it is |
|---|---|
| **SNMP Manager** | Software on a server that monitors devices (also called NMS — Network Management System) |
| **SNMP Agent** | Software running on the device being monitored (switch, router, server) |
| **MIB** | Management Information Base — a database of all monitorable variables on a device |

### OID — Object Identifier
- Every piece of data in the MIB has a unique ID called an OID
- Example OIDs: CPU usage, interface status, temperature, port up/down

### Key SNMP Messages

| Message | Purpose |
|---|---|
| **GET** | Manager asks agent: "what is your current CPU usage?" |
| **SET** | Manager tells agent: "change this configuration value" |
| **TRAP** | Agent sends alert to manager on its own: "something went wrong" |

### Management Based on 3 Ideas
1. Manager requests info from agent
2. Manager can force agent to perform a task (by resetting values)
3. Agent warns manager about unusual situations (via Traps)

---

## 4. Where AI Fits In

### Normal (Dumb) Monitoring
```
if CPU > 80%:
    send_alert()
```
Problem: threshold is hardcoded. False alarms, missed anomalies.

### AI-Powered Monitoring
```
Model learns normal behavior of each switch over time
→ Flags deviations from that pattern
→ No hardcoded rules needed
```

### Project Architecture
```
Network Switch
     ↓ (SNMP Agent)
Python Script (polls switch via SNMP GET)
     ↓
Collected Metrics: CPU, temperature, port status, bandwidth
     ↓
ML Model (anomaly detection)
     ↓
Alert / Dashboard (Django UI or Grafana)
```

**Tech stack expected:** Python, pysnmp, scikit-learn (or LSTM), Django, possibly Grafana

---

## 5. Questions to Ask Mentor on Day 1

1. What specific metrics are we monitoring — port status, CPU, temperature, traffic?
2. Are we building the anomaly detection model from scratch or integrating with existing tools like Zabbix or Grafana?
3. What is the tech stack already decided — are we using Python, and do we have access to actual switches or simulated data?

---

*Notes by Arnav | Tata Prashikshan Internship 2026*