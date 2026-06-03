<div align="center">

# 🔧 Network Monitor AI

### AI-Powered Network Switch Monitoring System

[![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-green?style=flat-square&logo=django)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-blue?style=flat-square&logo=postgresql)](https://supabase.com)
[![Redis](https://img.shields.io/badge/Redis-Channel_Layer-red?style=flat-square&logo=redis)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-blue?style=flat-square&logo=docker)](https://docker.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-IsolationForest-orange?style=flat-square&logo=scikitlearn)](https://scikit-learn.org)

*Built during Tata Steel Internship — Week 2 to Week 6*

</div>

---

## What Is This?

A production-grade network switch monitoring system that polls 3 virtual switches every 10 seconds via real **SNMP protocol**, stores metrics in **cloud PostgreSQL**, detects anomalies using **unsupervised machine learning**, and streams live updates to a dashboard via **WebSocket** — no page refresh needed.

Think of it as a lightweight, open-source alternative to SolarWinds — built from scratch in Python.

> **"The ML model learns each switch's individual baseline. Core Switch normally runs at 70–90% CPU — that's normal for it. Access Switch at 70% is unusual — the model flags that, even though 70% isn't globally high. Fixed thresholds can't do this."**

---

## Features

- **Real SNMP Polling** — uses `pysnmp` v7 async API to query switches over UDP, same protocol as enterprise tools
- **3 Virtual Switches** — Docker containers with different CPU/temp profiles simulating Core, Access, and Distribution switches
- **Isolation Forest ML** — unsupervised anomaly detection trained on 537 samples, learns per-switch baselines
- **Dual Detection** — ML model + threshold rules run simultaneously as backup
- **WebSocket Live Updates** — Django Channels + Redis pushes new rows to dashboard instantly
- **Cloud PostgreSQL** — Supabase-hosted database, no local DB required
- **REST API** — 3 endpoints (metrics, switches, anomalies) with Django REST Framework
- **Email Alerts** — Gmail SMTP alerts on ML detections with 30-minute cooldown
- **CSV Export** — one-click export of all collected data
- **Dashboard Filters** — filter by time range (1h/24h/7d/all), anomaly type, and individual switch
- **Admin Panel** — Django admin at `/admin/` for direct DB access

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Language | Python 3.11 | Core application |
| Web Framework | Django 5.0 | Dashboard + API |
| ASGI Server | Daphne 4.0 | WebSocket support |
| Real-time | Django Channels + Redis | Live dashboard updates |
| ML | scikit-learn (IsolationForest) | Anomaly detection |
| Database | PostgreSQL via Supabase | Cloud metrics storage |
| ORM | Django ORM + dj-database-url | DB abstraction |
| API | Django REST Framework | JSON endpoints |
| Network Protocol | pysnmp v7 (async) | SNMP polling |
| Virtualisation | Docker + Docker Compose | Virtual switches |
| Charts | Chart.js | Live line charts |
| Email | Django SMTP (Gmail) | Anomaly alerts |
| Async | asyncio + asgiref | Concurrent switch polling |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCKER CONTAINERS                         │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────────────┐ │
│  │ Core Switch  │ │Access Switch │ │Distribution Switch   │ │
│  │ CPU: 60-90%  │ │ CPU: 20-50%  │ │   CPU: 40-75%        │ │
│  │ Port: 1161   │ │ Port: 1162   │ │   Port: 1163         │ │
│  └──────┬───────┘ └──────┬───────┘ └──────────┬───────────┘ │
└─────────┼────────────────┼───────────────────-┼─────────────┘
          │    SNMP/UDP (asyncio.gather — simultaneous)        
          ▼                                                     
┌─────────────────────────┐                                    
│   src/monitor_snmp.py   │  polls every 10 seconds            
│   - poll_switch()       │                                    
│   - detect_anomaly()    │──── IsolationForest ────► anomaly_model.pkl
│   - save_metric()       │                                    
└────────────┬────────────┘                                    
             │                                                 
      ┌──────┴──────┐                                          
      │             │                                          
      ▼             ▼                                          
┌──────────┐   ┌─────────────────────────────────┐            
│ Supabase │   │  Redis (Channel Layer)           │            
│ PostgreSQL│   │  group_send('metrics', data)    │            
│          │   └──────────────┬──────────────────┘            
└──────────┘                  │                                
      │                       ▼                                
      │             ┌──────────────────────┐                   
      └────────────►│  Daphne ASGI Server  │                   
                    │  dashboard.asgi:app  │                   
                    └──────────┬───────────┘                   
                               │                               
                    ┌──────────┴───────────┐                   
                    │                      │                   
                    ▼                      ▼                   
             ┌────────────┐      ┌──────────────────┐          
             │ HTTP Views │      │ WebSocket        │          
             │ /          │      │ /ws/metrics/     │          
             │ /api/...   │      │ MetricsConsumer  │          
             │ /export/   │      └────────┬─────────┘          
             └────────────┘               │                    
                                          ▼                    
                                 ┌─────────────────┐           
                                 │ Browser         │           
                                 │ ws.onmessage()  │           
                                 │ addTableRow()   │           
                                 │ (no reload)     │           
                                 └─────────────────┘           
                                          │                    
                              ┌───────────┴────────┐          
                              │  if ML anomaly:    │          
                              │  send_mail()       │          
                              │  (30 min cooldown) │          
                              └────────────────────┘          
```

---

## Project Structure

```
network-monitor-ai/
│
├── src/
│   ├── monitor_snmp.py       ← main script — polls switches, saves, alerts
│   └── train_model.py        ← trains IsolationForest, saves anomaly_model.pkl
│
├── monitor/                  ← Django app
│   ├── models.py             ← Switch + SwitchMetric database tables
│   ├── views.py              ← dashboard view + 3 API endpoints + CSV export
│   ├── serializers.py        ← DRF model → JSON conversion
│   ├── consumers.py          ← WebSocket handler (connect/disconnect/push)
│   ├── routing.py            ← WebSocket URL: ws/metrics/
│   ├── alerts.py             ← email alert with cooldown logic
│   ├── admin.py              ← Django admin registration
│   └── templates/monitor/
│       └── dashboard.html    ← main dashboard page
│
├── monitor/static/monitor/
│   ├── css/dashboard.css     ← dashboard styling
│   └── js/dashboard.js       ← WebSocket client + Chart.js init
│
├── dashboard/                ← Django project config
│   ├── settings.py           ← DB, Redis, email, static files config
│   ├── urls.py               ← all URL routes
│   ├── asgi.py               ← HTTP + WebSocket protocol routing
│   └── wsgi.py               ← WSGI fallback
│
├── docker-snmp/              ← virtual switch setup
│   ├── Dockerfile            ← Ubuntu + snmpd container recipe
│   ├── snmpd.conf            ← SNMP agent config (custom OIDs)
│   ├── docker-compose.yml    ← 3 switches with different profiles
│   └── scripts/
│       ├── cpu.sh            ← random CPU within switch's range
│       ├── memory.sh
│       ├── temperature.sh
│       └── bandwidth.sh
│
├── research/                 ← daily learning notes (Days 1–15)
├── .env                      ← DATABASE_URL, EMAIL, SECRET_KEY (not in git)
├── requirements.txt
├── Procfile                  ← production deployment command
└── anomaly_model.pkl         ← trained ML model (not in git)
```

---

## Setup

### Prerequisites
- Python 3.11+
- Docker Desktop running
- Git

### 1. Clone and install
```bash
git clone https://github.com/Arnav-Naive/network-monitor-ai.git
cd network-monitor-ai
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Create `.env` file
```env
DATABASE_URL=postgresql://postgres:password@db.xxxx.supabase.co:5432/postgres
EMAIL_USER=your@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
SECRET_KEY=your-django-secret-key
```

### 3. Run migrations
```bash
python manage.py migrate
```

### 4. Start Docker containers
```bash
# Start 3 virtual switches
docker compose -f docker-snmp/docker-compose.yml up -d

# Start Redis for WebSocket channel layer
docker run -d -p 6379:6379 --name redis redis:alpine
```

### 5. Add switches to database
```bash
python manage.py shell
```
```python
from monitor.models import Switch
Switch.objects.create(name="Core Switch 01", ip_address="127.0.0.1", port=1161, location="Server Room A")
Switch.objects.create(name="Access Switch 02", ip_address="127.0.0.1", port=1162, location="Floor 2")
Switch.objects.create(name="Distribution Switch 03", ip_address="127.0.0.1", port=1163, location="Server Room B")
exit()
```

### 6. Collect data and train ML model
```bash
# Terminal 1 — run for 15+ minutes to collect 150+ samples
python src/monitor_snmp.py

# Then train
python src/train_model.py
```

---

## Running the System

Every session requires **3 terminals running simultaneously:**

```bash
# Terminal 1 — start containers (once per session)
docker start switch-core-01 switch-access-02 switch-dist-03
docker start redis

# Terminal 2 — data collector (keep running)
python src/monitor_snmp.py

# Terminal 3 — web server
daphne -p 8000 dashboard.asgi:application
```

Open `http://localhost:8000`

> **Note:** Use `daphne` instead of `manage.py runserver` — Django's dev server does not support WebSocket.

---

## API Endpoints

All endpoints return JSON. Browsable via Django REST Framework UI.

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/switches/` | GET | All 3 switches with connection details |
| `/api/metrics/` | GET | Last 100 metric readings with switch names |
| `/api/metrics/?switch=1` | GET | Filter metrics by switch ID |
| `/api/anomalies/` | GET | Only anomaly records |
| `/export/` | GET | Download all data as CSV |

**Example response — `/api/switches/`:**
```json
{
    "count": 3,
    "results": [
        {
            "id": 1,
            "name": "Core Switch 01",
            "ip_address": "127.0.0.1",
            "port": 1161,
            "location": "Server Room A",
            "is_active": true
        }
    ]
}
```

---

## ML Model Details

| Property | Value |
|----------|-------|
| Algorithm | Isolation Forest (scikit-learn) |
| Training samples | 537 readings across 3 switches |
| Features | cpu_usage, memory_usage, temperature, bandwidth, crc_errors, tx_rate, rx_rate |
| Contamination | 0.1 (expects ~10% anomalies) |
| Detection type | Unsupervised (no labelled anomaly data needed) |
| Output | +1 = normal, -1 = anomaly |
| Saved as | `anomaly_model.pkl` (pickle) |

**Why Isolation Forest over thresholds:**
Fixed thresholds treat every switch the same. Core Switch normally runs at 70–90% CPU — a threshold at 80% would false-alarm constantly. Isolation Forest learns that 80% is normal *for Core Switch* but anomalous *for Access Switch*. Per-switch baselines, zero labelling required.

---

## Dashboard Features

- **Real-time table** — new rows appear via WebSocket push, no page reload
- **Line chart** — CPU, temperature, memory over last 50 readings (Chart.js)
- **Summary cards** — Total Logs, ML Anomalies Detected, System Health %
- **Filters** — Time range (1h / 24h / 7d / all) × Anomaly type (all / anomalies / normal) × Switch
- **Color-coded anomalies** — purple for ML detections, red for threshold alerts
- **CSV export** — all collected data in one click
- **Admin panel** — `/admin/` for direct database management

---

## Requirements

```
Django>=5.0
scikit-learn>=1.4
numpy>=1.24
pysnmp>=7.0
asgiref>=3.7
python-dotenv>=1.0
psycopg2-binary>=2.9
dj-database-url>=2.0
djangorestframework>=3.14
channels>=4.0
channels-redis>=4.0
daphne>=4.0
redis>=4.0
```

---

## Key Design Decisions

**asyncio.gather for parallel polling**
```python
tasks = [poll_switch(switch) for switch in switches]
results = await asyncio.gather(*tasks)
```
Polls all 3 switches simultaneously. Without this, 3 × 2s timeout = 6s per cycle. With gather, worst case is still 2s regardless of switch count.

**Redis over InMemoryChannelLayer**
`InMemoryChannelLayer` only shares state within one process. Since `monitor_snmp.py` and `daphne` are separate processes, Redis is required as the shared message broker.

**sync_to_async for Django ORM**
Django's ORM is synchronous. Wrapping DB writes with `@sync_to_async` lets them run from inside the async monitor loop without blocking the event loop.

---

## Development Log

| Day | Feature |
|-----|---------|
| 1–5 | SNMP basics, pysnmp, Docker setup |
| 6–8 | Django setup, models, basic dashboard |
| 9–11 | ML model, Isolation Forest, anomaly detection |
| 12 | Multi-switch support, Docker Compose |
| 13 | PostgreSQL (Supabase) + REST API |
| 14–15 | WebSocket live updates, Redis, Daphne |

Full daily notes in `research/` folder.

---

<div align="center">

Built with Python · Django · scikit-learn · Docker · Redis · PostgreSQL

</div>

---

## Architecture Diagrams

```mermaid
flowchart TD
    subgraph Docker["🐳 Docker Containers"]
        S1["Core Switch 01\nCPU: 60–90%\nPort: 1161"]
        S2["Access Switch 02\nCPU: 20–50%\nPort: 1162"]
        S3["Distribution Switch 03\nCPU: 40–75%\nPort: 1163"]
    end

    subgraph Monitor["📡 monitor_snmp.py"]
        POLL["asyncio.gather()\npoll all 3 simultaneously"]
        DETECT["detect_anomaly()\nML + Threshold"]
        SAVE["save_metric()\nDB write"]
    end

    subgraph ML["🧠 ML Pipeline"]
        MODEL["IsolationForest\n537 samples\ncontamination=0.1"]
        PKL["anomaly_model.pkl"]
    end

    subgraph Storage["☁️ Supabase PostgreSQL"]
        SW["Switch table\n3 rows"]
        SM["SwitchMetric table\n1 row per reading"]
    end

    subgraph Realtime["⚡ Real-time Layer"]
        REDIS["Redis\nChannel Layer"]
        DAPHNE["Daphne\nASGI Server"]
        WS["WebSocket\n/ws/metrics/"]
    end

    subgraph Frontend["🖥️ Dashboard localhost:8000"]
        CHART["Chart.js\nLine Charts"]
        TABLE["Live Table\nWebSocket rows"]
        API["REST API\n/api/metrics/\n/api/switches/\n/api/anomalies/"]
    end

    EMAIL["📧 Gmail Alert\n30 min cooldown"]

    S1 & S2 & S3 -->|SNMP UDP| POLL
    POLL --> DETECT
    DETECT --> MODEL
    MODEL -->|trained from| PKL
    DETECT --> SAVE
    SAVE --> SM
    SW --> POLL
    SAVE --> REDIS
    REDIS --> DAPHNE
    DAPHNE --> WS
    WS --> TABLE
    SM --> CHART
    SM --> API
    SAVE -->|ML anomaly| EMAIL

    style Docker fill:#1a1a2e,color:#fff
    style Monitor fill:#16213e,color:#fff
    style ML fill:#0f3460,color:#fff
    style Storage fill:#533483,color:#fff
    style Realtime fill:#e94560,color:#fff
    style Frontend fill:#1a1a2e,color:#fff
```

```mermaid
sequenceDiagram
    participant Docker as 🐳 Docker Switch
    participant Monitor as monitor_snmp.py
    participant DB as PostgreSQL
    participant Redis as Redis
    participant Daphne as Daphne
    participant Browser as Browser

    loop Every 10 seconds
        Monitor->>Docker: SNMP GET (cpu, memory, temp, bandwidth)
        Docker-->>Monitor: integer values
        Monitor->>Monitor: detect_anomaly() — ML + thresholds
        Monitor->>DB: SwitchMetric.objects.create()
        DB-->>Monitor: saved metric object
        Monitor->>Redis: channel_layer.group_send('metrics', data)
        Redis->>Daphne: message delivered
        Daphne->>Browser: ws.onmessage(data)
        Browser->>Browser: addTableRow(data)
        Note over Browser: New row appears instantly — no reload
    end
```

> 📁 For detailed flow diagrams — ML pipeline, database schema, and debugging flows —
> see the [`/docs`](./docs/) folder.