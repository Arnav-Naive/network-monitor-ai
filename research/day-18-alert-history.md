# Day 18 — Alert History Page

**Date:** 2026-05-31

## What I Built

Ek dedicated page jo saare ML anomaly alerts track karta hai.
URL: `localhost:8000/alerts/`

**Page mein kya dikhta hai:**
- Total alerts count
- Emails sent count
- Failed emails count
- Full table — timestamp, switch, anomaly type, CPU, temp, email status

## New Model — AlertHistory

```python
class AlertHistory(models.Model):
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    anomaly_type = models.CharField(max_length=200)
    cpu_usage = models.IntegerField()
    temperature = models.IntegerField()
    email_sent = models.BooleanField(default=False)
```

Har baar ML anomaly detect hoti hai aur email jaata hai —
ek row save hoti hai is table mein.

## How It Works
monitor_snmp.py detects ML anomaly
→ send_anomaly_alert() called
→ email send karne ki koshish
→ success ya fail — dono cases mein AlertHistory.objects.create()
→ /alerts/ page pe dikh jaata hai

## Key Learning — ForeignKey

```python
switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
```

`CASCADE` matlab — agar Switch delete ho toh uske saare 
AlertHistory records bhi delete ho jayenge automatically.

## Under The Hood

**Kyun alag model banaya SwitchMetric se alag:**
SwitchMetric = har 10 second ka data (thousands of rows)
AlertHistory = sirf wo moments jab alert gaya (few rows)

Dono alag purpose ke liye — mix karna galat hota.

## Next Steps

- Bar chart on main dashboard
- LinkedIn post
- Final commit + project wrap up