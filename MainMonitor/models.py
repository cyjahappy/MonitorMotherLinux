from django.db import models


class ServerInfoThreshold(models.Model):
    """
    存储系统各项阈值的数据
    """
    id = models.AutoField(primary_key=True)
    cpu_threshold = models.FloatField()
    memory_threshold = models.FloatField()
    disk_threshold = models.FloatField()
    bandwidth_threshold = models.FloatField()
    ping_threshold = models.FloatField(default=1)
    HTML_open_time_threshold = models.FloatField()
    backend_management_system_open_time_threshold = models.FloatField()
    microservices_exec_time_threshold = models.FloatField()
    tcp_sent_Mbps_threshold = models.FloatField(default=3)
    tcp_received_Mbps_threshold = models.FloatField(default=3)


class ChildServerList(models.Model):
    """
    存储子服务器的IP地址
    """
    server_ip = models.GenericIPAddressField(primary_key=True)
    server_name = models.CharField(max_length=20, null=True)
