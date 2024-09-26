import os
import time
import json
import uuid
from kafka import KafkaConsumer, TopicPartition
from kafka.errors import NoBrokersAvailable, KafkaError

# Get Kafka broker and topic from environment variables
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'localhost:9093')
TOPIC = os.environ.get('TOPIC', 'test-topic')

print(f"Kafka broker: {KAFKA_BROKER}")
print(f"Topic: {TOPIC}")

def create_kafka_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                bootstrap_servers=KAFKA_BROKER,
                auto_offset_reset='latest',
                enable_auto_commit=True,
                group_id=str(uuid.uuid4()),  # Unique group_id for independent consumption
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                api_version='auto',
                request_timeout_ms=40000,
                fetch_min_bytes=1000,      # Increase batch size to 16KB
                fetch_max_wait_ms=30000,    # this condition is requred since the default is 500ms
                                            # the consumer would still consume long before min_bytes is reached
            )
            # Check if the topic exists
            topics = consumer.topics()
            if TOPIC in topics:
                consumer.subscribe([TOPIC])
                print("Connected to Kafka broker and subscribed to topic.")
                return consumer
            else:
                print("Topic not available. Retrying in 5 seconds...")
                consumer.close()
                time.sleep(5)
        except NoBrokersAvailable:
            print("Kafka broker not available. Retrying in 5 seconds...")
            time.sleep(5)
        except KafkaError as e:
            print(f"Kafka error during consumer initialization: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error during consumer initialization: {e}")
            time.sleep(5)

def main():
    print("Starting consumer...")
    # Initialize Kafka consumer with robust connection checking
    consumer = create_kafka_consumer()
    
    while True:
        try:
            for message in consumer:
                # Access the message value and verify it
                data = message.value
                print(f"Received: {data}")
        except KafkaError as e:
            print(f"Kafka error during message consumption: {e}")
            consumer.close()
            consumer = create_kafka_consumer()
        except Exception as e:
            print(f"Unexpected error during message consumption: {e}")
            consumer.close()
            consumer = create_kafka_consumer()

if __name__ == '__main__':
    main()
