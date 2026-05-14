from django.core.mail import send_mail
from django.conf import settings

def send_anomaly_alert(metric, anomalies):
    """Send email when ML detects anomaly"""
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
            [settings.EMAIL_HOST_USER],  # sends to yourself
            fail_silently=False,
        )
        print(f"  📧 Alert email sent!")
        return True
    except Exception as e:
        print(f"  ❌ Email failed: {e}")
        return False