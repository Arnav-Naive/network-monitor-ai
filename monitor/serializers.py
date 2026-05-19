from rest_framework import serializers
from .models import SwitchMetric, Switch

class SwitchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Switch
        fields = ['id', 'name', 'ip_address', 'port', 'location', 'is_active']

class SwitchMetricSerializer(serializers.ModelSerializer):
    switch_name = serializers.CharField(source='switch.name', read_only=True)
    
    class Meta:
        model = SwitchMetric
        fields = [
            'id', 'switch_name', 'timestamp',
            'cpu_usage', 'memory_usage', 'temperature',
            'bandwidth', 'interface_status', 'crc_errors',
            'reliability', 'tx_rate', 'rx_rate', 'anomalies'
        ]