from django.db import models
    
class SwitchMetric(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.IntegerField()
    memory_usage = models.IntegerField()
    temperature = models.IntegerField()
    bandwidth = models.IntegerField()
    interface_status = models.IntegerField()  # 1=up, 0=down
    crc_errors = models.IntegerField()
    reliability = models.CharField(max_length=10)
    tx_rate = models.IntegerField()
    rx_rate = models.IntegerField()
    anomalies = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']  # newest first
    
    def __str__(self):
        return f"{self.timestamp} - CPU: {self.cpu_usage}%"