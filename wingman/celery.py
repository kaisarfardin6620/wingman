from __future__ import absolute_import, unicode_literals
import os
from pathlib import Path
from celery import Celery
from dotenv import load_dotenv
from celery.schedules import crontab

BASE_DIR = Path(__file__).resolve().parent.parent

env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wingman.settings')

app = Celery('wingman')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'check-reminders-every-minute': {
        'task': 'chat.tasks.check_reminders_task',
        'schedule': crontab(minute='*'),
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')