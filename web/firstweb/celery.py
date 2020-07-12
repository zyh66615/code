'''
@Author: zyh
@Date: 2020-07-09 10:34:28
@LastEditTime: 2020-07-12 20:11:14
@LastEditors: zyh
@Description: celery的设置（包括定时任务）
@FilePath: /web/firstweb/celery.py
'''
from __future__ import absolute_import, unicode_literals
from celery.schedules import crontab
import os

from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'firstweb.settings')

app = Celery('firstweb')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'task2': {
        'task': 'backend.tasks.crawl_images',
        'schedule': crontab(minute="0,20,40", hour='10-20')
    },
    'task3': {
        'task': 'backend.tasks.task3',
        'schedule': crontab(minute="*/2")
    }
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
