# Network Monitor AI — Complete Walkthrough

> Read this like a story — start to finish.

---

## The One-Line Explanation

> "I built a system that watches network switches, learns their normal behavior using machine learning, and alerts you when something unusual happens — like a smarter version of SolarWinds."

---

## The Big Picture (Before Opening Any File)

```
3 Docker Containers (fake switches)
        ↓ SNMP protocol (UDP port 161)
monitor_snmp.py (polls every 10 seconds)
        ↓ saves data
Supabase PostgreSQL (cloud database)
        ↓ reads data          ↓ pushes instantly
Django Dashboard          WebSocket (Redis)
  localhost:8000               ↓
                          Browser updates live
        ↓ if anomaly
Email Alert sent
```

That's the entire system. Everything else is just the details of each arrow.

---

## Part 1: The Fake Switches (Docker)

**Open:** `docker-snmp/` folder

### `docker-snmp/Dockerfile`

```dockerfile
FROM ubuntu:22.04
RUN apt-get install -y snmpd   # installs real SNMP software
COPY scripts/*.sh /usr/local/bin/
COPY snmpd.conf /etc/snmp/snmpd.conf
CMD ["snmpd", "-f", ...]       # runs SNMP agent when container starts
```

This is a recipe. When you run `docker build`, Docker creates a mini Ubuntu Linux computer with SNMP installed.

### `docker-snmp/snmpd.conf`

This config file tells SNMP: "when someone asks for CPU, run `cpu.sh` and return the result."

### `docker-snmp/scripts/cpu.sh`

```bash
#!/bin/sh
MIN=${CPU_MIN:-40}
MAX=${CPU_MAX:-90}
echo $((MIN + $(od -An -N2 -tu2 /dev/urandom) % RANGE))
```

Generates a random number between MIN and MAX. Each switch has different ranges set in `docker-compose.yml`.

### `docker-snmp/docker-compose.yml`

```yaml
switch1:  CPU 60-90%   (Core Switch — always busy)
switch2:  CPU 20-50%   (Access Switch — light load)
switch3:  CPU 40-75%   (Distribution Switch — medium)
```

3 containers, 3 different personalities. This is why ML matters — same CPU% means different things for different switches.

**Command to start all 3:**

```bash
docker compose -f docker-snmp/docker-compose.yml up -d
```

---

## Part 2: The Database (What Gets Stored)

**Open:** `monitor/models.py`

Two tables:

### Switch table — stores the 3 switches

```python
class Switch(models.Model):
    name = "Core Switch 01"
    ip_address = "127.0.0.1"
    port = 1161
    location = "Server Room A"
```

### SwitchMetric table — stores every reading

```python
class SwitchMetric(models.Model):
    switch = ForeignKey(Switch)   # which switch this reading came from
    timestamp = auto              # when it was recorded
    cpu_usage = 78
    memory_usage = 65
    temperature = 61
    bandwidth = 450
    anomalies = "ML DETECTED ANOMALY"  # or None
```

Every 10 seconds, 3 new rows get added — one per switch. After a day you have thousands of rows.

---

## Part 3: The Monitor Script (The Heart)

**Open:** `src/monitor_snmp.py`

This is the script that runs continuously. Walk through it top to bottom:

### Step 1 — Django setup (lines 1–12)

```python
sys.path.insert(0, ...)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()
```

Loads Django so we can use models outside the web server.

### Step 2 — OIDs (lines 14–19)

```python
OIDS = {
    'cpu': '1.3.6.1.4.1.8072.1.3.2.3.1.2.3.99.112.117',
    ...
}
```

OID = address of a specific metric on the switch. Like a phone number — you call this number to get CPU usage.

### Step 3 — `get_snmp_value()` (lines 21–40)

```python
async def get_snmp_value(ip, port, oid):
    errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
        SnmpEngine(),
        CommunityData('public'),      # password = "public"
        UdpTransportTarget((ip, port)),
        ObjectType(ObjectIdentity(oid))
    )
    return int(str(varBind[1]).strip())
```

Sends one SNMP GET request. Like calling the switch: "give me your CPU value." Returns an integer.

### Step 4 — `poll_switch()` (lines 42–60)

```python
async def poll_switch(switch):
    cpu       = await get_snmp_value(ip, port, OIDS['cpu'])
    memory    = await get_snmp_value(ip, port, OIDS['memory'])
    temperature = await get_snmp_value(ip, port, OIDS['temperature'])
    bandwidth = await get_snmp_value(ip, port, OIDS['bandwidth'])
    return { "cpu_usage": cpu, ... }
```

Polls all 4 metrics from one switch. Returns a dictionary.

### Step 5 — ML model loading (lines 62–68)

```python
with open('anomaly_model.pkl', 'rb') as f:
    ml_model = pickle.load(f)
```

Loads the trained model from disk once at startup. Pickle = Python's way of saving objects to files.

### Step 6 — `detect_anomaly()` (lines 70–85)

```python
def detect_anomaly(data):
    features = np.array([[cpu, memory, temp, bandwidth, crc, tx, rx]])

    if ml_model.predict(features)[0] == -1:
        anomalies.append("ML DETECTED ANOMALY")

    if data["cpu_usage"] > 85:
        anomalies.append("HIGH CPU: 85%")
```

Two types of detection running simultaneously:
- **ML model** — "is this pattern unusual for this switch?"
- **Threshold** — "is this number too high?"

### Step 7 — `save_metric()` (lines 87–120)

```python
@sync_to_async
def save_metric(switch, data, anomalies):
    metric = SwitchMetric.objects.create(...)   # save to database

    if 'ML DETECTED' in anomalies:
        send_anomaly_alert(metric, anomalies)   # send email

    channel_layer.group_send('metrics', {...})  # push to WebSocket

    return metric
```

Three things happen when saving: database write, email alert, WebSocket push.

### Step 8 — `monitor_loop()` (lines 122–145)

```python
async def monitor_loop():
    while True:
        switches = await get_switches()            # get 3 switches from DB

        tasks = [poll_switch(s) for s in switches]
        results = await asyncio.gather(*tasks)     # poll all 3 simultaneously

        for switch, data in zip(switches, results):
            anomalies = detect_anomaly(data)
            metric = await save_metric(switch, data, anomalies)
            print(f"{switch.name} | CPU: {data['cpu_usage']}%")

        await asyncio.sleep(10)   # wait 10 seconds, repeat
```

The main loop. `asyncio.gather` is key — polls all 3 switches at the same time instead of one by one.

---

## Part 4: The ML Model

**Open:** `src/train_model.py`

```python
data = SwitchMetric.objects.all().values_list(
    'cpu_usage', 'memory_usage', 'temperature',
    'bandwidth', 'crc_errors', 'tx_rate', 'rx_rate'
)
# data shape: 537 rows × 7 columns

X = np.array(data)

model = IsolationForest(contamination=0.1, random_state=42)
model.fit(X)    # learns what "normal" looks like

pickle.dump(model, f)   # saves to anomaly_model.pkl
```

### What IsolationForest Actually Does

Imagine 537 data points plotted in 7-dimensional space. Normal points cluster together. Anomalies are isolated. The algorithm builds random trees — anomalies get isolated in fewer cuts (shorter path). Score close to `-1` = anomaly, close to `+1` = normal.

`contamination=0.1` = "expect roughly 10% of readings to be anomalies"

### Why This Is Better Than Thresholds

Core Switch normally runs at 70–90% CPU. Access Switch normally runs at 20–50%. If Access Switch suddenly hits 70%, that's unusual **for that switch** even though 70% isn't globally "bad." ML learns each switch's baseline. Thresholds don't.

---

## Part 5: Email Alerts

**Open:** `monitor/alerts.py`

```python
COOLDOWN_MINUTES = 30   # change to 1 for demo

def send_anomaly_alert(metric, anomalies):
    if last_alert_time and timezone.now() - last_alert_time < timedelta(minutes=30):
        return False    # cooldown active, skip

    send_mail(
        subject="⚠ Network Anomaly Detected",
        message=f"CPU: {metric.cpu_usage}%, Anomaly: {anomalies}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.EMAIL_HOST_USER],
    )
    last_alert_time = timezone.now()
```

Only ML detections trigger emails, not threshold alerts. Cooldown prevents spam.

---

## Part 6: The Dashboard

**Open:** `monitor/views.py`

### `dashboard_view()` — the main page

```python
def dashboard_view(request):
    filter_type = request.GET.get('filter', 'all')   # from URL ?filter=anomalies
    date_range  = request.GET.get('range', '24h')    # from URL ?range=1h
    switch_id   = request.GET.get('switch', 'all')   # from URL ?switch=2

    logs_qs = SwitchMetric.objects.select_related('switch').all()
    # apply filters...

    total_logs   = SwitchMetric.objects.count()
    ml_anomalies = SwitchMetric.objects.filter(anomalies__icontains='ML DETECTED').count()

    return render(request, 'monitor/dashboard.html', context)
```

### `monitor/templates/monitor/dashboard.html` — structure top to bottom

1. Header
2. Export CSV button → calls `/export/` URL
3. Filter bar → time range + anomaly type + switch selector
4. 3 summary cards → Total Logs, ML Anomalies, System Health %
5. Line chart → Chart.js, shows last 50 readings
6. Data table → every metric, color coded

### `monitor/static/monitor/js/dashboard.js`

```javascript
const ws = new WebSocket(`ws://${window.location.host}/ws/metrics/`);

ws.onmessage = function(event) {
    const data = JSON.parse(event.data);
    addTableRow(data);    // adds row to top of table instantly
};

ws.onclose = function() {
    setTimeout(function(){ location.reload(); }, 10000);   // fallback
};
```

WebSocket replaces the old `setTimeout(reload)`. New rows appear instantly without any page refresh.

---

## Part 7: WebSocket (How Live Updates Work)

**Open:** `monitor/consumers.py`

```python
class MetricsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add('metrics', self.channel_name)
        await self.accept()    # browser connects → join 'metrics' group

    async def metrics_update(self, event):
        await self.send(text_data=json.dumps(event['data']))   # forward to browser
```

**Open:** `monitor/routing.py`

```python
websocket_urlpatterns = [
    re_path(r'ws/metrics/$', consumers.MetricsConsumer.as_asgi()),
]
```

Maps `ws://localhost:8000/ws/metrics/` to the consumer.

### The Full WebSocket Chain

```
monitor_snmp.py
    → channel_layer.group_send('metrics', data)
    → Redis (shared message broker)
    → Daphne reads from Redis
    → MetricsConsumer.metrics_update()
    → browser ws.onmessage()
    → addTableRow(data)
    → new row appears in table
```

Redis is critical — without it, monitor and Daphne can't talk (different processes, different memory).

---

## Part 8: REST API

**Open:** `monitor/views.py` — bottom section

```python
@api_view(['GET'])
def api_metrics(request):
    metrics = SwitchMetric.objects.all()[:100]
    serializer = SwitchMetricSerializer(metrics, many=True)
    return Response({'count': len(serializer.data), 'results': serializer.data})
```

**Open:** `monitor/serializers.py`

```python
class SwitchMetricSerializer(serializers.ModelSerializer):
    switch_name = serializers.CharField(source='switch.name', read_only=True)
    class Meta:
        model = SwitchMetric
        fields = ['id', 'switch_name', 'cpu_usage', ...]
```

Serializer converts Django model objects → JSON automatically.

**3 endpoints:**
- `localhost:8000/api/switches/` → list of all switches
- `localhost:8000/api/metrics/` → last 100 readings
- `localhost:8000/api/anomalies/` → only anomaly records

---

## Part 9: Settings and Config

**Open:** `dashboard/settings.py` — key sections only

```python
DATABASES = { dj_database_url.config(os.environ.get('DATABASE_URL')) }
# Supabase PostgreSQL — connection string from .env

CHANNEL_LAYERS = { 'BACKEND': 'channels_redis.core.RedisChannelLayer' }
# Redis for WebSocket cross-process messaging

ASGI_APPLICATION = 'dashboard.asgi.application'
# Uses ASGI (not WSGI) because of WebSocket support
```

**Open:** `dashboard/asgi.py`

```python
application = ProtocolTypeRouter({
    'http': get_asgi_application(),               # normal HTTP requests
    'websocket': URLRouter(websocket_urlpatterns) # WebSocket connections
})
```

Routes HTTP vs WebSocket to different handlers.

---

## How to Demo to Mentor (Step by Step)

### Before the meeting — start everything

```bash
# Terminal 1
docker start switch-core-01 switch-access-02 switch-dist-03
docker start redis

# Terminal 2
python src/monitor_snmp.py

# Terminal 3
daphne -p 8000 dashboard.asgi:application
```

### During demo — show in this order

**1. Terminal 2**
> "This is polling 3 virtual switches every 10 seconds via real SNMP protocol. Each switch has different CPU ranges — this simulates what real switches in different parts of the plant would look like."

**2. Dashboard** `localhost:8000`
> "This is the live dashboard. Watch the table — new rows appear automatically without any page refresh. That's WebSocket."

**3. Filter: Anomalies Only**
> "These are the ML-detected anomalies. Yellow = ML found an unusual pattern. Red = threshold crossed."

**4. API** `localhost:8000/api/anomalies/`
> "The system also exposes a REST API. Any other system — mobile app, another dashboard — can consume this data."

**5. Admin** `localhost:8000/admin/`
> "All 3 switches in database. 1800+ metric readings collected."

**6. GitHub**
Show daily commits over 3 weeks.

**7. Explain ML**
> "Isolation Forest is unsupervised. It trained on 537 samples and learned each switch's normal baseline. Core Switch normally runs 60–90% CPU — that's normal for it. Access Switch at 70% is unusual — ML flags that even though 70% isn't globally high. Thresholds can't do this."

### Answer to "humara past experience nahi hai"

> "Sir, Isolation Forest doesn't need past anomaly examples. It learns what normal looks like from current stable data. Your 1-year stable network is actually perfect training data — the model learns YOUR baseline, not a generic one."

---

## Complete File Map

```
network-monitor-ai/
│
├── src/
│   ├── monitor_snmp.py    ← MAIN SCRIPT — polls switches, saves data, sends alerts
│   └── train_model.py     ← Run once to train ML model
│
├── monitor/               ← Django app
│   ├── models.py          ← Switch + SwitchMetric database tables
│   ├── views.py           ← Dashboard view + 3 API endpoints
│   ├── serializers.py     ← Converts models to JSON for API
│   ├── consumers.py       ← WebSocket handler
│   ├── routing.py         ← WebSocket URL routing
│   ├── alerts.py          ← Email alert logic
│   ├── admin.py           ← Admin panel registration
│   └── templates/monitor/dashboard.html  ← The actual webpage
│
├── monitor/static/monitor/
│   ├── css/dashboard.css  ← All styling
│   └── js/dashboard.js    ← WebSocket + Chart.js code
│
├── dashboard/             ← Django project config
│   ├── settings.py        ← Database, Redis, email, static files config
│   ├── urls.py            ← All URL routes
│   └── asgi.py            ← HTTP + WebSocket routing
│
├── docker-snmp/           ← Virtual switch setup
│   ├── Dockerfile         ← Container recipe
│   ├── snmpd.conf         ← SNMP agent config
│   ├── docker-compose.yml ← 3 switches with different profiles
│   └── scripts/           ← cpu.sh, memory.sh, temperature.sh, bandwidth.sh
│
├── .env                   ← DATABASE_URL, EMAIL credentials, SECRET_KEY (not in git)
├── requirements.txt       ← All Python dependencies
└── Procfile               ← Production deployment command
```

---

## One-Paragraph Summary for Any Interviewer

"I built an AI-powered network switch monitoring system during my Tata Steel internship. The system polls 3 virtual switches every 10 seconds using real SNMP protocol — the same protocol used by enterprise tools like SolarWinds. Metrics are stored in PostgreSQL on Supabase. An Isolation Forest ML model trained on 537 samples detects anomalies by learning each switch's individual baseline — so it catches subtle issues that fixed threshold alerts miss. The Django dashboard updates in real-time via WebSocket using Django Channels and Redis. The system also sends email alerts and exposes a REST API with 3 endpoints. The entire monitoring stack runs in Docker containers."

---

## Quick Reference — Things to Know Cold

| Question | Answer |
|----------|--------|
| What protocol does SNMP use? | UDP, port 161 |
| Why asyncio.gather? | Polls all 3 switches simultaneously, not one by one |
| Why Redis? | InMemoryChannelLayer only works in one process. Redis is shared between monitor_snmp.py and Daphne |
| Why Daphne instead of runserver? | Django's dev server doesn't support WebSocket. Daphne is an ASGI server |
| What does contamination=0.1 mean? | Tells IsolationForest to expect ~10% of data to be anomalous |
| What does -1 mean from model.predict()? | Anomaly. +1 means normal |
| Why select_related('switch')? | Avoids N+1 query problem — fetches switch data in same DB query instead of one query per row |
| Where is the ML model saved? | anomaly_model.pkl in project root |
| Why sync_to_async? | Django ORM is synchronous. Needed to call it from inside async monitor loop |
| What is a serializer? | Converts Django model objects → JSON for the REST API |

---

## Common Interview Questions on This Project

**"Why not use a simpler threshold-based system?"**
Thresholds are static. Core Switch at 80% CPU is normal, Access Switch at 80% is a crisis. ML adapts to each switch's individual behavior. You'd need one threshold per switch per metric manually maintained. ML generalizes automatically.

**"Why WebSocket instead of polling?"**
Polling wastes resources — browser asks every N seconds whether or not new data exists. WebSocket is event-driven — server pushes only when there's something new. More efficient, lower latency, more realistic for production monitoring.

**"Why PostgreSQL over SQLite?"**
SQLite is a file. It breaks under concurrent writes, doesn't support network access, and has no connection pooling. Every production system uses PostgreSQL or similar. Supabase gives cloud hosting, a visual table editor, and connection pooling for free.

**"What would you improve?"**
Per-switch ML models instead of one shared model. Right now all 3 switches train one IsolationForest together. Ideally each switch trains its own model so Access Switch anomalies don't get drowned out by Core Switch's noisy data.

**"What is ASGI vs WSGI?"**
WSGI handles one request at a time, synchronously. ASGI handles multiple connections concurrently and supports long-lived connections like WebSocket. Django added ASGI support in version 3.0. WebSocket requires ASGI — you can't use WSGI for this.