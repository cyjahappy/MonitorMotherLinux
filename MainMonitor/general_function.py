from .models import ChildServerList, ServerInfoThreshold
import requests


def get_child_server_ip_list():
    """
    获取子服务器IP地址列表
    :return:
    """
    server_ip_list = []
    server_ip_all_QuerySet = ChildServerList.objects.all()
    total_server_ip = server_ip_all_QuerySet.count()
    i = 0
    while i < total_server_ip:
        server_ip_list.append(server_ip_all_QuerySet[i].server_ip)
        i = i + 1
    return server_ip_list


def update_child_server_ip_list():
    """
    将所有子服务器数据库中的服务器列表更新成与母服务器同步
    """
    server_ip_list = get_child_server_ip_list()
    for server_ip in server_ip_list:
        new_server_ip_list = server_ip_list
        new_server_ip_list.remove(server_ip)
        server_ip_list_dict = {
            "server_ip_list": new_server_ip_list
        }
        url = 'http://' + server_ip + '/monitor/update-server-list'
        requests.post(url, data=server_ip_list_dict)


def update_server_info_threshold(server_info_threshold_dict):
    """
    更新本服务器的数据库阈值表
    :return:
    """
    ServerInfoThreshold.objects.filter(id=1).update(**server_info_threshold_dict)
    pass


def bytes_to_dict(bytes_content):
    bytes_content_str = str(bytes_content, encoding="utf-8")
    bytes_content_dict = eval(bytes_content_str)
    return bytes_content_dict
