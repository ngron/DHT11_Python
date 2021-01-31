# coding: UTF-8
import RPi.GPIO as GPIO
import dht11
import time
import datetime
import requests
import os

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 14
instance = dht11.DHT11(pin=14)

# LINE NotifyのAPI設定
url = "https://notify-api.line.me/api/notify"
token = os.environ["LINE_NOTIFY_TOKEN"]
headers = {"Authorization" : "Bearer "+ token}

MIN_TEMPERATURE = 18
MAX_TEMPERATURE = 22

def notify_to_line(message):
    payload = {
        "message": message,
        "notificationDisabled": False,
    }
    print(payload)
    res = requests.post(url, headers = headers, params = payload)
    print(res)

try:
    result = instance.read()
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        temperature = result.temperature
        humidity = result.humidity
        print("Temperature: %-3.1f C" % temperature)
        print("Humidity: %-3.1f %%" % humidity)
        print(temperature)
        print(humidity)
        if temperature > MAX_TEMPERATURE:
            print("暑いよーーー")
            message = f"暑いよーーー><\n温度: {temperature} ℃\n湿度: {humidity} %"
            notify_to_line(message)
            print(res)
        elif temperature < MIN_TEMPERATURE:
            print("寒いよーーー><")
            message = f"寒いよーーー><\n温度: {temperature} ℃\n湿度: {humidity} %"
            notify_to_line(message)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()