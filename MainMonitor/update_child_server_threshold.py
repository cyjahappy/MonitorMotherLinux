from .models import ServerInfoThreshold, ChildServerList
from .serializers import ServerInfoThresholdSerializer
import requests


# 部署的时候要改端口!!!!!!!

def update_child_server_threshold():
    """
    获取ServerInfoThreshold表中的阈值信息, 用以更新子服务器数据库中阈值表的信息
    :return:
    """

    server_info_threshold = ServerInfoThreshold.objects.get(pk=1)
    serializer = ServerInfoThresholdSerializer(server_info_threshold)
    server_ip_all_QuerySet = ChildServerList.objects.all()
    total_server_ip = server_ip_all_QuerySet.count()
    i = 0
    while i < total_server_ip:
        server_ip = server_ip_all_QuerySet[i].server_ip
        url = 'http://' + server_ip + '/monitor/server-info-threshold-update/1/'
        requests.put(url, data=serializer.data)
        i = i + 1
