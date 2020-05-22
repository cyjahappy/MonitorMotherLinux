from rest_framework import serializers
from .models import ServerInfoThreshold


class ServerInfoThresholdSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServerInfoThreshold
        fields = (
            'cpu_threshold', 'memory_threshold', 'disk_threshold', 'bandwidth_threshold', 'HTML_open_time_threshold',
            'tcp_sent_Mbps_threshold', 'tcp_received_Mbps_threshold', 'microservices_exec_time_threshold',
            'backend_management_system_open_time_threshold', 'ping_threshold')