import os

from celery import Celery
from celery.schedules import crontab

from django.conf import settings

# 配置环境变量：
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'database_system.settings')

celery_app = Celery('database_system')

# 加载配置文件：
celery_app.config_from_object('django.conf:settings', namespace='CELERY')

# 自动检测任务：
celery_app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# 配置celery任务：
celery_app.conf.beat_schedule = {
    "random_instance_password_task":{
        "task": "celery_tasks.tasks.random_instance_password",
        "schedule":crontab(minute=0,hour="*/12") # 每个12小时跑一次
    },
    "daily-instance-stats_task":{
        "task": "celery_tasks.tasks.daily_instance_stats",
        "schedule":crontab(hour=0, minute=0) # 每天12点执行
    }
}