from django.shortcuts import render
from .models import SwitchMetric, Switch
from django.db.models import Q
from django.utils import timezone
import json
import csv
from django.http import HttpResponse
from datetime import timedelta

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import SwitchMetricSerializer, SwitchSerializer

from .models import SwitchMetric, Switch, AlertHistory

def dashboard_view(request):
    filter_type = request.GET.get('filter', 'all')
    date_range = request.GET.get('range', '24h')
    switch_id = request.GET.get('switch', 'all')

    now = timezone.now()
    if date_range == '1h':
        from_time = now - timedelta(hours=1)
    elif date_range == '24h':
        from_time = now - timedelta(hours=24)
    elif date_range == '7d':
        from_time = now - timedelta(days=7)
    else:
        from_time = None

    logs_qs = SwitchMetric.objects.select_related('switch').all()

    if from_time:
        logs_qs = logs_qs.filter(timestamp__gte=from_time)
    if switch_id != 'all':
        logs_qs = logs_qs.filter(switch_id=switch_id)
    if filter_type == 'anomalies':
        logs_qs = logs_qs.exclude(Q(anomalies__isnull=True) | Q(anomalies='None'))
    elif filter_type == 'normal':
        logs_qs = logs_qs.filter(Q(anomalies__isnull=True) | Q(anomalies='None'))

    logs = logs_qs[:50]
    chart_data = list(logs_qs[:50])
    chart_data.reverse()

    total_logs = SwitchMetric.objects.count()
    ml_anomalies = SwitchMetric.objects.filter(anomalies__icontains='ML DETECTED').count()
    normal_logs = SwitchMetric.objects.filter(Q(anomalies__isnull=True) | Q(anomalies='None')).count()
    normal_percentage = round((normal_logs / total_logs * 100), 1) if total_logs > 0 else 0

    switches = Switch.objects.filter(is_active=True)

    context = {
        'logs': logs,
        'total_logs': total_logs,
        'ml_anomalies': ml_anomalies,
        'normal_percentage': normal_percentage,
        'timestamps': json.dumps([l.timestamp.strftime('%H:%M:%S') for l in chart_data]),
        'cpu_data': json.dumps([l.cpu_usage for l in chart_data]),
        'temp_data': json.dumps([l.temperature for l in chart_data]),
        'memory_data': json.dumps([l.memory_usage for l in chart_data]),
        'filter_type': filter_type,
        'date_range': date_range,
        'switch_id': switch_id,
        'switches': switches,
        'has_real_switches': Switch.objects.filter(is_demo=False, is_active=True).exists(),  # ADD THIS
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


@api_view(['GET'])
def api_metrics(request):
    """Returns last 100 metrics as JSON"""
    switch_id = request.GET.get('switch', None)
    
    metrics = SwitchMetric.objects.select_related('switch').all()[:100]
    
    if switch_id:
        metrics = SwitchMetric.objects.filter(switch_id=switch_id)[:100]
    
    serializer = SwitchMetricSerializer(metrics, many=True)
    return Response({
        'count': len(serializer.data),
        'results': serializer.data
    })

@api_view(['GET'])
def api_switches(request):
    """Returns all switches as JSON"""
    switches = Switch.objects.filter(is_active=True)
    serializer = SwitchSerializer(switches, many=True)
    return Response({
        'count': switches.count(),
        'results': serializer.data
    })

@api_view(['GET'])
def api_anomalies(request):
    """Returns only anomaly records"""
    anomalies = SwitchMetric.objects.select_related('switch').exclude(
        anomalies__isnull=True
    ).exclude(anomalies='None')[:50]
    
    serializer = SwitchMetricSerializer(anomalies, many=True)
    return Response({
        'count': len(serializer.data),
        'results': serializer.data
    })
    
def switch_detail_view(request, switch_id):
    switch = Switch.objects.get(id=switch_id)
    
    # Last 100 readings of this switch    
    metrics_qs = SwitchMetric.objects.filter(switch=switch).order_by('-timestamp')

    # Stats
    total = metrics_qs.count()
    anomaly_count = metrics_qs.filter(anomalies__isnull=False).exclude(anomalies='None').count()
    normal_count = total - anomaly_count
    health = round((normal_count / total * 100), 1) if total > 0 else 0

    # Latest reading
    latest = metrics_qs.first()

    # Chart data
    chart_data = list(metrics_qs[:50])
    chart_data.reverse()

    metrics = metrics_qs[:100]  # slice at the end
    
    context = {
        'switch': switch,
        'metrics': metrics,
        'total': total,
        'anomaly_count': anomaly_count,
        'health': health,
        'latest': latest,
        'timestamps': json.dumps([m.timestamp.strftime('%H:%M:%S') for m in chart_data]),
        'cpu_data': json.dumps([m.cpu_usage for m in chart_data]),
        'temp_data': json.dumps([m.temperature for m in chart_data]),
        'memory_data': json.dumps([m.memory_usage for m in chart_data]),
        'bandwidth_data': json.dumps([m.bandwidth for m in chart_data]),
    }
    
    return render(request, 'monitor/switch_detail.html', context)

def alert_history_view(request):
    alerts = AlertHistory.objects.select_related('switch').all()[:100]
    
    total_alerts = AlertHistory.objects.count()
    email_sent_count = AlertHistory.objects.filter(email_sent=True).count()
    
    context = {
        'alerts': alerts,
        'total_alerts': total_alerts,
        'email_sent_count': email_sent_count,
    }
    
    return render(request, 'monitor/alert_history.html', context)