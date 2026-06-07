<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&weight=700&size=28&pause=1000&color=00D4AA&center=true&vCenter=true&width=600&lines=Network+Monitor+AI;AI-Powered+Switch+Monitoring;Built+at+Tata+Steel+Internship" alt="Typing SVG" />

<br/>

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Django](https://img.shields.io/badge/Django-5.0-092E20?style=for-the-badge&logo=django&logoColor=white)](https://djangoproject.com)
[![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Supabase-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://supabase.com)
[![Redis](https://img.shields.io/badge/Redis-Channel_Layer-DC382D?style=for-the-badge&logo=redis&logoColor=white)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-IsolationForest-F7931E?style=for-the-badge&logo=scikitlearn&logoColor=white)](https://scikit-learn.org)

<br/>

> **Polls 3 network switches every 10 seconds via real SNMP · Detects anomalies using unsupervised ML · Streams live updates via WebSocket · No page refresh needed**

<br/>

| 🌐 Django Dashboard | ⚛️ React Dashboard | 💻 GitHub |
|:---:|:---:|:---:|
| [network-monitor-ai.onrender.com](https://network-monitor-ai.onrender.com) | [network-monitor-ai.vercel.app](https://network-monitor-ai.vercel.app) | [Arnav-Naive/network-monitor-ai](https://github.com/Arnav-Naive/network-monitor-ai) |

<br/>

</div>

---

## 🧠 The Core Idea

Traditional monitoring tools use **fixed thresholds** — if CPU > 80%, alert. But 80% CPU might be perfectly normal for a Core Switch that's always under heavy load, while the same 80% on a lightly loaded Access Switch signals a real problem.

This system uses **Isolation Forest** (unsupervised ML) to learn each switch's **individual baseline**. No labelled anomaly data needed. No manual threshold tuning per switch.

```
Fixed Threshold Approach          ML Approach (This Project)
──────────────────────────        ──────────────────────────────────
CPU > 80% → ALERT always          "Is THIS unusual for THIS switch?"

Core Switch CPU 80%   → 🚨 ALERT  Core Switch CPU 80%   → ✅ Normal
Access Switch CPU 80% → 🚨 ALERT  Access Switch CPU 80% → ⚠️ ANOMALY
```

---

## ✨ Features

| Feature | Details |
|:--------|:--------|
| **Real SNMP Polling** | `pysnmp` v7 async — same protocol used by SolarWinds & enterprise tools |
| **3 Virtual Switches** | Docker containers with different CPU/temp profiles (Core, Access, Distribution) |
| **ML Anomaly Detection** | Isolation Forest trained on 537 samples, learns per-switch baseline |
| **Dual Detection** | ML model + threshold rules run simultaneously as independent layers |
| **WebSocket Live Feed** | Django Channels + Redis pushes rows to browser instantly — no page reload |
| **Two Dashboards** | Django (server-side) + React (Vite + Tailwind + Recharts) |
| **Cloud PostgreSQL** | Supabase-hosted DB — no local setup required |
| **REST API** | 3 DRF endpoints consumable by any frontend or external system |
| **Email Alerts** | Gmail SMTP on ML detections with 30-minute cooldown |
| **Alert History** | Every alert logged with email delivery status — full audit trail |
| **Per-Switch Detail** | Dedicated page per switch: health %, anomaly count, individual charts |
| **Dashboard Filters** | Time range × Anomaly type × Switch — in both Django and React |
| **Real Switch Ready** | Add any real switch IP + SNMP community string via admin — no code changes |
| **CSV Export** | One-click export of all collected metrics |
| **Deployed** | Django on Render · React on Vercel · DB on Supabase |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      🐳 DOCKER CONTAINERS                       │
│  ┌───────────────┐  ┌────────────────┐  ┌──────────────────┐   │
│  │ Core Switch   │  │ Access Switch  │  │ Dist. Switch     │   │
│  │ CPU: 60–90%   │  │ CPU: 20–50%    │  │ CPU: 40–75%      │   │
│  │ Port: 1161    │  │ Port: 1162     │  │ Port: 1163       │   │
│  └──────┬────────┘  └───────┬────────┘  └────────┬─────────┘   │
└─────────┼───────────────────┼────────────────────┼─────────────┘
          │          SNMP / UDP (Real Protocol)     │
          └─────────────────┬───────────────────────┘
                            ▼
            ┌───────────────────────────────┐
            │      src/monitor_snmp.py      │  ← runs every 10 seconds
            │                               │
            │  asyncio.gather()             │  ← polls all 3 simultaneously
            │  detect_anomaly()             │  ← ML model + thresholds
            │  save_metric()                │  ← DB write + email + WS push
            └───────────┬───────────────────┘
                        │
           ┌────────────┴────────────┐
           ▼                         ▼
  ┌─────────────────┐     ┌──────────────────────┐
  │  ML Detection   │     │  Threshold Detection  │
  │ IsolationForest │     │  CPU > 85%            │
  │ per-switch      │     │  Temp > 78°C          │
  │ baseline        │     │  (backup layer)       │
  └────────┬────────┘     └────────┬─────────────┘
           └──────────┬────────────┘
                      ▼
         ┌────────────────────────────┐
         │        save_metric()       │
         │                            │
         │  1. → Supabase PostgreSQL  │
         │  2. → Email (if ML hit)    │
         │  3. → Redis channel_layer  │
         └──────┬─────────────────────┘
                │
    ┌───────────┴──────────┐
    ▼                       ▼
┌──────────────┐    ┌──────────────────┐
│  PostgreSQL  │    │  Redis           │
│  (Supabase)  │    │  Channel Layer   │
│  Cloud DB    │    │  Message Broker  │
└──────┬───────┘    └────────┬─────────┘
       │                     │
       └────────┬────────────┘
                ▼
    ┌───────────────────────┐
    │   Daphne ASGI Server  │  ← NOT manage.py runserver
    │   localhost:8000      │    (runserver has no WebSocket)
    └──────────┬────────────┘
               │
    ┌──────────┴──────────┐
    ▼                      ▼
┌─────────────┐   ┌──────────────────────┐
│  HTTP Views │   │  WebSocket           │
│  /          │   │  /ws/metrics/        │
│  /api/...   │   │  MetricsConsumer     │
│  /alerts/   │   │  → browser instantly │
│  /export/   │   └──────────────────────┘
└─────────────┘
       │
  ┌────┴──────────────────────────────────────────┐
  │                 Deployed Versions             │
  │  Django  → network-monitor-ai.onrender.com    │
  │  React   → network-monitor-ai.vercel.app      │
  └───────────────────────────────────────────────┘
```

---

## 🔄 Live Update Flow (WebSocket Chain)

```mermaid
sequenceDiagram
    participant Switch as 🐳 Docker Switch
    participant Monitor as monitor_snmp.py
    participant ML as IsolationForest
    participant DB as PostgreSQL (Supabase)
    participant Redis as Redis
    participant Daphne as Daphne (ASGI)
    participant Browser as Browser

    loop Every 10 seconds
        Monitor->>Switch: SNMP GET (CPU, Mem, Temp, BW)
        Switch-->>Monitor: integer values via UDP
        Monitor->>ML: predict([cpu, mem, temp, bw, crc, tx, rx])
        ML-->>Monitor: +1 normal / -1 anomaly
        Monitor->>DB: SwitchMetric.objects.create()
        Monitor->>Redis: channel_layer.group_send('metrics', data)
        Redis->>Daphne: message delivered to group
        Daphne->>Browser: ws.onmessage(data)
        Note over Browser: Row appears instantly — no reload
    end
```

---

## 🧠 ML Pipeline

```mermaid
flowchart LR
    A[537 readings\n7 features each] --> B[numpy array\n537 × 7]
    B --> C[IsolationForest\ncontamination=0.1\nrandom_state=42]
    C --> D[anomaly_model.pkl]
    D --> E[Loaded on startup\nmonitor_snmp.py]
    E --> F{predict\nnew reading}
    F -->|score = +1| G[✅ Normal]
    F -->|score = -1| H[⚠️ ML DETECTED ANOMALY]
```

**Features used:** `cpu_usage`, `memory_usage`, `temperature`, `bandwidth`, `crc_errors`, `tx_rate`, `rx_rate`

**Why Isolation Forest?**
- Unsupervised — no labelled anomaly data required
- Learns per-switch baseline automatically from historical data
- Fast inference (linear time) — works within 10-second polling loop
- High-dimensional friendly — handles all 7 features simultaneously

---

## 🗄️ Database Schema

```mermaid
erDiagram
    Switch {
        int id PK
        string name
        string ip_address
        int port
        string location
        string community_string
        bool is_demo
        bool is_active
    }
    SwitchMetric {
        int id PK
        int switch_id FK
        datetime timestamp
        int cpu_usage
        int memory_usage
        int temperature
        int bandwidth
        int tx_rate
        int rx_rate
        string anomalies
    }
    AlertHistory {
        int id PK
        int switch_id FK
        datetime timestamp
        string anomaly_type
        int cpu_usage
        int temperature
        bool email_sent
    }

    Switch ||--o{ SwitchMetric : "has many"
    Switch ||--o{ AlertHistory : "has many"
```

---

## 🛠️ Tech Stack

| Layer | Technology | Why |
|:------|:-----------|:----|
| Language | Python 3.11 | Core application |
| Web Framework | Django 5.0 | Dashboard + REST API + Admin |
| React Frontend | React 19 + Vite + Tailwind v4 + Recharts | Modern client-side UI |
| ASGI Server | Daphne 4.0 | WebSocket support (`runserver` doesn't support WS) |
| Real-time | Django Channels + Redis | Live dashboard — cross-process message broker |
| ML | scikit-learn — IsolationForest | Unsupervised anomaly detection |
| Database | PostgreSQL via Supabase | Cloud DB, production-ready |
| API | Django REST Framework | JSON endpoints consumed by React |
| Network Protocol | pysnmp v7 (async) | Real SNMP polling — same as enterprise tools |
| Virtual Switches | Docker + Net-SNMP | 3 containers with different CPU/temp profiles |
| Charts (Django) | Chart.js | Line + bar charts |
| Charts (React) | Recharts | Modern declarative charts |
| Email | Django SMTP — Gmail | Anomaly alerts with cooldown |
| Async | asyncio + asgiref | Concurrent polling + sync/async bridge |
| Deployment (BE) | Render | Django + static files |
| Deployment (FE) | Vercel | React static build |
| CORS | django-cors-headers | Allows React (port 5173) to call Django (port 8000) |
| Version Control | Git + GitHub (PRs) | 11 PRs, feature branch workflow |

---

## 📁 Project Structure

```
network-monitor-ai/
│
├── src/
│   ├── monitor_snmp.py          ← HEART — polls switches, runs ML, saves data, pushes WS
│   ├── train_model.py           ← Run once to train IsolationForest → anomaly_model.pkl
│   └── migrate_alerts.py        ← One-time script to backfill AlertHistory from old data
│
├── monitor/                     ← Django App
│   ├── models.py                ← Switch · SwitchMetric · AlertHistory
│   ├── views.py                 ← Dashboard + per-switch pages + 3 APIs + CSV + alerts page
│   ├── serializers.py           ← DRF: model objects → JSON for React consumption
│   ├── consumers.py             ← WebSocket handler (connect / disconnect / push)
│   ├── routing.py               ← Maps ws://localhost:8000/ws/metrics/ → MetricsConsumer
│   ├── alerts.py                ← Email alert logic with 30-minute cooldown
│   ├── admin.py                 ← Registers all 3 models in Django admin
│   └── templates/monitor/
│       ├── dashboard.html       ← Main dashboard (Chart.js + filters + live table)
│       ├── switch_detail.html   ← Per-switch page (health %, charts, history)
│       └── alert_history.html  ← Alert audit trail with email status
│
├── monitor/static/monitor/
│   ├── css/dashboard.css        ← All dashboard styling
│   └── js/dashboard.js          ← WebSocket client + Chart.js initialisation
│
├── dashboard/                   ← Django Project Config
│   ├── settings.py              ← DB · Redis · Email · CORS · CSRF config
│   ├── urls.py                  ← All URL routes
│   ├── asgi.py                  ← HTTP + WebSocket protocol router
│   └── wsgi.py                  ← WSGI fallback for production
│
├── frontend/                    ← React App (Vite)
│   ├── src/
│   │   ├── App.jsx              ← Main component · filters · WebSocket · metrics table
│   │   ├── SummaryCards.jsx     ← Total · Anomalies · System Health %
│   │   ├── MetricsLineChart.jsx ← CPU / Temp / Memory line chart (Recharts)
│   │   ├── BandwidthChart.jsx   ← Per-switch bandwidth bar chart (Recharts)
│   │   └── LiveFeed.jsx         ← WebSocket live rows with pulsing indicator
│   ├── .env.production          ← VITE_API_URL → Render URL for Vercel build
│   └── vite.config.js           ← Proxy /api → localhost:8000 in dev
│
├── docker-snmp/                 ← Virtual Switch Setup
│   ├── Dockerfile               ← Ubuntu 22.04 + snmpd recipe
│   ├── snmpd.conf               ← SNMP agent config (custom OID mappings)
│   ├── docker-compose.yml       ← 3 switches with different env var profiles
│   └── scripts/
│       ├── cpu.sh               ← Random CPU within switch range (/dev/urandom)
│       ├── memory.sh            ← Random memory
│       ├── temperature.sh       ← Random temp within switch range
│       └── bandwidth.sh         ← Random bandwidth
│
├── docs/                        ← Architecture diagrams (Mermaid)
│   ├── Diagram 1 — Full System Architecture.md
│   ├── Diagram 2 — WebSocket Live Update Flow.md
│   ├── Diagram 3 — ML Anomaly Detection Pipeline.md
│   ├── Diagram 4 — Database Schema.md
│   ├── mentor-demo-guide.md
│   ├── ml-workflow.md
│   └── system-architecture.md
│
├── research/                    ← Daily learning notes (Days 0–27)
│
├── .env                         ← DATABASE_URL · EMAIL · SECRET_KEY  ← never committed
├── .gitignore
├── requirements.txt
├── Procfile                     ← Render: migrate + gunicorn
├── docker-compose.yml           ← Root compose (Redis + 3 switches)
└── manage.py
```

---

## ⚡ Quick Start

### Prerequisites
- Python 3.11+
- Docker Desktop
- Node.js 18+ (React frontend only)

### 1. Clone and install

```bash
git clone https://github.com/Arnav-Naive/network-monitor-ai.git
cd network-monitor-ai
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

### 2. Create `.env`

```env
DATABASE_URL=postgresql://postgres:password@db.xxxx.supabase.co:5432/postgres
EMAIL_USER=your@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
SECRET_KEY=your-django-secret-key
```

> **Supabase tip:** Use the **Session Pooler URL** (not Direct connection) — it's IPv4 compatible and avoids DNS issues on mobile hotspots.

### 3. Run migrations

```bash
python manage.py migrate
```

### 4. Start Docker containers

```bash
# 3 virtual switches
docker compose -f docker-snmp/docker-compose.yml up -d

# Redis (WebSocket channel layer)
docker run -d -p 6379:6379 --name redis redis:alpine
```

### 5. Add switches to database

```bash
python manage.py shell
```
```python
from monitor.models import Switch
Switch.objects.create(name="Core Switch 01",         ip_address="127.0.0.1", port=1161, location="Server Room A")
Switch.objects.create(name="Access Switch 02",       ip_address="127.0.0.1", port=1162, location="Floor 2")
Switch.objects.create(name="Distribution Switch 03", ip_address="127.0.0.1", port=1163, location="Server Room B")
exit()
```

### 6. Collect data and train ML model

```bash
# Terminal — let run 15+ minutes to collect 150+ samples
python src/monitor_snmp.py

# Then in another terminal
python src/train_model.py
# Output: Training on 537 data points... ✓ Model saved to anomaly_model.pkl
```

---

## ▶️ Running the System

Every session requires **3 terminals running simultaneously:**

```bash
# Terminal 1 — Docker containers
docker start switch-core-01 switch-access-02 switch-dist-03
docker start redis

# Terminal 2 — Data collector (keep running)
python src/monitor_snmp.py

# Terminal 3 — Web server (ASGI — supports WebSocket)
daphne -p 8000 dashboard.asgi:application

# Terminal 4 — React dev server (optional)
cd frontend && npm run dev
```

| URL | What |
|:----|:-----|
| `http://localhost:8000` | Django dashboard (full-featured) |
| `http://localhost:5173` | React dashboard (modern UI) |
| `http://localhost:8000/admin/` | Django admin panel |

> ⚠️ **Use `daphne`, not `manage.py runserver`** — Django's dev server doesn't support WebSocket.

---

## 🔌 API Reference

All endpoints return JSON. Browsable via Django REST Framework UI.

```
GET  /api/switches/    → All 3 switches with connection details
GET  /api/metrics/     → Last 100 metric readings
GET  /api/anomalies/   → Only anomaly records
GET  /export/          → Download all data as CSV
```

**Example — `/api/switches/`:**
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

**Example — `/api/anomalies/`:**
```json
{
  "count": 722,
  "results": [
    {
      "id": 4821,
      "switch_name": "Distribution Switch 03",
      "timestamp": "2026-06-06T09:23:18Z",
      "cpu_usage": 67,
      "temperature": 69,
      "anomalies": "ML DETECTED ANOMALY"
    }
  ]
}
```

---

## 📊 ML Model Details

| Property | Value |
|:---------|:------|
| Algorithm | `IsolationForest` (scikit-learn) |
| Training samples | 537 readings across 3 switches |
| Features | `cpu_usage`, `memory_usage`, `temperature`, `bandwidth`, `crc_errors`, `tx_rate`, `rx_rate` |
| Contamination | `0.1` — expects ~10% anomalies in training data |
| Detection type | Unsupervised — no labelled anomaly examples needed |
| Output | `+1` = normal, `-1` = anomaly |
| Saved as | `anomaly_model.pkl` (excluded from git) |

---

## 🔑 Key Design Decisions

**`asyncio.gather()` for parallel polling**
```python
tasks = [poll_switch(switch) for switch in switches]
results = await asyncio.gather(*tasks)
```
Sequential: 3 switches × 2s timeout = 6s per cycle. With `gather`: always ≤2s regardless of switch count.

**Redis over `InMemoryChannelLayer`**

`InMemoryChannelLayer` stores messages in RAM of one process only. `monitor_snmp.py` and `daphne` are separate processes — messages would silently vanish. Redis is the shared external broker both can reach.

**`@sync_to_async` for Django ORM**

pysnmp v7 requires a fully async event loop. Django ORM is synchronous. `@sync_to_async` runs ORM calls in a thread pool — the async monitor loop never blocks.

**`wss://` auto-detection for deployment**
```javascript
const ws = new WebSocket(
    `${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws/metrics/`
);
```
`ws://` is blocked on HTTPS pages (mixed content). This detects the protocol at runtime — works locally and deployed.

---

## 🌐 Connecting a Real Switch

No code changes needed. The architecture handles real and virtual switches identically.

1. Go to `localhost:8000/admin/` → **Switches → Add Switch**
2. Fill in:

| Field | Value |
|:------|:------|
| Name | Any descriptive name |
| IP Address | Switch's actual IP (e.g. `192.168.1.1`) |
| Port | `161` (standard SNMP) |
| Community String | Switch's read-only community string |
| is_demo | ☐ uncheck |

3. Dashboard header automatically shows **🟢 Live Mode** when a real switch is active

---

## 🚧 Known Limitations

| Limitation | Reason | Workaround |
|:-----------|:-------|:-----------|
| WebSocket unavailable on deployed version | Render free tier doesn't support persistent WS | 10-second auto-refresh fallback |
| 50-second cold start on Render | Free tier spins down after inactivity | First request takes ~50s |
| `anomaly_model.pkl` not in git | Binary file, excluded via `.gitignore` | Run `python src/train_model.py` after setup |
| React shows last 100 readings only | DRF API default pagination | Filters applied client-side on fetched data |

---

## 📈 Project Numbers

| Metric | Value |
|:-------|:------|
| Development Days | 27 working days |
| GitHub PRs Merged | 11 |
| ML Training Samples | 537 readings |
| ML Features | 7 per reading |
| Switches Monitored | 3 virtual (real switch ready) |
| Polling Interval | Every 10 seconds |
| Database Records | 7,000+ metrics · 1,289 alerts |
| REST API Endpoints | 3 |
| Emails Sent | 4 (30-minute cooldown) |

---

## 🗓️ Development Log

| Days | Feature |
|:-----|:--------|
| 1–5 | SNMP basics, pysnmp v7 async rewrite, Docker Net-SNMP containers |
| 6–8 | Django setup, models, basic dashboard with Chart.js |
| 9–11 | IsolationForest ML model, dual detection (ML + thresholds) |
| 12 | Multi-switch support, Docker Compose, asyncio.gather parallelism |
| 13 | PostgreSQL via Supabase, Django REST Framework — 3 endpoints |
| 14–15 | WebSocket with Django Channels, Redis channel layer, Daphne |
| 16–19 | Real switch support, per-switch detail pages, alert history, bar chart |
| 20–25 | React + Vite + Tailwind + Recharts, Render + Vercel deployment |
| 26–27 | React filters (time × anomaly × switch), final polish |

Full daily notes in [`research/`](./research/) folder.

---

## 🐛 Hardest Bugs Fixed

| Bug | Root Cause | Fix |
|:----|:-----------|:----|
| WebSocket connected, zero messages | `InMemoryChannelLayer` = single-process only | Replaced with Redis channel layer |
| `$RANDOM` returning same value in Docker | `$RANDOM` is bash-only, containers use `/bin/sh` | Switched to `/dev/urandom` |
| Supabase DNS failure on hotspot | Direct connection uses IPv6, hotspot is IPv4 | Session Pooler URL |
| `ws://` blocked on deployed HTTPS | Mixed content security policy | Auto-detect `wss://` on HTTPS |
| `.vite/` cache committed (51,000+ files) | Missing `.gitignore` entry | `git rm -r --cached frontend/.vite/` |
| Django ORM crash in async loop | ORM is synchronous, pysnmp v7 requires async | `@sync_to_async` decorator |

---

## 🤝 Git Workflow

Feature branch → PR → Review → Merge to main. No direct pushes to main.

```
git checkout -b feature/your-feature
# write code
git add . && git commit -m "feat: description"
git push origin feature/your-feature
# open PR on GitHub → merge → git checkout main && git pull
```

All 11 PRs visible at [github.com/Arnav-Naive/network-monitor-ai/pulls](https://github.com/Arnav-Naive/network-monitor-ai/pulls?q=is%3Apr+is%3Aclosed)

---

## 📦 Requirements

```
Django>=5.0              scikit-learn>=1.4        channels>=4.0
numpy>=1.24              psycopg2-binary>=2.9      channels-redis>=4.0
pysnmp>=7.0              dj-database-url>=2.0      daphne>=4.0
asgiref>=3.7             djangorestframework>=3.14  redis>=4.0
python-dotenv>=1.0       whitenoise>=6.6            gunicorn>=21.0
                         django-cors-headers>=4.3
```

---

<div align="center">

Built with Python · Django · scikit-learn · Docker · Redis · PostgreSQL · React

**Tata Steel Prashikshan Internship 2026 · Solo Project · 27 Days**

</div>