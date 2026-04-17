from kafka import KafkaProducer
import time

producer = KafkaProducer(bootstrap_servers='localhost:9092')

for i in range(5):
    message = f"message {i}"
    producer.send('test-topic', message.encode('utf-8'))
    print(f"sent: {message}")
    time.sleep(1)

producer.flush()