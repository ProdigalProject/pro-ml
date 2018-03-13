from __future__ import absolute_import 
from celery import Celery 
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings') 

app = Celery('backend') 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks() 

@app.task(bind=True) 
def debug_task(x, y): 
    print("adding work...") 
