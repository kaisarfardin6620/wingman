from __future__ import absolute_import, unicode_literals
import os
from pathlib import Path
from dotenv import load_dotenv
from celery import Celery

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(os.path.join(BASE_DIR, '.env'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'wingman.settings')

app = Celery('wingman')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
