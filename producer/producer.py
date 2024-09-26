import os
from datetime import datetime
import time
import json
from kafka import KafkaProducer
from kafka.errors import NoBrokersAvailable, KafkaError

# Get Kafka broker and topic from environment variables
KAFKA_BROKER = os.environ.get('KAFKA_BROKER', 'localhost:9092')
TOPIC = os.environ.get('TOPIC', 'test-topic')

print(f"Kafka broker: {KAFKA_BROKER}")
print(f"Topic: {TOPIC}")

def create_kafka_producer():
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers=KAFKA_BROKER,
                value_serializer=lambda v: json.dumps(v).encode('utf-8'),
                api_version='auto',
                request_timeout_ms=5000,
                retries=5,
                retry_backoff_ms=1000,
            )
            # Force metadata update
            partitions = producer.partitions_for(TOPIC)
            if partitions is not None:
                print("Connected to Kafka broker.")
                return producer
            else:
                print("Kafka broker not available. Retrying in 5 seconds...")
                time.sleep(5)
        except NoBrokersAvailable:
            print("Kafka broker not available. Retrying in 5 seconds...")
            time.sleep(5)
        except KafkaError as e:
            print(f"Kafka error during producer initialization: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"Unexpected error during producer initialization: {e}")
            time.sleep(5)

def main():
    # Initialize Kafka producer with robust connection checking
    producer = create_kafka_producer()

    while True:
        try:
            # Create a simple message with a counter
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            message = {'current_time': current_time}

            # Send message to Kafka topic
            producer.send(TOPIC, message)
            print(f"Sent: {message}")
            time.sleep(1)  # Wait for 1 second before sending the next message
        except KafkaError as e:
            print(f"Kafka error during message send: {e}")
            # Optionally, reinitialize the producer
            producer = create_kafka_producer()
        except Exception as e:
            print(f"Unexpected error during message send: {e}")
            # Optionally, reinitialize the producer
            producer = create_kafka_producer()

if __name__ == '__main__':
    main()
