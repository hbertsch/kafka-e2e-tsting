# Kafka Producer and Consumer Project

[toc]

## Introduction and Purpose of the Project

This project demonstrates a simple messaging system using **Apache Kafka**. The goal is to showcase how a **Kafka producer** can continuously send messages to a topic, while different types of **Kafka consumers** listen to and process these messages in distinct ways. This project features three distinct consumers:

- **consumer_from_oldest**: Consumes messages from the earliest (oldest) offset in the Kafka topic.
- **consumer_from_newest**: Consumes messages from the latest (newest) offset in the Kafka topic.
- **consumer_batch_message**: Consumes messages in batches rather than one by one, showcasing Kafka’s ability to process messages more efficiently under certain workloads.

This project aims to help developers understand how different configurations can affect consumer behavior when working with Kafka topics and messages.

## How to Set Up

### Prerequisites

- Docker
- Docker Compose
- Bash shell (or equivalent)
- Python
- Poetry (for Python dependency management)

Make sure you have these tools installed and properly configured on your system before proceeding.

### Project Structure Overview

The project is divided into the following components:

- **Producer**: Sends continuous messages to a Kafka topic.
- **Consumers**: Three different types of consumers, each behaving differently based on their configuration.
- **Docker Compose**: Manages the Kafka broker, Zookeeper, and all services (producer and consumers) through a multi-container setup.

### Installing Dependencies

1. Clone the repository:

   ```shell
   git clone <repository-url>
   cd <repository-folder>
   ```

2. Install the Python dependencies using **Poetry**. Run the following command in the project directory where the `pyproject.toml` file is located:

   ```shell
   poetry install
   ```

   This will create a virtual environment and install all the required dependencies specified in the `pyproject.toml` and `poetry.lock` files, including `kafka-python`.

## How to Run

1. Build and start all services using Docker Compose. You can choose between two different bash scripts:

   - For a regular build:

     ```shell
     ./buildAndRun.sh
     ```

   - For a build without cache (useful if you’ve changed any Docker-related configurations):

     ```shell
     ./buildAndRun_nocache.sh
     ```

   These scripts will:

   - Start Zookeeper and Kafka services.
   - Build and run the Kafka producer and all three Kafka consumers.

2. Once all the services are up and running, the producer will start sending messages to the Kafka topic (`test-topic`), and each consumer will begin consuming messages according to its configuration.

## What We See in the Test

As the test runs, each consumer will behave differently depending on its configuration. The **sample_consumer.log** shows the behavior of each consumer:

- **consumer_from_oldest**: This consumer starts processing messages from the beginning of the Kafka topic (oldest offset). It ensures that no messages are missed, even if the consumer starts after the producer has already sent messages.
- **consumer_from_newest**: This consumer only processes new messages that are sent after it has started. It ignores any historical data, focusing on real-time processing.
- **consumer_batch_message**: This consumer processes messages in batches. Instead of handling one message at a time, it waits until there are enough messages to process a batch, which can be more efficient for certain workloads.

### Observing Consumer Behavior

By checking the logs, you'll see how these consumers handle message consumption differently. The `sample_consumer.log` showcases examples where:

- The **consumer_from_oldest** processes the full history of the Kafka topic, ensuring all messages from the beginning are handled.
- The **consumer_from_newest** skips over older messages and immediately starts processing only the new ones.
- The **consumer_batch_message** processes messages in bulk, providing faster processing times under certain conditions.

This allows you to observe how each consumer type can be tailored to specific use cases.

### Sample Consumer Log Output

Here's an excerpt from the `sample_consumer.log` that highlights the differences:

```shell
consumer_from_oldest    | Received: {'current_time': '2024-09-26 14:41:24'}
consumer_from_oldest    | Received: {'current_time': '2024-09-26 14:41:35'}
consumer_from_oldest    | Received: {'current_time': '2024-09-26 14:41:36'}
consumer_from_oldest    | Received: {'current_time': '2024-09-26 14:41:37'}
consumer_from_oldest    | Received: {'current_time': '2024-09-26 14:41:38'}
kafka-producer          | Sent: {'current_time': '2024-09-26 14:41:39'}
consumer_from_newest    | Received: {'current_time': '2024-09-26 14:41:39'}
consumer_from_oldest    | Received: {'current_time': '2024-09-26 14:41:39'}
kafka-producer          | Sent: {'current_time': '2024-09-26 14:41:40'}
consumer_from_oldest    | Received: {'current_time': '2024-09-26 14:41:40'}
consumer_from_newest    | Received: {'current_time': '2024-09-26 14:41:40'}
kafka-producer          | Sent: {'current_time': '2024-09-26 14:41:41'}
consumer_from_newest    | Received: {'current_time': '2024-09-26 14:41:41'}
consumer_from_oldest    | Received: {'current_time': '2024-09-26 14:41:41'}
kafka                   | [2024-09-26 14:41:41,741] INFO [GroupCoordinator 1]: Member kafka-python-2.0.2-424131e3-fcd1-4a48-af30-a77675b960c6 in group 3a6f1e04-f26a-4429-9786-3d596c123c04 has failed, removing it from the group (kafka.coordinator.group.GroupCoordinator)
kafka                   | [2024-09-26 14:41:41,742] INFO [GroupCoordinator 1]: Preparing to rebalance group 3a6f1e04-f26a-4429-9786-3d596c123c04 in state PreparingRebalance with old generation 1 (__consumer_offsets-43) (reason: removing member kafka-python-2.0.2-424131e3-fcd1-4a48-af30-a77675b960c6 on heartbeat expiration) (kafka.coordinator.group.GroupCoordinator)
kafka                   | [2024-09-26 14:41:41,742] INFO [GroupCoordinator 1]: Group 3a6f1e04-f26a-4429-9786-3d596c123c04 with generation 2 is now empty (__consumer_offsets-43) (kafka.coordinator.group.GroupCoordinator)
kafka                   | [2024-09-26 14:41:41,743] INFO [GroupCoordinator 1]: Member kafka-python-2.0.2-b300bf78-6421-4763-ad13-42ee7d93b1d3 in group 9d5115f5-6642-497d-9bde-d869131715ca has failed, removing it from the group (kafka.coordinator.group.GroupCoordinator)
kafka                   | [2024-09-26 14:41:41,743] INFO [GroupCoordinator 1]: Preparing to rebalance group 9d5115f5-6642-497d-9bde-d869131715ca in state PreparingRebalance with old generation 1 (__consumer_offsets-1) (reason: removing member kafka-python-2.0.2-b300bf78-6421-4763-ad13-42ee7d93b1d3 on heartbeat expiration) (kafka.coordinator.group.GroupCoordinator)
kafka                   | [2024-09-26 14:41:41,743] INFO [GroupCoordinator 1]: Group 9d5115f5-6642-497d-9bde-d869131715ca with generation 2 is now empty (__consumer_offsets-1) (kafka.coordinator.group.GroupCoordinator)
kafka-producer          | Sent: {'current_time': '2024-09-26 14:41:42'}
```

This log output demonstrates how each consumer processes messages differently, depending on their configuration.

## Configuring Consumers

Kafka consumers can be customized in various ways depending on the needs of the application. In this project, the consumers are differentiated by their starting offset and batch processing behavior:

1. **Starting Offset Configuration**:
   - `earliest`: Start consuming messages from the earliest offset (historical data).
   - `latest`: Start consuming messages only from the latest offset (new data).
2. **Batch Processing**:
   - Consumers can be configured to process messages in batches, which improves throughput for high-traffic scenarios. This is controlled by adjusting the batch size and the time to wait before processing the batch.

### How to Configure

The consumers in this project are configured via their Dockerfiles and Python scripts. If you want to change the behavior, you can modify the following settings:

- **consumer_from_oldest**:
  - Dockerfile: `consumer_fromOldest.dockerfile`
  - Script: `consumer_fromOldest.py`
  - Configuration: This consumer is set to start from the earliest offset.
- **consumer_from_newest**:
  - Dockerfile: `consumer_fromNewest.dockerfile`
  - Script: `consumer_fromNewest.py`
  - Configuration: This consumer starts from the latest offset.
- **consumer_batch_message**:
  - Dockerfile: `consumer_batchMessage.dockerfile`
  - Script: `consumer_batchMessage.py`
  - Configuration: This consumer is configured to process messages in batches.

These configurations are reflected in the `docker-compose.yml` file, which defines the behavior of each consumer.