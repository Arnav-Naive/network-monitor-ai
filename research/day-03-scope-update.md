# Day 03 — Project Scope Clarified

**Date:** 2026-05-07

## Key Discussion with Mentor

Mentor clarified actual project requirements:

**Their existing system:**
- SolarWinds NPM for network monitoring
- Already has predictive alerts
- No sample CSV data available — data accessed via CLI + SNMP

**My task:**
1. Build SolarWinds-style monitoring system from scratch (simplified version)
2. Add innovation layer — AI-based anomaly detection
3. Find additional improvements (security monitoring, earlier failure prediction)

**Timeline:** 3 months is sufficient

## Updated Metrics to Monitor

Based on mentor input:
- CPU usage
- Memory usage  
- Temperature
- Interface bandwidth
- Interface status (UP/DOWN)
- CRC errors (data corruption count)
- Reliability score (255/255 = perfect)
- TX rate (transmit speed)
- RX rate (receive speed)

## Next Steps

**Week 1-2:** Build core monitoring with simulated data  
**Week 3-4:** Connect to real switches via pysnmp  
**Week 5-8:** Add ML anomaly detection layer  
**Week 9-12:** Polish + extra innovation + demo prep

## SolarWinds Workflow (My Understanding)

**How it works:**
1. **Discovery:** System finds all network devices (switches, routers)
2. **Polling:** Uses SNMP to query each device every 2-10 minutes
3. **Data Collection:** Stores metrics in database (CPU, bandwidth, etc.)
4. **Threshold Monitoring:** If metric crosses preset limit → alert
5. **Dashboard:** Shows current status of all devices in one view
6. **Alerts:** Email/SMS when problems detected

**Key features:**
- Network topology map (visual diagram of connections)
- Performance graphs (CPU/bandwidth over time)
- Custom alerting rules
- Historical data for analysis

**What they DON'T have (my opportunity):**
- AI-based pattern learning (they use fixed thresholds)
- Predictive failure detection (alert before crash happens)
- Automatic baseline adjustment (thresholds stay static)

My project will add the AI layer on top of this basic workflow.