# Project Demo Guide — For Mentor Presentation

## What I Built

**AI-Powered Network Switch Monitoring System**

A system that polls 3 virtual network switches every 10 seconds via real SNMP protocol, stores metrics in cloud PostgreSQL, detects anomalies using ML, and displays live updates on a dashboard via WebSocket.

---

## Current Stack

| Component | Technology |
|-----------|-----------|
| Monitor Script | `src/monitor_snmp.py` — pysnmp v7 async |
| Database | PostgreSQL via Supabase |
| ML Model | Isolation Forest (scikit-learn) — 537+ samples |
| Dashboard | Django + Chart.js + WebSocket |
| Real-time | Django Channels + Redis + Daphne |
| API | Django REST Framework — 3 endpoints |
| Alerts | Gmail SMTP + AlertHistory model |
| Containers | Docker — 3 virtual switches |

---

## Demo Flow (10 minutes)

### Terminal — show live monitoring

python src/monitor_snmp.py

> "This polls 3 virtual switches every 10 seconds via real SNMP protocol —
> same protocol used by SolarWinds and enterprise tools."

### Dashboard — localhost:8000
> "New rows appear instantly — no page refresh. That's WebSocket pushing
> data from the monitor script to the browser in real time."

### Per-Switch Detail Page — click any switch name
> "Each switch has its own dedicated page — health %, anomaly count,
> line chart for CPU/temp/memory, bar chart for bandwidth."

### Anomalies Only filter
> "ML-detected anomalies in yellow, threshold alerts in red.
> The model learned each switch's individual baseline."

### Alert History — /alerts/
> "Every ML alert is logged here with email delivery status.
> Full audit trail."

### API — /api/anomalies/
> "REST API exposes all data as JSON — any frontend or external
> system can consume this."

### GitHub — show commit history + PRs
> "Daily commits over 5 weeks, proper feature branch workflow —
> PR for every feature."

---

## Real Switch — How to Connect

Admin panel → Switches → Add Switch:
- **Name:** any descriptive name
- **IP Address:** switch's IP on your network
- **Port:** 161 (standard SNMP)
- **Community String:** switch's read-only community string
- **is_demo:** uncheck (False)

System automatically uses the real switch's community string.
Dashboard shows 🟢 Live Mode when any real switch is active.

---

## Why ML Over Thresholds

| Threshold | ML (Isolation Forest) |
|-----------|----------------------|
| Fixed: CPU > 80% = alert | Learned: 80% is normal for Core Switch |
| Same rule for all switches | Per-switch baseline |
| False alarms on busy switches | Context-aware detection |
| Can't catch subtle patterns | Catches unusual combinations |

---

## Key Technical Answers

**Why Daphne instead of runserver?**
Django's dev server doesn't support WebSocket. Daphne is an ASGI server.

**Why Redis?**
InMemoryChannelLayer only works within one process. Monitor script and
Daphne are separate processes — Redis is the shared message broker.

**Why async/await in monitor script?**
pysnmp v7 is fully async. asyncio.gather() polls all 3 switches
simultaneously instead of sequentially.

**Why sync_to_async?**
Django ORM is synchronous. Needed to call it from inside the async
monitor loop without blocking the event loop.