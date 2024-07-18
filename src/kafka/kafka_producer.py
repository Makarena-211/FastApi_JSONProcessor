from confluent_kafka import Producer
import json 
import uuid

conf = {
    'bootstrap.servers': 'localhost:9092'
}

producer = Producer(**conf)

def delievery_report(err, msg):
    if err is not None:
        print(f"Message delievery failed {err}")
    else: 
        print(f"Message delievered to {msg.topic()} [{msg.partition()}]")

def sent_message(topic, value):
    producer.produce(topic, value=json.dumps(value), callback=delievery_report)
    producer.flush()