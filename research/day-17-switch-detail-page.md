# Day 17 — Per-Switch Detail Page + Git Workflow

**Date:** 2026-05-31

## What I Built

### Feature: Per-Switch Detail Page
Har switch ka apna dedicated page — `/switch/1/`, `/switch/2/`, `/switch/3/`

Main dashboard pe switch name pe click karo → uski full detail page khulti hai.

**Page mein kya dikhta hai:**
- Switch info — IP, port, location, community string, Demo/Live badge
- Latest reading cards — CPU, Memory, Temperature, Bandwidth, Health%, Anomaly count
- Line chart — CPU, Temperature, Memory (last 50 readings)
- Bar chart — Bandwidth utilization (last 50 readings)  
- Full metrics table — last 100 readings

## New Concepts

### URL Parameters
```python
path('switch/<int:switch_id>/', views.switch_detail_view, name='switch_detail'),
```
`<int:switch_id>` — URL se integer value capture karke view function mein bhejta hai.
`/switch/1/` → `switch_id = 1`
`/switch/2/` → `switch_id = 2`

### Queryset Slicing Bug
**Problem:**
```python
metrics = queryset[:100]  # slice le liya
anomaly_count = metrics.filter(...)  # ERROR — slice ke baad filter nahi ho sakta
```

**Fix:**
```python
metrics_qs = queryset  # pehle saari operations
total = metrics_qs.count()
anomaly_count = metrics_qs.filter(...).count()
metrics = metrics_qs[:100]  # slice sabse last mein
```

**Rule:** Django queryset pe pehle saare filters/counts karo, slice sabse end mein lo.

### Bar Chart (Chart.js)
```javascript
new Chart(ctx, {
    type: 'bar',  // line ki jagah bar
    data: {
        datasets: [{
            backgroundColor: 'rgba(102,126,234,0.7)',  // fill color
            borderColor: 'rgb(102,126,234)',
        }]
    }
});
```

## Git Workflow — PR #3
git checkout -b feature/switch-detail-page
... code likha ...
git add .
git commit -m "day-17: per-switch detail page with charts"
git push origin feature/switch-detail-page
GitHub pe PR banaya → Merge kiya → git pull origin main

## Bugs Fixed

**Bug 1:** `dashboard.html` mein `has_real_switches` context variable add karna bhool gaya tha — Demo Mode banner nahi dikh raha tha.

**Bug 2:** Queryset slice ke baad filter — `TypeError: Cannot filter a query once a slice has been taken.`

**Bug 3:** Hotel WiFi DNS restriction — Supabase hostname resolve nahi ho raha tha. Fix: sirf hotspot use karo.

## Next Steps

- Alert history page
- Bar chart on main dashboard (per-switch bandwidth comparison)