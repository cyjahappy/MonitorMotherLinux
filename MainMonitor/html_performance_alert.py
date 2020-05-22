def html_performance_alert(html_performance_problematic_source_ip, html_performance_problematic_target_url_dict):
    """
    接收前端性能测试中不达标的URL信息, 生成报警邮件的内容
    :param iperf3_problematic_source_ip:
    :param iperf3_problematic_target_server_dict:
    :return:
    """
    html_performance_problematic_target_server_ip = list(html_performance_problematic_target_url_dict.keys())
    html_performance_problematic_test_results = list(html_performance_problematic_target_url_dict.values())
    print(html_performance_problematic_target_server_ip)
    print(html_performance_problematic_test_results)


def html_performance_result_get_error_alert(server_error_list):
    """
    接收无法获取前端性能检测结果的子服务器IP地址列表, 生成警报邮件内容
    :param server_error_list:
    :return:
    """
    print(server_error_list, '无法获取前端性能检测结果')
