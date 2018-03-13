# Celery tasks

from celery import Celery 
app = Celery('hello', broker='amqp://pdg:pdg@localhost/%2fprodigal')

@app.task 
def hello(): 
    return 'hello world'
