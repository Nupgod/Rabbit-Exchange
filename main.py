# from machine import I2C, Pin
# from time import sleep
# from pico_i2c_lcd import I2cLcd
# import random

# stock_symbol_list = {
#     "AAPL": "Apple",
#     "MOEX": "Moscow exchange",
#     "GOOG": "Google Alphabet",
#     "GAZP": "Gazprom",
#     "SBER": "SBER",
#     "LKOH": "Lukoil",
#     "OZON": "OZON",
#     "RUAL": "Rusal",
#     "TCSG": "Tinkoff"
# }
# messages = {}

# # Define GPIO pins
# RED = 17
# GREEN = 16
# YELLOW = 15

# # PCF8574 on 0x50
# I2C_ADDR = 0x27     # DEC 39, HEX 0x27
# NUM_ROWS = 2
# NUM_COLS = 16

# # define custom I2C interface, default is 'I2C(0)'
# # check the docs of your device for further details and pin infos
# i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
# lcd = I2cLcd(i2c, I2C_ADDR, NUM_ROWS, NUM_COLS)

# # Set up the GPIO pins
# red_led = Pin(RED, Pin.OUT)
# green_led = Pin(GREEN, Pin.OUT)
# yellow_led = Pin(YELLOW, Pin.OUT)

# while True:
#     ticker = random.choice(list(stock_symbol_list.keys()))
#     company = stock_symbol_list[ticker]
#     new_price = random.randint(120, 450)
#     change = 0.0
#     if ticker in messages:
#         old_price = messages[ticker]['price']
#         change = ((new_price - old_price) / old_price) * 100
#     messages[ticker] = {'price': new_price, 'change': change, 'company': company}

#     # Set up the LCD display
#     lcd.clear()
#     lcd.putstr(messages[ticker]['company'])
#     lcd.move_to(1, 1)
#     lcd.putstr(ticker + " : " + str(new_price))
#     # Turn on the LED
#     if change > 0:
#         green_led.value(1)
#         yellow_led.value(0)
#         red_led.value(0)
#     elif change < 0:
#         yellow_led.value(0)
#         green_led.value(0)
#         red_led.value(1)
#     else:
#         yellow_led.value(1)
#         green_led.value(0)
#         red_led.value(0)
#     sleep(3)

import network
from machine import I2C, Pin
from pico_i2c_lcd import I2cLcd
from umqtt.simple import MQTTClient
from time import sleep
import json

# Wi-Fi settings
ssid = 'WIFI NAME'
password = 'WIFI PASSWORD'

# MQTT settings
mqtt_broker_host = 'host.wokwi.internal'
mqtt_broker_port = 1883
mqtt_topic = 'data_topic'
mqtt_username = 'pika'
mqtt_password = ''

# Define GPIO pins
GREEN = 16
RED = 17

# PCF8574 on 0x50
I2C_ADDR = 0x27
NUM_ROWS = 2
NUM_COLS = 16

# Define custom I2C interface, default is 'I2C(0)'
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, NUM_ROWS, NUM_COLS)

# Set up the GPIO pins
green_led = Pin(GREEN, Pin.OUT)
red_led = Pin(RED, Pin.OUT)

# Handle incoming messages
def on_message(topic, msg):
    print('Received message:', msg)
    data = json.loads(msg)
    ticker = data['ticker']
    price = data['price']
    change = data['change']
    company = data['company']
    
    # Set up the LCD display
    lcd.clear()
    lcd.putstr(messages[ticker]['company'])
    lcd.move_to(1, 1)
    lcd.putstr(ticker + " : " + str(new_price))
    # Turn on the LED
    if change > 0:
        green_led.value(1)
        yellow_led.value(0)
        red_led.value(0)
    elif change < 0:
        yellow_led.value(0)
        green_led.value(0)
        red_led.value(1)
    else:
        yellow_led.value(1)
        green_led.value(0)
        red_led.value(0)

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    print()
    wlan.connect(ssid, password)
    print('Connecting to WiFi...', end='')
    while not wlan.isconnected():
        print('.', end='')
        sleep(1)
    print('\nConnected to WiFi')
    print(wlan.ifconfig())

# Connect to RabbitMQ
def connect_mqtt():
    client = MQTTClient(client_id="pico", server=mqtt_broker_host, port=mqtt_broker_port, user=mqtt_username, password=mqtt_password)
    client.set_callback(on_message)
    client.connect()
    client.subscribe(mqtt_topic)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_broker_host, mqtt_topic))
    return client

# Main loop
def main():
    connect_wifi()
    client = connect_mqtt()
    try:
        while True:
            client.wait_msg()
    except KeyboardInterrupt:
        client.disconnect()
        print('Disconnected from MQTT broker')

if __name__ == '__main__':
    main()
