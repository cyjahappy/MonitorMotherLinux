from .models import ChildServerList


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


def bytes_to_dict(bytes_content):
    bytes_content_str = str(bytes_content, encoding="utf-8")
    bytes_content_dict = eval(bytes_content_str)
    return bytes_content_dict
