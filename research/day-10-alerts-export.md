# Day 10 — Email Alerts + CSV Export

**Date:** 2026-05-14

## Feature 1: Email Alerts

When ML detects an anomaly, system sends an email automatically.

**How it works:**
1. `monitor_snmp.py` detects anomaly
2. Calls `send_anomaly_alert()` from `monitor/alerts.py`
3. Django's `send_mail()` sends via Gmail SMTP

**Key concept — SMTP:**
SMTP = Simple Mail Transfer Protocol. Gmail acts as relay.
Credentials stored in `.env` file (never committed to GitHub).

**Cooldown system:**
```python
COOLDOWN_MINUTES = 30  # prevents spam
# Change to 1 for demo, 30 for production
```

**Gmail App Password:**
Not your real Gmail password. Generated separately under
Google Account → Security → App Passwords.
More secure — can be revoked without changing main password.

## Feature 2: CSV Export

Added `/export/` URL that downloads all data as CSV file.

```python
response = HttpResponse(content_type='text/csv')
response['Content-Disposition'] = 'attachment; filename="export.csv"'
```

`Content-Disposition` header tells browser to download the file
instead of displaying it.

## What I Didn't Understand (Honest)

- async/await pattern in Python
- sync_to_async wrapper for Django DB calls
- Docker internals

These worked via copy-paste. Will revisit when needed again.

## Files Changed

- `monitor/alerts.py` — new file, email logic
- `monitor/views.py` — added export_csv view
- `dashboard/urls.py` — added /export/ route
- `dashboard/settings.py` — email configuration
- `.env` — Gmail credentials (not in GitHub)