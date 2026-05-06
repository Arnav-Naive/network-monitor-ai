# Day 02 — Django Dashboard Setup

**Date:** 2026-05-06  
**Status:** Working prototype completed

## What I Built

Created Django web dashboard to visualize network monitoring data.

**Features:**
- Reads data from `data/logs.csv`
- Displays all metrics in HTML table
- Highlights anomalies in red
- Responsive table with hover effects

**Tech stack:**
- Django 5.x
- Python csv module
- HTML/CSS (inline styling)

**File structure:**
monitor/
├── views.py (dashboard_view function)
├── templates/monitor/dashboard.html
dashboard/
├── settings.py (registered monitor app)
├── urls.py (mapped root URL to dashboard)

## How It Works

1. `monitor.py` script generates simulated data → saves to CSV
2. Django view reads CSV using `csv.DictReader`
3. Data passed to HTML template as context
4. Template loops through data and renders table

## Next Steps

**Tomorrow:**
- Add auto-refresh (page updates every 10 seconds without manual reload)
- Improve UI styling
- Add metrics summary cards (total logs, anomaly count)

**After real switch access:**
- Replace CSV with database (SQLite/PostgreSQL)
- Connect to real SNMP data
- Add ML-based anomaly detection

---

*Basic dashboard working. Ready to scale.*