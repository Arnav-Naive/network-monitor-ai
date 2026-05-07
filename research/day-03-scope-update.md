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