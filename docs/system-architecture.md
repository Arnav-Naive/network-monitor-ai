# System Architecture

## Current Stack (Week 5)
3 Docker Containers (virtual switches)
↓ SNMP/UDP (asyncio.gather — simultaneous)
src/monitor_snmp.py (polls every 10 seconds)
↓ saves data
Supabase PostgreSQL (cloud database)
↓ reads data          ↓ pushes instantly
Django Dashboard          Redis (Channel Layer)
localhost:8000               ↓
Daphne ASGI Server
↓
Browser (WebSocket)
↓
if ML anomaly:
Email Alert + AlertHistory

## Data Flow

**Phase 1: Collection**
Monitor script polls 3 switches simultaneously via SNMP GET.
Each switch returns CPU, memory, temperature, bandwidth.

**Phase 2: Detection**
Two methods run simultaneously:
- Isolation Forest ML model (learned each switch's baseline)
- Fixed thresholds (CPU > 85%, temp > 78°C) as backup

**Phase 3: Storage**
SwitchMetric saved to PostgreSQL.
If ML anomaly → AlertHistory record created + email sent.

**Phase 4: Real-time Push**
channel_layer.group_send() → Redis → Daphne → WebSocket → Browser.
New row appears in dashboard instantly, no reload.

**Phase 5: Visualization**
Dashboard: line chart, bandwidth bar chart, filters, summary cards.
Per-switch pages: individual history, health %, anomaly count.

## Database Tables

| Table | Purpose | Rows (approx) |
|-------|---------|---------------|
| Switch | 3 switches with IP, port, community_string | 3 |
| SwitchMetric | Every 10-second reading | 4000+ |
| AlertHistory | ML anomaly alerts with email status | grows over time |