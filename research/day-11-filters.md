# Day 11 — Dashboard Filters

**Date:** 2026-05-15

## What I Built

Added two filters to the dashboard that work together:

**Time Range Filter:** Last 1h / Last 24h / Last 7d / All Time  
**Anomaly Type Filter:** All / Anomalies Only / Normal Only

## How It Works

Filters pass through URL parameters:
`http://localhost:8000/?range=24h&filter=anomalies`

Django reads them in the view:
```python
filter_type = request.GET.get('filter', 'all')
date_range = request.GET.get('range', '24h')
```

## New Concept: Q Objects

Normal filter: `logs.filter(anomalies='None')` — only works for exact match

Q objects allow OR conditions:
```python
from django.db.models import Q

# This means: anomalies is NULL OR anomalies equals 'None'
logs.filter(Q(anomalies__isnull=True) | Q(anomalies='None'))
```

Without Q objects this isn't possible in one line.

## New Concept: timedelta

Used to calculate time ranges:
```python
from datetime import timedelta
from_time = now - timedelta(hours=24)  # 24 hours ago
logs.filter(timestamp__gte=from_time)  # gte = greater than or equal
```

## Full Feature List After Day 11

- ✅ Real SNMP polling via Docker
- ✅ ML anomaly detection (Isolation Forest)
- ✅ Email alerts with 30-min cooldown
- ✅ CSV export
- ✅ Date range filters
- ✅ Anomaly type filters
- ✅ Auto-refresh dashboard
- ✅ Charts (CPU/Temp/Memory)
- ✅ Summary cards

## Next Steps

- Show complete system to mentor (Day 12)
- Multiple switch support
- Deployment