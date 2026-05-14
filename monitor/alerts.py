from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from .models import SwitchMetric

# Track last alert time (in memory)
last_alert_time = None

def send_anomaly_alert(metric, anomalies):
    global last_alert_time
    
    # Cooldown: only send every 30 minutes
    if last_alert_time and timezone.now() - last_alert_time < timedelta(minutes=30):
        return False
    
    subject = f"⚠ Network Anomaly Detected - {metric.timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
    
    message = f"""
NETWORK ANOMALY ALERT
=====================
Time: {metric.timestamp.strftime('%Y-%m-%d %H:%M:%S')}
Anomalies: {', '.join(anomalies)}

Metrics at time of detection:
- CPU Usage: {metric.cpu_usage}%
- Memory Usage: {metric.memory_usage}%
- Temperature: {metric.temperature}°C
- Bandwidth: {metric.bandwidth} Mbps
- Interface Status: {'UP' if metric.interface_status else 'DOWN'}

Login to dashboard: http://localhost:8000
    """
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [settings.EMAIL_HOST_USER],
            fail_silently=False,
        )
        last_alert_time = timezone.now()
        print(f"  📧 Alert email sent!")
        return True
    except Exception as e:
        print(f"  ❌ Email failed: {e}")
        return False