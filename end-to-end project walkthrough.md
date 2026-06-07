# Network Monitor AI — Complete Master Document
### Tata Steel Prashikshan Internship | 6 Weeks | Solo Project

---

## SECTION 1: THE ONE-LINE PITCH

> **"I built an AI-powered network switch monitoring system that replaces fixed threshold alerts with machine learning — the same way SolarWinds works, but smarter."**

---

## SECTION 2: THE PROBLEM

### What companies currently do (Dumb Way):
```
if CPU > 80%:
    send_alert()
```

**Why this fails:**
- Core Switch normally runs at 80% CPU — that's normal for it
- Access Switch at 80% CPU = crisis, but the rule is the same
- Too many false alarms → engineers ignore alerts
- Subtle patterns (unusual combination of metrics) get missed completely

### What I built (Smart Way):
The ML model **learns each switch's individual baseline**.
- Core Switch at 80% CPU → Normal ✅
- Access Switch at 80% CPU → ANOMALY ⚠️
- Same number, different meaning, different switch

---

## SECTION 3: SYSTEM ARCHITECTURE

### Bird's Eye View
```
┌─────────────────────────────────────────────────────────────┐
│                  3 DOCKER CONTAINERS                         │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────────────────┐ │
│  │ Core Switch │  │Access Switch │  │Distribution Switch  │ │
│  │ CPU: 60-90% │  │ CPU: 20-50%  │  │   CPU: 40-75%       │ │
│  │ Port: 1161  │  │ Port: 1162   │  │   Port: 1163        │ │
│  └──────┬──────┘  └──────┬───────┘  └──────────┬──────────┘ │
└─────────┼────────────────┼──────────────────────┼────────────┘
          │         SNMP/UDP (Real Protocol)       │
          └──────────────────┬─────────────────────┘
                             ▼
              ┌──────────────────────────┐
              │    monitor_snmp.py       │
              │  polls every 10 seconds  │
              │  asyncio.gather() →      │
              │  all 3 simultaneously    │
              └────────┬─────────────────┘
                       │
           ┌───────────┴──────────┐
           │                      │
           ▼                      ▼
  ┌────────────────┐    ┌──────────────────────┐
  │  ML Detection  │    │  Threshold Detection  │
  │ IsolationForest│    │  CPU > 85% or         │
  │  (per-switch   │    │  Temp > 78°C          │
  │   baseline)    │    └──────────┬────────────┘
  └───────┬────────┘               │
          └──────────┬─────────────┘
                     ▼
        ┌────────────────────────┐
        │   save_metric()        │
        │   3 things happen:     │
        │   1. Save to Supabase  │
        │   2. Email alert       │
        │   3. WebSocket push    │
        └────────┬───────────────┘
                 │
    ┌────────────┴────────────┐
    │                         │
    ▼                         ▼
┌──────────────┐     ┌──────────────────┐
│  PostgreSQL  │     │  Redis           │
│  (Supabase)  │     │  (Channel Layer) │
│  Cloud DB    │     │  Message Broker  │
└──────┬───────┘     └────────┬─────────┘
       │                      │
       └──────────┬───────────┘
                  ▼
       ┌─────────────────────┐
       │   Daphne ASGI Server│
       │   localhost:8000    │
       └──────────┬──────────┘
                  │
       ┌──────────┴──────────┐
       │                     │
       ▼                     ▼
  ┌──────────┐      ┌─────────────────┐
  │HTTP Views│      │WebSocket        │
  │Dashboard │      │/ws/metrics/     │
  │API       │      │Browser updates  │
  └──────────┘      │INSTANTLY        │
                    └─────────────────┘
                    
Also runs on:
React (Vite) → localhost:5173
Deployed Django → network-monitor-ai.onrender.com
Deployed React → network-monitor-ai.vercel.app
```

---

## SECTION 4: TECH STACK TABLE

| Layer | Technology | Why Used |
|-------|-----------|----------|
| Language | Python 3.11 | Core application |
| Web Framework | Django 5.0 | Dashboard + REST API |
| React Frontend | React + Vite + Tailwind v4 + Recharts | Modern UI, separate from backend |
| ASGI Server | Daphne 4.0 | WebSocket support (runserver doesn't support WS) |
| Real-Time | Django Channels + Redis | Live dashboard without page refresh |
| ML | scikit-learn (IsolationForest) | Unsupervised anomaly detection |
| Database | PostgreSQL via Supabase | Cloud database, production-ready |
| API | Django REST Framework | JSON endpoints for React/mobile |
| Network Protocol | pysnmp v7 (async) | Real SNMP polling — same as SolarWinds |
| Virtual Switches | Docker + Net-SNMP | 3 containers simulating real switches |
| Charts (Django) | Chart.js | Line + bar charts |
| Charts (React) | Recharts | Modern Recharts library |
| Email | Django SMTP (Gmail) | Anomaly email alerts |
| Async | asyncio + asgiref | Concurrent switch polling |
| Deployment (BE) | Render | Django backend deployed |
| Deployment (FE) | Vercel | React frontend deployed |
| Version Control | Git + GitHub (PRs) | 10 PRs, feature branch workflow |

---

## SECTION 5: PROJECT STRUCTURE — EVERY FILE EXPLAINED

```
network-monitor-ai/
│
├── src/                          ← Python scripts (not Django)
│   ├── monitor_snmp.py           ← HEART OF PROJECT — runs 24/7
│   ├── train_model.py            ← Run once to train ML model
│   └── migrate_alerts.py        ← One-time script to backfill alert history
│
├── monitor/                      ← Django App
│   ├── models.py                 ← 3 database tables: Switch, SwitchMetric, AlertHistory
│   ├── views.py                  ← All logic: dashboard + 3 APIs + CSV + alerts
│   ├── serializers.py            ← Converts DB objects → JSON for React
│   ├── consumers.py              ← WebSocket handler (connect/disconnect/push)
│   ├── routing.py                ← Maps ws://localhost:8000/ws/metrics/ to consumer
│   ├── alerts.py                 ← Email alert with 30-min cooldown logic
│   ├── admin.py                  ← Registers Switch, SwitchMetric, AlertHistory in admin
│   └── templates/monitor/
│       ├── dashboard.html        ← Main Django dashboard page
│       ├── switch_detail.html    ← Per-switch detail page
│       └── alert_history.html   ← Alert history page
│
├── monitor/static/monitor/
│   ├── css/dashboard.css         ← All dashboard styling
│   └── js/dashboard.js           ← WebSocket client + Chart.js init
│
├── dashboard/                    ← Django Project Config
│   ├── settings.py               ← Database, Redis, email, CORS config
│   ├── urls.py                   ← All URL routes
│   ├── asgi.py                   ← HTTP + WebSocket protocol router
│   └── wsgi.py                   ← WSGI fallback for deployment
│
├── frontend/                     ← React App (separate from Django)
│   ├── src/
│   │   ├── App.jsx               ← Main component, filters, WebSocket
│   │   ├── SummaryCards.jsx      ← Total, Anomalies, Health % cards
│   │   ├── MetricsLineChart.jsx  ← CPU/Temp/Memory line chart
│   │   ├── BandwidthChart.jsx    ← Per-switch bandwidth bar chart
│   │   └── LiveFeed.jsx          ← WebSocket live rows table
│   ├── .env.production           ← Points to Render URL for Vercel build
│   └── vite.config.js            ← Proxy /api → localhost:8000
│
├── docker-snmp/                  ← Virtual Switch Setup
│   ├── Dockerfile                ← Ubuntu + snmpd recipe
│   ├── snmpd.conf                ← SNMP agent config (OIDs)
│   ├── docker-compose.yml        ← 3 switches with different CPU/temp ranges
│   └── scripts/
│       ├── cpu.sh                ← Random CPU within switch range (/dev/urandom)
│       ├── memory.sh             ← Random memory
│       ├── temperature.sh        ← Random temp within switch range
│       └── bandwidth.sh         ← Random bandwidth
│
├── docs/                         ← Architecture diagrams (Mermaid)
│   ├── Diagram 1 — Full System Architecture.md
│   ├── Diagram 2 — WebSocket Live Update Flow.md
│   ├── Diagram 3 — ML Anomaly Detection Pipeline.md
│   ├── Diagram 4 — Database Schema.md
│   ├── mentor-demo-guide.md
│   ├── ml-workflow.md
│   ├── project-walkthrough.md
│   └── system-architecture.md
│
├── research/                     ← Daily learning notes (Days 0–27)
│
├── .env                          ← Secrets: DATABASE_URL, EMAIL, SECRET_KEY
├── .gitignore                    ← Never commits: .env, *.pkl, staticfiles/
├── requirements.txt              ← All Python dependencies
├── Procfile                      ← Render deployment command
├── docker-compose.yml           ← Root compose (includes Redis + 3 switches)
├── manage.py                     ← Django management
└── README.md                     ← Full documentation with live demo links
```

---

## SECTION 6: CODE WALKTHROUGH — FILE BY FILE

### 6.1 The Docker Switches (Where Data Comes From)

**`docker-snmp/scripts/cpu.sh`**
```bash
#!/bin/sh
MIN=${CPU_MIN:-40}
MAX=${CPU_MAX:-90}
RANGE=$((MAX - MIN))
echo $((MIN + $(od -An -N2 -tu2 /dev/urandom) % RANGE))
```
- Generates a random number between MIN and MAX
- Core Switch: 60–90%, Access Switch: 20–50%, Distribution: 40–75%
- `/dev/urandom` = Linux random bytes (works in all shells, unlike `$RANDOM` which is bash-only — this was a bug we fixed)

**`docker-snmp/snmpd.conf`**
```
extend cpu /usr/local/bin/cpu.sh
extend memory /usr/local/bin/memory.sh
```
- Tells SNMP agent: "when someone asks for CPU, run cpu.sh and return the result"

**`docker-snmp/docker-compose.yml`**
```yaml
switch1:
  environment:
    - CPU_MIN=60
    - CPU_MAX=90
```
- Each switch gets different environment variables → different CPU ranges → different baselines → ML learns the difference

---

### 6.2 The Monitor Script (The Heart)

**`src/monitor_snmp.py`** — this runs in a terminal 24/7

**Step 1 — Django setup at the top:**
```python
sys.path.insert(0, ...)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
```
This loads Django so we can use models (database) outside the web server.

**Step 2 — OIDs (addresses for each metric):**
```python
OIDS = {
    'cpu': '1.3.6.1.4.1.8072.1.3.2.3.1.2.3.99.112.117',
    'memory': '1.3.6.1.4.1.8072.1.3.2.3.1.2.6.109.101...',
}
```
OID = Object Identifier. Like a phone number for each metric. You "call" this number and the switch tells you its CPU value.

**Step 3 — `get_snmp_value()` — sends one SNMP GET request:**
```python
async def get_snmp_value(ip, port, oid, community='public'):
    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        snmpEngine,
        CommunityData(community),      # password = "public" (switch default)
        await UdpTransportTarget.create((ip, port), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )
    return int(str(varBind[1]).strip())
```
Sends one UDP packet to the switch, gets back an integer.

**Step 4 — `poll_switch()` — polls all 4 metrics from one switch:**
```python
async def poll_switch(switch):
    cpu       = await get_snmp_value(ip, port, OIDS['cpu'], community)
    memory    = await get_snmp_value(ip, port, OIDS['memory'], community)
    temp      = await get_snmp_value(ip, port, OIDS['temperature'], community)
    bandwidth = await get_snmp_value(ip, port, OIDS['bandwidth'], community)
    return {"cpu_usage": cpu, "memory_usage": memory, ...}
```

**Step 5 — `detect_anomaly()` — two detection methods run simultaneously:**
```python
def detect_anomaly(data):
    # Method 1: ML Model
    features = np.array([[cpu, memory, temp, bandwidth, crc, tx, rx]])
    if ml_model.predict(features)[0] == -1:
        anomalies.append("ML DETECTED ANOMALY")
    
    # Method 2: Fixed Thresholds (backup)
    if data["cpu_usage"] > 85:
        anomalies.append(f"HIGH CPU: {data['cpu_usage']}%")
```

**Step 6 — `save_metric()` — 3 things happen when saving:**
```python
@sync_to_async
def save_metric(switch, data, anomalies):
    metric = SwitchMetric.objects.create(...)  # 1. Save to DB
    
    if 'ML DETECTED' in anomalies:
        send_anomaly_alert(metric, anomalies)   # 2. Send email
    
    channel_layer.group_send('metrics', {...})  # 3. Push to WebSocket
    
    return metric
```
`@sync_to_async` = Django ORM is synchronous, but our loop is async. This decorator bridges them.

**Step 7 — `monitor_loop()` — the main infinite loop:**
```python
async def monitor_loop():
    while True:
        switches = await get_switches()
        
        # KEY: polls all 3 simultaneously, not one by one
        tasks = [poll_switch(s) for s in switches]
        results = await asyncio.gather(*tasks)
        
        for switch, data in zip(switches, results):
            anomalies = detect_anomaly(data)
            await save_metric(switch, data, anomalies)
        
        await asyncio.sleep(10)  # wait 10 seconds, repeat forever
```
`asyncio.gather()` = parallel polling. Without it: 3 switches × 2 second timeout = 6 seconds per cycle. With it: still 2 seconds regardless of switch count.

---

### 6.3 The Database Models

**`monitor/models.py`** — 3 tables:

```python
class Switch(models.Model):
    name             # "Core Switch 01"
    ip_address       # "127.0.0.1"
    port             # 1161
    location         # "Server Room A"
    community_string # "public" (SNMP password — each switch can have different one)
    is_demo          # True = Docker, False = real switch
    is_active        # True/False

class SwitchMetric(models.Model):
    switch           # ForeignKey → which switch
    timestamp        # auto, when it was recorded
    cpu_usage        # integer
    memory_usage     # integer
    temperature      # integer
    bandwidth        # integer
    tx_rate          # integer
    rx_rate          # integer
    anomalies        # text, e.g. "ML DETECTED ANOMALY" or None

class AlertHistory(models.Model):
    switch           # ForeignKey → which switch
    timestamp        # when alert happened
    anomaly_type     # what was detected
    cpu_usage        # at time of alert
    temperature      # at time of alert
    email_sent       # True/False — audit trail
```

Every 10 seconds: 3 new rows in SwitchMetric (one per switch). After a day: thousands of rows.

---

### 6.4 The ML Model

**`src/train_model.py`** — run once to train:

```python
# Pull all data from database
data = SwitchMetric.objects.all().values_list(
    'cpu_usage', 'memory_usage', 'temperature',
    'bandwidth', 'crc_errors', 'tx_rate', 'rx_rate'
)
# Shape: 537 rows × 7 columns

X = np.array(data)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)   # learns what "normal" looks like

pickle.dump(model, f)  # saves to anomaly_model.pkl
```

**How Isolation Forest Works (Simple Version):**
```
Imagine 537 data points in 7-dimensional space.
Normal points → clustered together → hard to isolate
Anomalies → standing alone → easy to isolate with 1-2 cuts

Algorithm:
1. Build random decision trees
2. Count cuts needed to isolate each point
3. Anomaly = isolated in fewer cuts → score close to -1
4. Normal = needs many cuts → score close to +1
```

**contamination=0.1** = "expect roughly 10% of readings to be anomalies"
**random_state=42** = reproducible results every run

---

### 6.5 Email Alerts

**`monitor/alerts.py`:**
```python
COOLDOWN_MINUTES = 30  # prevents spam (change to 1 for demo)

def send_anomaly_alert(metric, anomalies):
    # Skip if sent in last 30 minutes
    if last_alert_time and timezone.now() - last_alert_time < timedelta(minutes=30):
        return False
    
    send_mail(subject, message, from_email, to_email)
    
    # BOTH success and failure get logged
    AlertHistory.objects.create(
        switch=metric.switch,
        anomaly_type=', '.join(anomalies),
        email_sent=True/False  # audit trail
    )
```

Only ML-detected anomalies trigger emails. Threshold alerts (HIGH CPU, HIGH TEMP) do NOT send emails — they're just visual in the dashboard.

---

### 6.6 The Django Dashboard

**`monitor/views.py` → `dashboard_view()`:**
```python
def dashboard_view(request):
    # Read filters from URL
    filter_type = request.GET.get('filter', 'all')   # ?filter=anomalies
    date_range  = request.GET.get('range', '24h')    # ?range=1h
    switch_id   = request.GET.get('switch', 'all')   # ?switch=2
    
    # Apply filters to database query
    logs_qs = SwitchMetric.objects.select_related('switch').all()
    if from_time:
        logs_qs = logs_qs.filter(timestamp__gte=from_time)
    if filter_type == 'anomalies':
        logs_qs = logs_qs.exclude(Q(anomalies__isnull=True) | Q(anomalies='None'))
    
    # Per-switch bandwidth for bar chart
    switch_bandwidth = []
    for s in switches:
        latest = SwitchMetric.objects.filter(switch=s).order_by('-timestamp').first()
        switch_bandwidth.append({'name': s.name, 'bandwidth': latest.bandwidth, ...})
    
    return render(request, 'monitor/dashboard.html', context)
```

**`monitor/templates/monitor/dashboard.html` — structure:**
```
1. Header + Demo/Live Mode indicator
2. Alert History button + Export CSV button
3. Filter bar (Time Range × Anomaly Type × Switch)
4. 3 Summary Cards (Total Logs, ML Anomalies, System Health %)
5. Line chart — CPU/Temp/Memory last 50 readings (Chart.js)
6. Bandwidth bar chart — per-switch comparison (Chart.js)
7. Data table — every metric, color coded
   → Yellow badge = ML DETECTED ANOMALY
   → Red text = threshold alert (HIGH CPU, HIGH TEMP)
   → Switch name = clickable → goes to /switch/1/ detail page
```

---

### 6.7 WebSocket — How Live Updates Work

**The Chain (exactly what happens every 10 seconds):**
```
monitor_snmp.py
    → channel_layer.group_send('metrics', data)
    → Redis (shared message broker between processes)
    → Daphne reads from Redis
    → MetricsConsumer.metrics_update()
    → browser ws.onmessage()
    → addTableRow(data) or setLiveRows() in React
    → new row appears INSTANTLY — no page reload
```

**Why Redis is needed:**
`InMemoryChannelLayer` (the default) only works within ONE process.
`monitor_snmp.py` and `daphne` are TWO separate processes.
Redis is the shared external message bus — both can read/write to it.

Without Redis: messages sent by monitor disappear into void (silent failure, no error).

**`monitor/consumers.py`:**
```python
class MetricsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('metrics', self.channel_name)
        await self.accept()  # browser joins the 'metrics' group
    
    async def metrics_update(self, event):
        # Called when monitor_snmp.py sends to 'metrics' group
        await self.send(text_data=json.dumps(event['data']))
```

**`monitor/static/monitor/js/dashboard.js`:**
```javascript
// HTTPS detection for deployed version
const ws = new WebSocket(
    `${location.protocol === 'https:' ? 'wss' : 'ws'}://${location.host}/ws/metrics/`
);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    addTableRow(data);  // new row appears at top of table
};

ws.onclose = function() {
    // Fallback: if WebSocket not available (Render free tier)
    setTimeout(function(){ location.reload(); }, 10000);
};
```

---

### 6.8 REST API Endpoints

**`monitor/views.py`** — DRF endpoints:

| URL | Returns | Used By |
|-----|---------|---------|
| `/api/switches/` | All 3 switches as JSON | React frontend |
| `/api/metrics/` | Last 100 metrics as JSON | React frontend |
| `/api/anomalies/` | Only anomaly records | React / external systems |

**`monitor/serializers.py`** — converts Django models → JSON:
```python
class SwitchMetricSerializer(serializers.ModelSerializer):
    switch_name = serializers.CharField(source='switch.name', read_only=True)
    class Meta:
        model = SwitchMetric
        fields = ['id', 'switch_name', 'timestamp', 'cpu_usage', ...]
```
Without a serializer, you'd manually build a dict for every field for every object. Serializer does it automatically.

---

### 6.9 The React Frontend

**`frontend/src/App.jsx`** — main component:
```jsx
const [metrics, setMetrics] = useState([])
const [switches, setSwitches] = useState([])
const [filterType, setFilterType] = useState('all')

// Computed filtered data (no API call needed — filters on fetched 100 rows)
const filteredMetrics = metrics.filter(m => {
    if (filterType === 'anomalies' && !m.anomalies) return false
    if (switchFilter !== 'all' && m.switch_name !== switchFilter) return false
    // date range filter...
    return true
})

useEffect(() => {
    fetch('/api/switches/').then(r => r.json()).then(data => setSwitches(data.results))
    fetch('/api/metrics/').then(r => r.json()).then(data => setMetrics(data.results))
    
    const ws = new WebSocket(`ws://localhost:8000/ws/metrics/`)
    ws.onmessage = (event) => {
        const data = JSON.parse(event.data)
        setLiveRows(prev => [data, ...prev].slice(0, 20))
    }
}, [])
```

**Component Tree:**
```
App.jsx
├── Filter Bar (Time Range + Show + Switch buttons)
├── SummaryCards.jsx → Total, Anomalies, Health %
├── Switch Cards (3 cards: name, location, IP)
├── MetricsLineChart.jsx → CPU/Temp/Memory (Recharts)
├── BandwidthChart.jsx → Per-switch bandwidth (Recharts)
├── LiveFeed.jsx → WebSocket live rows (green pulsing dot)
└── Metrics Table → filteredMetrics, color-coded anomalies
```

---

### 6.10 Settings & Config

**`dashboard/settings.py`** — key sections:
```python
# Database — cloud PostgreSQL via connection string
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# Redis for WebSocket cross-process messaging
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {'hosts': [('127.0.0.1', 6379)]}
    }
}

# ASGI (not WSGI) — needed for WebSocket
ASGI_APPLICATION = 'dashboard.asgi.application'

# CORS — allows React (port 5173) to call Django (port 8000)
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "https://network-monitor-ai.vercel.app",
]

# Production — Render deployment
CSRF_TRUSTED_ORIGINS = ['https://network-monitor-ai.onrender.com']
```

**`dashboard/asgi.py`** — routes HTTP vs WebSocket:
```python
application = ProtocolTypeRouter({
    'http': get_asgi_application(),          # normal requests
    'websocket': AuthMiddlewareStack(
        URLRouter(monitor.routing.websocket_urlpatterns)
    ),
})
```

---

## SECTION 7: HOW TO RUN THE PROJECT (Every Session)

**Start these in separate terminals:**

```bash
# Terminal 1 — Start Docker containers
docker start switch-core-01 switch-access-02 switch-dist-03
docker start redis

# Terminal 2 — Start data collection (keep running)
python src/monitor_snmp.py

# Terminal 3 — Start Django server (ASGI, supports WebSocket)
daphne -p 8000 dashboard.asgi:application

# Terminal 4 (optional) — Start React dev server
cd frontend
npm run dev
```

**Then open:**
- `http://localhost:8000` → Django dashboard
- `http://localhost:5173` → React dashboard

**Why Daphne instead of `runserver`?**
Django's `manage.py runserver` = WSGI, doesn't support WebSocket.
Daphne = ASGI server, handles both HTTP and WebSocket connections.

---

## SECTION 8: LIVE DEMO GUIDE (For Mentor/Interview — 10 Minutes)

### Step 1 — Show the Terminal (1 min)
Point to Terminal 2 running `monitor_snmp.py`:
> "This polls 3 virtual switches every 10 seconds via real SNMP protocol — the same protocol used by SolarWinds and enterprise tools. Each switch has different CPU ranges, simulating different types of switches in a network."

### Step 2 — Open Django Dashboard localhost:8000 (2 min)
> "New rows appear in the table automatically — no page refresh. That's WebSocket pushing data from the monitor script to the browser in real time via Redis."

Show filters: Time Range, Show (Anomalies), Switch selector.
> "I can filter by time range, show only anomalies, or focus on one specific switch."

### Step 3 — Click a Switch Name (1 min)
Click "Core Switch 01" in the table → goes to `/switch/1/`
> "Each switch has its own dedicated page with health percentage, anomaly count, and individual charts for that switch."

### Step 4 — Show Anomalies (1 min)
Click "Anomalies Only" filter:
> "ML-detected anomalies appear in yellow. These are patterns the model found unusual based on that switch's baseline — not a fixed threshold. Threshold alerts appear in red as a backup layer."

### Step 5 — Alert History (1 min)
Click "Alert History" button → `/alerts/`
> "Every ML alert is logged here with email delivery status. This creates a full audit trail — you can see when alerts were sent and whether emails succeeded."

### Step 6 — REST API (1 min)
Go to `localhost:8000/api/anomalies/`
> "The system exposes a REST API. Any frontend, mobile app, or external system can consume this data in JSON format."

### Step 7 — React Dashboard (1 min)
Go to `localhost:5173`
> "I also built a modern React frontend consuming the same API. Same data, better UI — with interactive filters, live feed, and Recharts visualizations."

### Step 8 — Deployed URLs (1 min)
Open `https://network-monitor-ai.onrender.com`
> "Django is deployed on Render. React is deployed on Vercel. Both connect to the same Supabase PostgreSQL database."

### Step 9 — GitHub (1 min)
Show `github.com/Arnav-Naive/network-monitor-ai`
> "Daily commits over 6 weeks. Feature branch → Pull Request → Merge workflow. 10 PRs merged."

---

## SECTION 9: ML DEEP DIVE (For Technical Questions)

### Why Isolation Forest?

| Feature | Isolation Forest | Other Algorithms |
|---------|-----------------|------------------|
| Labeled data needed? | ❌ No (unsupervised) | Most need labeled anomalies |
| Training time | Fast (linear) | Can be slow |
| Per-switch baseline | ✅ Yes (learns from data) | Thresholds don't |
| Works with 7 features | ✅ High-dimensional | Some struggle |

### The Training Process:
```
537 samples (7 features each)
    ↓
numpy array: shape 537 × 7
    ↓
IsolationForest.fit(X)
    ↓ builds random decision trees
    ↓ measures isolation path length for each point
    ↓
anomaly_model.pkl (saved to disk)
    ↓
loaded on startup of monitor_snmp.py
    ↓
model.predict([new_reading]) → +1 (normal) or -1 (anomaly)
```

### Why This Is Better:
```
Threshold approach:             ML approach:
CPU > 80% = alert               "Is this unusual FOR THIS SWITCH?"

Core Switch:                    Core Switch:
CPU 80% → ALERT (false alarm!)  CPU 80% → Normal ✅ (it's always high)

Access Switch:                  Access Switch:
CPU 80% → ALERT (correct)       CPU 80% → ANOMALY ⚠️ (it's usually low)
```

---

## SECTION 10: GIT WORKFLOW USED

```
Feature Branch → PR → Merge → Pull
```

**All 10 PRs:**

| PR | Branch | What |
|----|--------|------|
| #1 | feature/root-docker-compose | Root docker-compose.yml |
| #2 | feature/real-switch-support | community_string, is_demo fields |
| #3 | feature/demo-mode-indicator + switch-detail-page | Demo/Live banner, per-switch page |
| #4 | feature/alert-history | AlertHistory model + page |
| #5 | feature/bandwidth-barchart | Bar chart on main dashboard |
| #6 | feature/fix-docs-and-alert-migration | Docs fix, bulk_create migration |
| #7 | feature/react-frontend | Full React + Vite + Tailwind setup |
| #8 | feature/render-deployment | Render deployment config |
| #9 | feature/readme-final | README with live URLs |
| #10 | feature/final-fixes | CSRF, Chart.js CDN, admin fixes |
| #11 | feature/react-filters | React time/anomaly/switch filters |

---

## SECTION 11: WHAT WORKS WHERE

| Feature | Local | Render (Django) | Vercel (React) |
|---------|-------|-----------------|----------------|
| Dashboard with filters | ✅ | ✅ | ✅ |
| ML anomaly badges | ✅ | ✅ | ✅ |
| Per-switch detail pages | ✅ | ✅ | Via Render |
| Alert history | ✅ | ✅ | Via Render |
| REST API | ✅ | ✅ | ✅ |
| CSV export | ✅ | ✅ | Via Render |
| WebSocket live updates | ✅ | ❌ (free tier) | ❌ (Render WS) |
| Auto-refresh fallback | N/A | ✅ | ✅ |
| React live feed | ✅ | N/A | ❌ (WS fallback) |

---

## SECTION 12: KEY TECHNICAL DECISIONS (Why I Built It This Way)

**1. Why asyncio.gather() instead of sequential polling?**
Sequential: 3 switches × 2s timeout = 6s per cycle.
Parallel: asyncio.gather() → all 3 simultaneously → still 2s worst case.

**2. Why Redis over InMemoryChannelLayer?**
InMemoryChannelLayer = RAM of one process only.
monitor_snmp.py and daphne = two separate processes.
Redis = external shared message bus. Both processes can read/write.

**3. Why @sync_to_async?**
Django ORM is synchronous. Our monitor loop is async (pysnmp v7 requires it).
@sync_to_async = bridge: runs ORM code in a separate thread, async wrapper around it.

**4. Why Supabase Session Pooler URL?**
Direct Supabase connection uses IPv6.
Indian mobile hotspots are IPv4 only.
Session Pooler URL → IPv4 compatible.

**5. Why Daphne instead of gunicorn for local?**
gunicorn = WSGI (handles HTTP only, synchronous).
Daphne = ASGI (handles HTTP + WebSocket, asynchronous).
WebSocket requires ASGI.

**6. Why two dashboards (Django + React)?**
Django = server-side rendered, filters via URL params, per-switch detail pages.
React = client-side rendered, modern UI, Recharts, state-based filtering.
Both consume the same PostgreSQL database via DRF API.

---

## SECTION 13: OBSTACLES FACED AND FIXED

| Problem | Root Cause | Fix Applied |
|---------|-----------|-------------|
| snmpsim not working on Windows | Linux-only tool | Switched to Docker + Net-SNMP |
| pysnmp import error | Deprecated package installed | pip uninstall pysnmp-lextudio, install pysnmp==7.1.10 |
| pysnmp v7 API changed completely | v7 = async rewrite | Rewrote all monitor code with async/await |
| Django ORM crash in async | Django ORM is synchronous | @sync_to_async wrapper |
| Docker shell scripts returning same value | $RANDOM doesn't work in /bin/sh | Switched to /dev/urandom |
| WebSocket connected but no messages | InMemoryChannelLayer = single process | Replaced with Redis |
| Static files 404 with Daphne | Daphne doesn't serve static | collectstatic + whitenoise |
| Supabase IPv6 on mobile hotspot | IPv6 vs IPv4 mismatch | Session Pooler URL |
| Railway deployment failed | IPv6 incompatibility | Switched to Render |
| ws:// blocked on HTTPS | Mixed content error | Auto-detect: wss:// on HTTPS |
| .vite/ cache committed (51k files) | Missing from .gitignore | git rm -r --cached + .gitignore |

---

## SECTION 14: DATABASE SCHEMA

```
Switch Table (3 rows)
┌────┬──────────────────────┬───────────────┬──────┬───────────────┬─────────────────┬─────────┐
│ id │ name                 │ ip_address    │ port │ community_str │ is_demo         │is_active│
├────┼──────────────────────┼───────────────┼──────┼───────────────┼─────────────────┼─────────┤
│ 1  │ Core Switch 01       │ 127.0.0.1     │ 1161 │ public        │ True            │ True    │
│ 2  │ Access Switch 02     │ 127.0.0.1     │ 1162 │ public        │ True            │ True    │
│ 3  │ Distribution Sw 03   │ 127.0.0.1     │ 1163 │ public        │ True            │ True    │
└────┴──────────────────────┴───────────────┴──────┴───────────────┴─────────────────┴─────────┘

SwitchMetric Table (7000+ rows, 3 new rows every 10 seconds)
┌────┬───────────┬───────────────┬───────────┬─────────────┬───────────┬──────────────────────┐
│ id │ switch_id │ timestamp     │ cpu_usage │ temperature │ bandwidth │ anomalies            │
├────┼───────────┼───────────────┼───────────┼─────────────┼───────────┼──────────────────────┤
│ 1  │ 1         │ 2026-06-06... │ 84        │ 72          │ 520       │ ML DETECTED ANOMALY  │
│ 2  │ 2         │ 2026-06-06... │ 31        │ 41          │ 410       │ None                 │
│ 3  │ 3         │ 2026-06-06... │ 57        │ 63          │ 680       │ None                 │
└────┴───────────┴───────────────┴───────────┴─────────────┴───────────┴──────────────────────┘

AlertHistory Table (1289 rows)
┌────┬───────────┬───────────────┬──────────────────────┬───────────┬─────────────┬────────────┐
│ id │ switch_id │ timestamp     │ anomaly_type         │ cpu_usage │ temperature │ email_sent │
├────┼───────────┼───────────────┼──────────────────────┼───────────┼─────────────┼────────────┤
│ 1  │ 1         │ 2026-06-06... │ ML DETECTED ANOMALY  │ 84        │ 72          │ True       │
│ 2  │ 3         │ 2026-06-05... │ HIGH CPU: 87%        │ 87        │ 58          │ False      │
└────┴───────────┴───────────────┴──────────────────────┴───────────┴─────────────┴────────────┘
```

---

## SECTION 15: REAL SWITCH READY

To connect a real Cisco/HP/any switch to this system:

1. Go to `localhost:8000/admin/`
2. Click **Switches → Add Switch**
3. Fill in:
   - **Name:** any descriptive name
   - **IP Address:** switch's actual IP (e.g. 192.168.1.1)
   - **Port:** 161 (standard SNMP port)
   - **Community String:** switch's read-only community string (not "public" in production)
   - **is_demo:** uncheck (set to False)

4. Dashboard automatically shows 🟢 **Live Mode** when a real switch is added
5. No code changes needed — the architecture handles both real and virtual

---

## SECTION 16: INTERVIEW ONE-LINERS

**60-second explanation:**
> "I built an AI-powered network switch monitoring system during my Tata Steel internship. The system polls 3 virtual switches every 10 seconds using real SNMP protocol — same protocol as SolarWinds. Metrics are stored in PostgreSQL on Supabase. An Isolation Forest ML model trained on 537 samples detects anomalies by learning each switch's individual baseline. The Django dashboard updates in real time via WebSocket using Redis and Daphne. I also built a React frontend consuming the same REST API. The system is deployed on Render (Django) and Vercel (React)."

**If asked "why not just use thresholds?"**
> "Thresholds are static. Core Switch at 80% CPU is normal operation for it — flagging that is a false alarm. Access Switch at 80% CPU is a crisis. ML adapts to each switch's individual behavior automatically without manually tuning one threshold per switch per metric."

**If asked "how does WebSocket work?"**
> "monitor_snmp.py sends to Redis channel layer, Daphne picks it up, MetricsConsumer forwards to browser via WebSocket. The key insight was that InMemoryChannelLayer doesn't work across processes — Redis is the shared external broker. Without it, messages silently disappear."

**If asked "what was the hardest bug?"**
> "WebSocket was connected (status 101), monitor was pushing (logs showed it), but browser was receiving nothing. No error anywhere. Turned out InMemoryChannelLayer stores messages in RAM of only one process. Monitor and Daphne are two separate processes. Added Redis as external broker and it worked immediately. Silent failures with no error messages are harder to debug than crashes."

---

## SECTION 17: LIVE DEMO URLS

| Version | URL |
|---------|-----|
| Django Dashboard | https://network-monitor-ai.onrender.com |
| React Dashboard | https://network-monitor-ai.vercel.app |
| GitHub Repository | https://github.com/Arnav-Naive/network-monitor-ai |

**Note:** Render free tier has 50-second spin-up delay after inactivity.
WebSocket falls back to 10-second auto-refresh on deployed version (Render free tier doesn't support persistent WebSocket connections).

---

## SECTION 18: NUMBERS THAT MATTER

| Metric | Value |
|--------|-------|
| Total Development Days | 27 working days |
| GitHub PRs Merged | 11 |
| ML Training Samples | 537 readings |
| ML Features | 7 per reading |
| Switches Monitored | 3 (virtual, ready for real) |
| Polling Interval | Every 10 seconds |
| Database Records | 7000+ metrics, 1289 alerts |
| API Endpoints | 3 (metrics, switches, anomalies) |
| Alert History Records | 1289 |
| Emails Sent | 4 (30-minute cooldown) |
| Tech Stack Items | 20+ |

---

*Arnav Fating | Tata Steel Prashikshan Internship 2026 | github.com/Arnav-Naive/network-monitor-ai*