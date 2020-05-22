from __future__ import absolute_import, unicode_literals
import os
from celery import Celery, platforms

# 获取settings.py的配置信息
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MonitorMotherLinux.settings')

# 定义Celery对象, 并将项目配置信息加载到对象中
# 定义Celery的参数
app = Celery('MonitorMotherLinux')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# 允许root 用户运行celery
platforms.C_FORCE_ROOT = True


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
