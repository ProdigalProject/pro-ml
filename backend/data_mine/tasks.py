from __future__ import absolute_import 
from celery.decorators import task

@task(name="say_hello")
def hello(): 
    return "HELLO" 

hello.delay()
