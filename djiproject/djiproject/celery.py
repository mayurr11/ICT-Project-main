from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# 设置 Django 的默认设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djiproject.settings')

app = Celery('djiproject')

# 从 Django 的 settings.py 配置中加载配置
app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动发现任务文件
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')