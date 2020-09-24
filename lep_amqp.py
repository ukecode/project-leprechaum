# example_publisher.py
import pika, os, logging
logging.basicConfig()

class lep_amqp:
    def __init__(self,url_amqp, queue):
        self.params = pika.URLParameters(url_amqp)
        self.params.socket_timeout = 5
        self.queue = queue
    
    def start_connection(self):
        self.connection = pika.BlockingConnection(self.params)
        self.channel = self.connection.channel() 
        self.channel.queue_declare(queue=self.queue) 

    def send_message(self, message, queue):
        self.channel.basic_publish(exchange='', routing_key=queue, body=message)
    
    def close_connection(self):
        self.connection.close()
    
    def send_one(self, message, queue):
        self.start_connection()
        self.send_message(message, queue)
        self.close_connection()