'''
@Author: zyh
@Date: 2020-07-09 10:34:28
@LastEditTime: 2020-07-13 14:08:31
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

# 签到的字典：
sign_in = {
    'tayeon': 'https://weibo.com/p/aj/general/button?ajwvr=6&api=http://i.huati.weibo.com/aj/super/checkin&texta=%E7%AD%BE%E5%88%B0&textb=%E5%B7%B2%E7%AD%BE%E5%88%B0&status=0&id=100808b943f0c7667000439af7ff3f7f33f531&location=page_100808_super_index&timezone=GMT+0800&lang=zh-cn&plat=Win32&ua=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/83.0.4103.116%20Safari/537.36%20Edg/83.0.478.61&screen=2048*1152&__rnd=1594619555420',
    'jessica': 'https://weibo.com/p/aj/general/button?ajwvr=6&api=http://i.huati.weibo.com/aj/super/checkin&texta=%E5%B7%B2%E7%AD%BE%E5%88%B0&textb=%E5%B7%B2%E7%AD%BE%E5%88%B0&status=1&id=1008082c2fa1b7274dc344e5a228ba0983f864&location=page_100808_super_index&timezone=GMT+0800&lang=zh-cn&plat=Win32&ua=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/83.0.4103.116%20Safari/537.36%20Edg/83.0.478.61&screen=2048*1152&__rnd=1594619491144',
    'yoona': 'https://weibo.com/p/aj/general/button?ajwvr=6&api=http://i.huati.weibo.com/aj/super/checkin&texta=%E7%AD%BE%E5%88%B0&textb=%E5%B7%B2%E7%AD%BE%E5%88%B0&status=0&id=1008080c5fb650788fe5c7577f0b6ec4a34038&location=page_100808_super_index&timezone=GMT+0800&lang=zh-cn&plat=Win32&ua=Mozilla/5.0%20(Windows%20NT%2010.0;%20Win64;%20x64)%20AppleWebKit/537.36%20(KHTML,%20like%20Gecko)%20Chrome/83.0.4103.116%20Safari/537.36%20Edg/83.0.478.61&screen=2048*1152&__rnd=1594619524722'
}

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.beat_schedule = {
    'task2': {
        'task': 'backend.tasks.crawl_images',
        'schedule': crontab(minute="0,30", hour='10-22')
    },
    'task3': {
        'task': 'backend.tasks.task3',
        'schedule': crontab(minute="*/5", hour='10-22')
    },
    'task4': {
        'task': 'backend.tasks.task4',
        'schedule': crontab(hour='14', minute='08'),
        'args': sign_in
    }
}
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
