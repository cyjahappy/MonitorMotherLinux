import requests
from .models import ChildServerList
from .general_function import bytes_to_dict

server_ip_all = ChildServerList.objects.all()
total_server_ip = server_ip_all.count()


def send_get_request_to_all_child_servers(path):
    """
    向所有子服务器逐个发送http://[子服务器的IP]/path的GET请求
    :return:
    """
    server_error_list = []
    i = 0
    while i < total_server_ip:
        server_ip = server_ip_all[i].server_ip
        # 部署的时候记得改端口!!!!!!!!!!!!!!!!!!!!!!!!!!!
        url = 'http://' + server_ip + path
        response = requests.get(url)
        if response.status_code == 500:
            server_error_list.append(server_ip)
        i = i + 1
    return server_error_list


def send_get_request_to_server(server_ip, path):
    """
    发送http://[server_ip]/path的GET请求
    :param server_ip:
    :param path:
    :return Response from server:
    """
    url = 'http://' + server_ip + path
    response = requests.get(url)
    if type(response.content) is bytes:
        response_content_dict = bytes_to_dict(response.content)
        return response_content_dict
    return response.content


def send_post_request_to_server(server_ip, path, data):
    url = 'http://' + server_ip + path
    response = requests.post(url, data=data)
    if type(response.content) is bytes:
        response_content_dict = bytes_to_dict(response.content)
        return response_content_dict
    return response.content
