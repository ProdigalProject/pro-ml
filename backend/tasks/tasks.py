from celery import Celery 

app = Celery('tasks', broker='amqp://pdg:pdg@localhost/%2fprodigal')  

@app.task 
def add(x, y): 
    return x + y
