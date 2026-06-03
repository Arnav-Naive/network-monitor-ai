# Day 20 — Docs Fix + Alert History Migration

**Date:** 2026-06-03

## What I Did

### Fix 1: ml-workflow.md — 341 → 537 samples
Old doc said 341 samples. Model retrained on 537. Updated to reflect reality.
Never leave outdated numbers in docs — interviewers notice.

### Fix 2: README badge — Week 2-3 → Week 2-6
Small but matters. Shows project was actively developed over 6 weeks.

### Fix 3: Alert History Migration Script
`src/migrate_alerts.py` — backfills old SwitchMetric anomalies into AlertHistory table.

**Problem:** AlertHistory model was new (Day 18). 
Old anomalies existed in SwitchMetric but AlertHistory was empty.
Demo mein "0 alerts" dikhta — weak lagta.

**Solution:** bulk_create se 200 recent anomaly records migrate kiye.

### Why bulk_create over get_or_create loop?
get_or_create = 1 DB query per record = 200 queries = slow/hang
bulk_create = 1 single query for all 200 records = fast

```python
AlertHistory.objects.bulk_create(records, ignore_conflicts=True)
```

`ignore_conflicts=True` — duplicate pe crash nahi karega, skip karega.

## IPv6 Issue — Supabase
Direct connection IPv6 use karta hai.
Indian mobile hotspot mostly IPv4 only hota hai.
Fix: Session Pooler URL use karo — IPv4 compatible hai.

Old URL: `db.hnvknkothxwcjfrvrrvy.supabase.co`
New URL: `aws-1-ap-northeast-2.pooler.supabase.com`

## Result
- Alert History: 1289 total alerts visible
- Emails sent: 4 (cooldown 30 min ne baaki rok diye)
- Git: PR #6 merged cleanly