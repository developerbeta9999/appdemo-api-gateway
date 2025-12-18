import json
import os
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': os.environ.get('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092'),
    'client.id': 'api-gateway-producer'
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f'❌ Error Kafka: {err}')
    else:
        print(f'✅ Enviado a: {msg.topic()}')

def publish(topic, method, body):
    # Estructura estándar del mensaje
    data = {
        'method': method,
        'body': body
    }
    json_data = json.dumps(data).encode('utf-8')
    producer.produce(topic, json_data, callback=delivery_report)
    producer.flush() # Forzamos envío inmediato para pruebas
