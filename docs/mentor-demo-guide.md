# Project Demo Guide — For Mentor Presentation

## What I Built

**AI-Powered Network Switch Monitoring System**

A system that collects network switch metrics, uses machine learning to detect unusual patterns, and displays alerts on a web dashboard.

---

## Key Components

### 1. Data Collection (`monitor_db.py`)
- Polls switch every 5 seconds (simulated data currently)
- Collects 9 metrics: CPU, Memory, Temp, Bandwidth, Interface status, CRC errors, Reliability, TX/RX rates
- Saves to SQLite database

### 2. Machine Learning (`train_model.py` + Isolation Forest)
- Trains on historical data (currently 341 samples)
- Learns what "normal" behavior looks like
- No hardcoded thresholds needed
- Can detect subtle anomalies that threshold alerts miss

### 3. Web Dashboard (Django)
- Real-time view of all metrics
- Auto-refreshes every 10 seconds
- Color-coded alerts:
  - **Red:** Threshold violations (HIGH CPU, PORT DOWN)
  - **Yellow:** ML-detected anomalies (pattern-based)

---

## Why ML is Better Than Thresholds

**Threshold Approach (Old):**
if CPU > 80%:
alert()
Problem: 80% might be normal for one switch, abnormal for another.

**ML Approach (My System):**

Model learns: Switch A normally runs 75-85% CPU
New reading: 90% → ANOMALY (unusual for this switch)

Adaptive, context-aware, fewer false alarms.

---

## Current Status

✅ Database integration working  
✅ ML model trained and detecting anomalies  
✅ Dashboard functional with auto-refresh  
✅ 341 training samples collected  

🔄 **Next Steps:**
1. Connect to real switches via pysnmp (need switch IP + SNMP community string)
2. Add data visualization (charts showing trends)
3. Deploy to test server for remote access

---

## What I Need

1. **Test switch access:**
   - IP address of one switch
   - SNMP community string (read-only)
   - OIDs for the metrics we're monitoring

2. **Historical data (optional):**
   - If you can export CSV of past switch metrics, I can train on real patterns

---

## Demo Points

1. Show monitor running in terminal (live data collection)
2. Show database admin (341 entries)
3. Show dashboard with ML anomaly highlighting
4. Explain how Isolation Forest learns patterns
5. Show code structure (clean, modular, professional)

**Time needed for demo:** 10 minutes