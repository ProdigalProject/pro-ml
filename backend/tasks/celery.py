from __future__ import absolute_import 
from celery import Celery 
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings') 

app = Celery('backend') 
app.config_from_object('django.conf:settings', namespace='CELERY') 
app.autodiscover_tasks() 

@app.task(bind=True) 
def add(x, y): 
    print("adding work...") 
    return x + y
