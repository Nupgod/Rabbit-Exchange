# Stock Exchange Simulation using MQTT and RabbitMQ

This project simulates a stock exchange system using the publisher/subscriber pattern with the MQTT protocol. The system employs RabbitMQ as the message broker, which is deployed using Docker Compose. The project includes both a publisher that generates and sends stock data and a subscriber that receives and processes this data.

## Features

- **Publisher/Subscriber Pattern**: Implements the publisher/subscriber pattern to simulate real-time stock exchange data flow.
- **MQTT Protocol**: Utilizes the MQTT protocol for efficient message communication.
- **RabbitMQ Broker**: Uses RabbitMQ as the message broker, supporting both MQTT and AMQP protocols.
- **Dockerized Setup**: Easy deployment with Docker Compose.
- **Flask Web Interface**: Displays the received stock data in a user-friendly web interface.

## Project Structure

- **Publisher**: Generates random stock data and publishes it to the MQTT broker.
- **Subscriber**: Subscribes to the MQTT broker, processes incoming data, and updates the web interface.
- **Flask Application**: Hosts a web server to display real-time stock data.
- **Docker Compose**: Configures and runs the RabbitMQ broker.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Setup

1. **Clone the repository**:
    ```sh
    git clone https://github.com/yourusername/stock-exchange-simulation.git
    cd stock-exchange-simulation
    ```

2. **RabbitMQ Configuration**:
    - Create a `config` directory with `rabbitmq.conf` and `advanced.config` files.
    - Create a `login.env` file in the `config` directory with your RabbitMQ credentials.

3. **Run Docker Compose**:
    ```sh
    docker-compose up -d
    ```

4. **Start the Publisher**:
    ```sh
    python MQTT_Pub.py
    ```

5. **Start the Subscriber**:
    ```sh
    python MQTT_Sub.py
    ```

### RabbitMQ Management Interface

Access the RabbitMQ management interface at [http://localhost:8080](http://localhost:8080) using the credentials specified in your `login.env` file.

### Flask Web Interface

Access the Flask web interface at [http://localhost:5001](http://localhost:5001) to view real-time stock data.
