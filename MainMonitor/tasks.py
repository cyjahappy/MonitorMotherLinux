# 用于定义使用Celery框架实现的定时任务和分布式任务
# 部署的时候要改端口!!!!!!!
from celery import shared_task
from .send_request import send_get_request_to_all_child_servers
from .server_info_alert import server_info_get_error_alert
from .html_performance_alert import html_performance_result_get_error_alert
from .iperf_alert import iperf_result_get_error
from django_celery_results.models import TaskResult


@shared_task
def check_server_info():
    """
    发送指令使所有子服务器获取并检测系统各项指标
    """
    server_error_list = send_get_request_to_all_child_servers('/monitor/server-info-to-db')
    if len(server_error_list) != 0:
        server_info_get_error_alert(server_error_list)


@shared_task
def html_performance_test():
    """
    发送指令使所有子服务器进行前端性能测试
    """
    server_error_list = send_get_request_to_all_child_servers('/monitor/html-performance-test-results-to-db')
    if len(server_error_list) != 0:
        html_performance_result_get_error_alert(server_error_list)


@shared_task
def iperf_test():
    """
    发送指令使所有子服务器相互进行iPerf3测试
    """
    server_error_list = send_get_request_to_all_child_servers('/monitor/iperf3-test-results-to-db')
    if len(server_error_list) != 0:
        iperf_result_get_error(server_error_list)


@shared_task
def ping_test():
    """
    发送指令使所有子服务器相互进行Ping测试
    """
    send_get_request_to_all_child_servers('/monitor/ping-results-to-db')


@shared_task
def clean_child_database():
    """
    发送指令使所有子服务器清理数据库中过期数据
    """
    send_get_request_to_all_child_servers('/monitor/clean-database-api')


@shared_task
def clean_celery_log_database():
    """
    清理母服务器自身Celery存储日志的数据表
    """
    TaskResult.objects.all().delete()
