# Day 01 — First Day at Internship

**Date:** 2026-05-05  
**Location:** Tata Steel IT Department, Angul

## What Happened

Met with mentor. Discussed project idea: AI-powered network switch monitoring system.

Key findings:
- They already have basic network monitoring (without AI)
- AI/ML is new to their team — no existing implementation
- Mentor asked me to research "how to implement AI in network monitoring"
- Will get access to real switches/network setup in 2-3 days
- For now: build prototype independently

## What I Built Today

Created a basic network monitoring script (`src/monitor.py`) that:
- Simulates SNMP data collection (CPU, temperature, bandwidth, port status)
- Detects anomalies using threshold-based logic
- Logs all data to CSV file for analysis
- Runs continuously, polls every 5 seconds

**Tech used:** Python, csv module, random (for simulation)

**Current approach:** Simulated data → later replace with real pysnmp calls when switch access is provided

## Research Done

### GitHub Repos Found:
1. **Acegenesis/System-Data-Analysis---Anomaly-Detection** — Python project analyzing system performance data with anomaly detection
2. **RyojiSeto/nano-monitor** — Lightweight network monitoring tool with ML-based anomaly detection
3. **Ayush75-arch/H2H-BinaryBandits-Network_Log_Translator** — AI-powered network log translator with anomaly detection

### Key Learnings:
- `pysnmp` library is standard for SNMP polling in Python
- scikit-learn has built-in outlier detection methods (novelty detection)
- Basic anomaly detection: threshold-based → upgrade to ML-based (learn patterns from data)
- Real implementation needs: data collection → model training → real-time detection

## Next Steps

**Tomorrow:**
- Add simple Django dashboard to visualize logged data
- Display metrics in table format
- Show anomaly alerts

**Day 3:**
- Improve UI
- Add real-time updates
- Prepare demo for mentor

**After mentor provides switch access:**
- Replace simulated data with real pysnmp calls
- Collect baseline data for ML training
- Implement scikit-learn anomaly detection model

---

*Built working prototype on Day 1. Ready to scale once real infrastructure access is granted.*