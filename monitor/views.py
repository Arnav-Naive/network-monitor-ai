import csv
from django.http import HttpResponse

from django.shortcuts import render
from .models import SwitchMetric
from django.db.models import Count, Q
import json

def dashboard_view(request):
    # Get last 50 entries for table
    logs = SwitchMetric.objects.all()[:50]
    
    # Get last 50 for chart (reverse order for chronological)
    chart_data = list(SwitchMetric.objects.all()[:50])
    chart_data.reverse()
    
    # Summary statistics
    total_logs = SwitchMetric.objects.count()
    ml_anomalies = SwitchMetric.objects.filter(
        anomalies__icontains='ML DETECTED'
    ).count()
    normal_logs = SwitchMetric.objects.filter(
        Q(anomalies__isnull=True) | Q(anomalies='None')
    ).count()
    
    # Calculate percentages
    normal_percentage = (normal_logs / total_logs * 100) if total_logs > 0 else 0
    
    # Prepare chart data
    timestamps = [log.timestamp.strftime('%H:%M:%S') for log in chart_data]
    cpu_data = [log.cpu_usage for log in chart_data]
    temp_data = [log.temperature for log in chart_data]
    memory_data = [log.memory_usage for log in chart_data]
    
# Prepare chart data as JSON strings
    
    context = {
        'logs': logs,
        'total_logs': total_logs,
        'ml_anomalies': ml_anomalies,
        'normal_logs': normal_logs,
        'normal_percentage': round(normal_percentage, 1),
        'timestamps': json.dumps(timestamps),
        'cpu_data': json.dumps(cpu_data),
        'temp_data': json.dumps(temp_data),
        'memory_data': json.dumps(memory_data),
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
    
    logs = SwitchMetric.objects.all()
    for log in logs:
        writer.writerow([
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            log.cpu_usage,
            log.memory_usage,
            log.temperature,
            log.bandwidth,
            'UP' if log.interface_status else 'DOWN',
            log.crc_errors,
            log.reliability,
            log.tx_rate,
            log.rx_rate,
            log.anomalies or 'None'
        ])
    
    return response