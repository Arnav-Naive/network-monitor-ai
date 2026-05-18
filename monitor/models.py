from django.db import models

class Switch(models.Model):
    name = models.CharField(max_length=100)
    ip_address = models.CharField(max_length=50)
    port = models.IntegerField(default=161)
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} ({self.ip_address})"

class SwitchMetric(models.Model):
    switch = models.ForeignKey(Switch, on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.IntegerField()
    memory_usage = models.IntegerField()
    temperature = models.IntegerField()
    bandwidth = models.IntegerField()
    interface_status = models.IntegerField()
    crc_errors = models.IntegerField()
    reliability = models.CharField(max_length=10)
    tx_rate = models.IntegerField()
    rx_rate = models.IntegerField()
    anomalies = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-timestamp']
    
    def __str__(self):
        return f"{self.switch} - {self.timestamp} - CPU: {self.cpu_usage}%"