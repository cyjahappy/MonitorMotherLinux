from django.contrib import admin
from django.urls import path
from MainMonitor import views
from MainMonitor.models import ChildServerList

urlpatterns = [
    path('admin/', admin.site.urls),
    path('server-info-threshold-api', views.ServerInfoThresholdList.as_view()),
    path('server-info-threshold-update', views.server_info_threshold_update),
    path('dashboard/<server_ip>', views.dashboard),
    # 网址直接输入dashboard不带server ip的话, 会将server ip设置为ChildServerList表中的第一个
    path('dashboard', views.dashboard, {'server_ip': ChildServerList.objects.all()[:1][0].server_ip}),
    path('homepage', views.homepage),
    path('iperf-test-alert', views.GetIPerfTestAlertMessage.as_view()),
    path('html-performance-test-alert', views.GetHTMLPerformanceTestAlertMessage.as_view()),
    path('server-info-alert', views.GetServerInfoAlertMessage.as_view()),
    path('update-child-server-list', views.update_child_server_list),
]
