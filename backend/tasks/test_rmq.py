import pika 

connection = pika.BlockingConnection(pika.URLParameters("amqp://pdg:pdg@localhost:5672/%2fprodigal"))
