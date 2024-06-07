import threading
import paho.mqtt.client as mqtt
import json
import random
import datetime

# MQTT settings
mqtt_broker_host = 'localhost'
mqtt_broker_port = 1883
mqtt_topic = 'data_topic'
mqtt_username = 'admin'
mqtt_password = 'admin'

# Stock symbols
stock_symbol_list = {
    "AAPL": "Apple",
    "MOEX": "Московская биржа",
    "GOOG": "Google Alphabet",
    "GAZP": "Газпром",
    "SBER": "Сбер",
    "LKOH": "Лукойл",
    "OZON": "OZON",
    "RUAL": "Русал",
    "TCSG": "Тинькофф"
}

def publish_messages():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_username, password=mqtt_password)
    client.connect(mqtt_broker_host, mqtt_broker_port)

    while True:
        ticker = random.choice(list(stock_symbol_list.keys()))
        company = stock_symbol_list[ticker]
        price = random.randint(120, 450)
        now = datetime.datetime.now()
        message_time = now.strftime("%H:%M:%S")
        data = {
            'company': company,
            'ticker': ticker,
            'price': price,
            'time': message_time
        }
        client.publish(mqtt_topic, json.dumps(data))
        print(f"Sent data: {data}")
        # Adjust sleep time as needed
        threading.Event().wait(random.randint(1, 5)) 

def start_publisher_thread():
    publisher_thread = threading.Thread(target=publish_messages)
    publisher_thread.start()

if __name__ == '__main__':
    start_publisher_thread()
