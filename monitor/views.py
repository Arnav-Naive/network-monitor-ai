from django.shortcuts import render
from .models import SwitchMetric
from django.db.models import Count, Q
from django.utils import timezone
import json
import csv
from django.http import HttpResponse
from datetime import datetime, timedelta

def dashboard_view(request):
    # Get filter parameters from URL
    filter_type = request.GET.get('filter', 'all')      # all / anomalies / normal
    date_range = request.GET.get('range', '24h')         # 1h / 24h / 7d / all

    # Date range filter
    now = timezone.now()
    if date_range == '1h':
        from_time = now - timedelta(hours=1)
    elif date_range == '24h':
        from_time = now - timedelta(hours=24)
    elif date_range == '7d':
        from_time = now - timedelta(days=7)
    else:
        from_time = None

    # Base queryset
    logs_qs = SwitchMetric.objects.all()
    if from_time:
        logs_qs = logs_qs.filter(timestamp__gte=from_time)

    # Anomaly type filter
    if filter_type == 'anomalies':
        logs_qs = logs_qs.exclude(Q(anomalies__isnull=True) | Q(anomalies='None'))
    elif filter_type == 'normal':
        logs_qs = logs_qs.filter(Q(anomalies__isnull=True) | Q(anomalies='None'))

    logs = logs_qs[:50]

    # Chart data
    chart_data = list(logs_qs[:50])
    chart_data.reverse()

    # Summary stats (always from full DB)
    total_logs = SwitchMetric.objects.count()
    ml_anomalies = SwitchMetric.objects.filter(
        anomalies__icontains='ML DETECTED'
    ).count()
    normal_logs = SwitchMetric.objects.filter(
        Q(anomalies__isnull=True) | Q(anomalies='None')
    ).count()
    normal_percentage = round((normal_logs / total_logs * 100), 1) if total_logs > 0 else 0

    timestamps = [log.timestamp.strftime('%H:%M:%S') for log in chart_data]
    cpu_data = [log.cpu_usage for log in chart_data]
    temp_data = [log.temperature for log in chart_data]
    memory_data = [log.memory_usage for log in chart_data]

    context = {
        'logs': logs,
        'total_logs': total_logs,
        'ml_anomalies': ml_anomalies,
        'normal_logs': normal_logs,
        'normal_percentage': normal_percentage,
        'timestamps': json.dumps(timestamps),
        'cpu_data': json.dumps(cpu_data),
        'temp_data': json.dumps(temp_data),
        'memory_data': json.dumps(memory_data),
        'filter_type': filter_type,
        'date_range': date_range,
    }

    return render(request, 'monitor/dashboard.html', context)


def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="network_monitor_export.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Timestamp', 'CPU (%)', 'Memory (%)', 'Temperature (°C)',
        'Bandwidth (Mbps)', 'Interface', 'CRC Errors',
        'Reliability', 'TX (Mbps)', 'RX (Mbps)', 'Anomalies'
    ])

    for log in SwitchMetric.objects.all():
        writer.writerow([
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            log.cpu_usage, log.memory_usage, log.temperature,
            log.bandwidth, 'UP' if log.interface_status else 'DOWN',
            log.crc_errors, log.reliability, log.tx_rate, log.rx_rate,
            log.anomalies or 'None'
        ])

    return response