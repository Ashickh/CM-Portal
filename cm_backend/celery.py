# celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

from celery.schedules import crontab
from django.conf import settings

# from app.invoice_management.tasks import create_invoice_object

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cm_backend.settings')

app = Celery('cm_backend')

app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django app configs.

app.autodiscover_tasks(lambda:settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'generate_bills' : {
    'task' : 'generate_bills',
    'schedule' : crontab(minute='*/5')
    },
    'send_payment_alert_email' : {
    'task' : 'send_payment_alert_email',
    'schedule' : crontab(minute='*/5')
    },
    'send_payment_alert_sms' : {
    'task' : 'send_payment_alert_sms',
    'schedule' : crontab(minute='*/5')
    },
}

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
