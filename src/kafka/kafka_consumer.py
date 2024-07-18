from confluent_kafka import Consumer, KafkaError

conf = {
    'bootstrap.servers':'localhost:9092',
    'group.id':'mygroup',
    'auto.offset.reset':'earliest'
}

def create_kafka_consumer():
    return Consumer(**conf)

def consume_messages(topic):
    consumer = create_kafka_consumer()
    consumer.subscribe([topic])

    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break
        print(f'Received message: {msg.value().decode("utf-8")}')