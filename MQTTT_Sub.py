import threading
import paho.mqtt.client as mqtt
import json
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Dict to store received messages
messages = {}

# MQTT settings
mqtt_broker_host = 'localhost'
mqtt_broker_port = 1883
mqtt_topic = 'data_topic'
mqtt_username = 'admin'
mqtt_password = 'admin'

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
        client.subscribe(mqtt_topic)
    else:
        print("Failed to connect to MQTT Broker. Return Code: " + str(rc))

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    print(f"Received data: {data}")
    ticker = data['ticker']
    new_price = data['price']
    time = data['time']
    company = data['company']
    if ticker in messages:
        old_price = messages[ticker]['price']
        change = ((new_price - old_price) / old_price) * 100
        messages[ticker] = {'price': new_price, 'change': change, 'time': time, 'company': company}
    else:
        messages[ticker] = {'price': new_price, 'change': 0.0, 'time': time, 'company': company}  # Initial change is 0%

def setup_mqtt_consumer():
    client = mqtt.Client()
    client.username_pw_set(username=mqtt_username, password=mqtt_password)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(mqtt_broker_host, mqtt_broker_port, 60)
    client.loop_forever()

# Start MQTT consumer in a separate thread
def start_consumer_thread():
    consumer_thread = threading.Thread(target=setup_mqtt_consumer)
    consumer_thread.start()

@app.route('/')
def index():
    return render_template('index.html', messages=messages)

if __name__ == '__main__':
    start_consumer_thread()
    app.run(host='localhost', port=5001)
