from django.shortcuts import render
from .models import ServerInfoThreshold, ChildServerList
from .serializers import ServerInfoThresholdSerializer
from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from ipware.ip import get_ip
from .iperf_alert import iperf_alert
from .html_performance_alert import html_performance_alert
from .server_info_alert import server_info_alert
from .update_child_server_threshold import update_child_server_threshold
from .send_request import send_get_request_to_server, send_post_request_to_server
from .general_function import get_child_server_ip_list
from numpy import mean


class ServerInfoThresholdList(generics.ListAPIView):
    """
    定义GET操作,返回JSON格式的服务器各项指标阈值
    """
    queryset = ServerInfoThreshold.objects.all()
    serializer_class = ServerInfoThresholdSerializer


class ServerInfoThresholdUpdate(generics.UpdateAPIView):
    """
    定义PUT操作,更新服务期各项指标阈值
    """
    queryset = ServerInfoThreshold.objects.all()
    serializer_class = ServerInfoThresholdSerializer
    update_child_server_threshold()


def homepage(request):
    """
    渲染首页
    :param request:
    :return:
    """
    # 系统各项指标信息的阈值
    server_info_threshold = ServerInfoThreshold.objects.get(id=1)
    server_info_threshold_data = {
        'cpu_threshold': server_info_threshold.cpu_threshold,
        'memory_threshold': server_info_threshold.memory_threshold,
        'disk_threshold': server_info_threshold.disk_threshold,
        'bandwidth_threshold': server_info_threshold.bandwidth_threshold,
        'ping_threshold': server_info_threshold.ping_threshold,
        'HTML_open_time_threshold': server_info_threshold.HTML_open_time_threshold,
        'backend_management_system_open_time_threshold': server_info_threshold.backend_management_system_open_time_threshold,
        'microservices_exec_time_threshold': server_info_threshold.microservices_exec_time_threshold,
        'tcp_sent_Mbps_threshold': server_info_threshold.tcp_sent_Mbps_threshold,
        'tcp_received_Mbps_threshold': server_info_threshold.tcp_received_Mbps_threshold,
    }
    return render(request, "Homepage.html", locals())


def dashboard(request, server_ip):
    """
    渲染Dashboard前端页面
    """
    child_server_ip_list = get_child_server_ip_list()
    # 该server_ip对应的主机的系统各项指标信息
    server_info = send_get_request_to_server(server_ip, '/monitor/server-info-minutes')
    # CRM首页前端性能测试结果(部署的时候要在这里更改URL地址)
    CRM_HTML_test_result = send_post_request_to_server(server_ip, '/monitor/html-performance-test-results-minutes',
                                                       {"url": "https://taobao.com"})
    # 后台管理系统前端性能测试结果(部署的时候要在这里更改URL地址)
    Management_System_HTML_test_result = send_post_request_to_server(server_ip, '/monitor/html-performance-test-results-minutes',
                                                                     {"url": "https://apple.com.cn"})
    # 该server_ip主机的server_list表
    server_list_response = send_get_request_to_server(server_ip, '/monitor/target-server-list')
    server_ip_list = []
    for server_list_instance in server_list_response:
        server_ip_list.append(server_list_instance['server_ip'])
    # 系统各项指标信息的阈值
    server_info_threshold = ServerInfoThreshold.objects.get(id=1)
    general_data = {
        'server_ip': server_ip,
        'server_ip_list': server_ip_list,
    }
    server_info_data = {
        'cpu': server_info['cpu'],
        'memory': server_info['memory'],
        'disk': server_info['disk'],
        'network': server_info['network'],
        'network_recv': server_info['network_recv'],
        'network_sent': server_info['network_sent'],
        'date': server_info['date'],
    }
    server_info_threshold_data = {
        'cpu_threshold': server_info_threshold.cpu_threshold,
        'memory_threshold': server_info_threshold.memory_threshold,
        'disk_threshold': server_info_threshold.disk_threshold,
        'bandwidth_threshold': server_info_threshold.bandwidth_threshold,
        'ping_threshold': server_info_threshold.ping_threshold,
        'HTML_open_time_threshold': server_info_threshold.HTML_open_time_threshold,
        'backend_management_system_open_time_threshold': server_info_threshold.backend_management_system_open_time_threshold,
        'microservices_exec_time_threshold': server_info_threshold.microservices_exec_time_threshold,
        'tcp_sent_Mbps_threshold': server_info_threshold.tcp_sent_Mbps_threshold,
        'tcp_received_Mbps_threshold': server_info_threshold.tcp_received_Mbps_threshold,
    }
    CRM_HTML_test_result_data = {
        'dns_query': CRM_HTML_test_result['dns_query'],
        'dns_query_mean': round(mean(CRM_HTML_test_result['dns_query']), 2),
        'tcp_connection': CRM_HTML_test_result['tcp_connection'],
        'tcp_connection_mean': round(mean(CRM_HTML_test_result['tcp_connection']), 2),
        'request': CRM_HTML_test_result['request'],
        'request_mean': round(mean(CRM_HTML_test_result['request']), 2),
        'dom_parse': CRM_HTML_test_result['dom_parse'],
        'dom_parse_mean': round(mean(CRM_HTML_test_result['dom_parse']), 2),
        'blank_screen': CRM_HTML_test_result['blank_screen'],
        'blank_screen_mean': round(mean(CRM_HTML_test_result['blank_screen']), 2),
        'dom_ready': CRM_HTML_test_result['dom_ready'],
        'dom_ready_mean': round(mean(CRM_HTML_test_result['dom_ready']), 2),
        'onload': CRM_HTML_test_result['onload'],
        'onload_mean': round(mean(CRM_HTML_test_result['onload']), 2),
        'date': CRM_HTML_test_result['date'],
    }
    Management_System_HTML_test_result_data = {
        'dns_query': Management_System_HTML_test_result['dns_query'],
        'dns_query_mean': round(mean(Management_System_HTML_test_result['dns_query']), 2),
        'tcp_connection': Management_System_HTML_test_result['tcp_connection'],
        'tcp_connection_mean': round(mean(Management_System_HTML_test_result['tcp_connection']), 2),
        'request': Management_System_HTML_test_result['request'],
        'request_mean': round(mean(Management_System_HTML_test_result['request']), 2),
        'dom_parse': Management_System_HTML_test_result['dom_parse'],
        'dom_parse_mean': round(mean(Management_System_HTML_test_result['dom_parse']), 2),
        'blank_screen': Management_System_HTML_test_result['blank_screen'],
        'blank_screen_mean': round(mean(Management_System_HTML_test_result['blank_screen']), 2),
        'dom_ready': Management_System_HTML_test_result['dom_ready'],
        'dom_ready_mean': round(mean(Management_System_HTML_test_result['dom_ready']), 2),
        'onload': Management_System_HTML_test_result['onload'],
        'onload_mean': round(mean(Management_System_HTML_test_result['onload']), 2),
        'date': Management_System_HTML_test_result['date'],
    }
    return render(request, 'Dashboard.html', locals())


class GetIPerfTestAlertMessage(APIView):
    """
    从子服务器中获取iPerf3检验结果不达标的IP地址列表
    """

    def post(self, request):
        iperf3_problematic_target_server_dict = dict(request.data)
        iperf3_problematic_source_ip = get_ip(request)
        iperf_alert(iperf3_problematic_source_ip, iperf3_problematic_target_server_dict)
        return Response(status.HTTP_200_OK)


class GetHTMLPerformanceTestAlertMessage(APIView):
    """
    从子服务器中获取前端性能检验结果不达标的URL列表
    """

    def post(self, request):
        html_performance_problematic_target_url_dict = dict(request.data)
        html_performance_problematic_source_ip = get_ip(request)
        html_performance_alert(html_performance_problematic_source_ip, html_performance_problematic_target_url_dict)
        return Response(status.HTTP_200_OK)


class GetServerInfoAlertMessage(APIView):
    """
    从子服务器中接收系统各项指标超过阈值的报警信息
    """

    def post(self, request):
        server_info_problematic_dict = dict(request.data)
        server_info_problematic_ip = get_ip(request)
        server_info_alert(server_info_problematic_ip, server_info_problematic_dict)
        return Response(status.HTTP_200_OK)
