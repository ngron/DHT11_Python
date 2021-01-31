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


try:
    while True:
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.datetime.now()))
            temperature = result.temperature
            humidity = result.humidity
            print("Temperature: %-3.1f C" % temperature)
            print("Humidity: %-3.1f %%" % humidity)
            # 温度が18℃未満なら「寒い」22℃以上なら「暑い」と通知する
            print(temperature)
            print(humidity)
            if False: #temperature > 22:
                print("暑いよーーー")
                message = f"暑いよーーー><\n温度: {temperature} ℃\n湿度: {humidity} %"
                print(res)
            elif True: #temperature < 22:
                print("寒いよーーー><")
                message = f"寒いよーーー><\n温度: {temperature} ℃\n湿度: {humidity} %"

            payload = {
                "message": message,
                "notificationDisabled": False
            }
            res = requests.post(url, headers = headers, params = payload)
            print(res)

        time.sleep(6)

except KeyboardInterrupt:
    print("Cleanup")
    GPIO.cleanup()