import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dashboard.settings')
django.setup()

from monitor.models import SwitchMetric, AlertHistory

print("Migrating old anomalies to AlertHistory...")

old_anomalies = SwitchMetric.objects.exclude(
    anomalies__isnull=True
).exclude(anomalies='None').select_related('switch').order_by('-timestamp')[:200]

records = []
for metric in old_anomalies:
    if metric.switch:
        records.append(AlertHistory(
            switch=metric.switch,
            timestamp=metric.timestamp,
            anomaly_type=metric.anomalies,
            cpu_usage=metric.cpu_usage,
            temperature=metric.temperature,
            email_sent=False,
        ))

AlertHistory.objects.bulk_create(records, ignore_conflicts=True)
print(f"✓ Migrated {len(records)} anomaly records to AlertHistory")