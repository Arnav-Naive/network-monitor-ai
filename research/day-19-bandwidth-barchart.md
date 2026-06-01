# Day 19 — Per-Switch Bandwidth Bar Chart + Project Complete

**Date:** 2026-06-01

## What I Built

Main dashboard pe ek naya bar chart add kiya — 
teeno switches ka bandwidth, TX rate, RX rate 
side by side comparison (latest reading).

**Why this matters:**
Line chart shows trends over time.
Bar chart shows comparison between switches at a glance.
Dono alag purpose serve karte hain — ek replace nahi karta doosre ko.

## How It Works

### Backend (views.py)
```python
switch_bandwidth = []
for s in switches:
    latest_metric = SwitchMetric.objects.filter(switch=s).order_by('-timestamp').first()
    switch_bandwidth.append({
        'name': s.name,
        'bandwidth': latest_metric.bandwidth if latest_metric else 0,
        'tx': latest_metric.tx_rate if latest_metric else 0,
        'rx': latest_metric.rx_rate if latest_metric else 0,
    })
```

Har switch ka latest reading fetch karo → dict mein store karo →
JSON mein convert karke template ko bhejo.

### Frontend (dashboard.js)
```javascript
const switchData = JSON.parse(bandwidthEl.dataset.bandwidth);
const switchNames = switchData.map(s => s.name);
const bandwidthValues = switchData.map(s => s.bandwidth);
```

`map()` — array ke har element pe ek operation karo, 
naya array return karo. Yahan switch objects se sirf 
names ya values nikal rahe hain.

### Chart.js Bar Chart
```javascript
new Chart(ctx, {
    type: 'bar',  // line ki jagah bar
    data: {
        labels: switchNames,  // X axis
        datasets: [
            { label: 'Bandwidth', data: bandwidthValues },
            { label: 'TX Rate', data: txValues },
            { label: 'RX Rate', data: rxValues }
        ]
    }
});
```

3 datasets = 3 colored bars per switch.
Chart.js automatically groups them side by side.

## Under The Hood

**Data hidden in HTML, read by JS — kyun?**

Django = server side (Python).
Chart.js = client side (JavaScript).

Dono directly baat nahi kar sakte. 
Solution: Django data ko HTML mein hidden div mein 
serialize karke rakh do, JS wahan se padh le.

```html
<!-- Django puts data here -->
<div id="bandwidthData" data-bandwidth='{{ switch_bandwidth|safe }}'></div>

<!-- JS reads from here -->
const data = JSON.parse(document.getElementById('bandwidthData').dataset.bandwidth);
```

Yeh pattern pure Django projects mein bahut common hai.
React mein yeh problem nahi hoti — directly API call kar sakte hain.

## Week 5 Summary — What Got Built

| Feature | Branch | PR |
|---------|--------|----|
| Real switch support | feature/real-switch-support | #2 |
| Demo/Live indicator | feature/demo-mode-indicator | #3 |
| Per-switch detail page | feature/switch-detail-page | #3 |
| Alert history page | feature/alert-history | #4 |
| Bandwidth bar chart | feature/bandwidth-barchart | #5 |

## Project Final Status

✅ 3-switch SNMP monitoring (Docker)
✅ ML anomaly detection (Isolation Forest, 537 samples)
✅ PostgreSQL via Supabase
✅ REST API (3 endpoints)
✅ WebSocket live updates (Redis + Daphne)
✅ Email alerts with cooldown + alert history
✅ Per-switch detail pages
✅ Bar chart + line charts
✅ Real switch ready (plug in IP + community string)
✅ Demo/Live mode indicator
✅ CSV export
✅ Proper Git workflow (feature branches + PRs)

