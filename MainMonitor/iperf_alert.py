def iperf_alert(iperf3_problematic_source_ip, iperf3_problematic_target_server_dict):
    """
    接收iPerf3测试中不达标的服务器信息, 生成报警邮件的内容
    :param iperf3_problematic_source_ip:
    :param iperf3_problematic_target_server_dict:
    :return:
    """
    iperf3_problematic_target_server_ip = list(iperf3_problematic_target_server_dict.keys())
    iperf3_problematic_test_results = list(iperf3_problematic_target_server_dict.values())
    print(iperf3_problematic_target_server_ip)
    print(iperf3_problematic_test_results)


def iperf_result_get_error(server_error_list):
    """
    获取无法获取iPerf3检测结果的服务器IP地址列表, 生成报警邮件内容
    :param server_error_list:
    :return:
    """
    print(server_error_list, '无法获取iPerf3检测结果')
