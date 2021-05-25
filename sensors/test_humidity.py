#!/usr/bin/python
 
import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# 
DHT_PIN = 17
POWER_PIN = 27

GPIO.setmode(GPIO.BCM)
GPIO.setup(POWER_PIN, GPIO.OUT)
GPIO.output(POWER_PIN, GPIO.LOW)
time.sleep(2)
GPIO.output(POWER_PIN, GPIO.HIGH)
time.sleep(2)
 
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(DHT_PIN)
#dhtDevice = adafruit_dht.DHT22(board.D11, use_pulseio=False)

# you can pass DHT22 use_pulseio=False if you wouldn't like to use pulseio.
# This may be necessary on a Linux single board computer like the Raspberry Pi,
# but it will not work in CircuitPython.
# dhtDevice = adafruit_dht.DHT22(board.D18, use_pulseio=False)
 
while True:
    try:
        # Print the values to the serial port
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        )
 
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print("RuntimeError:", error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error
 
    time.sleep(2.0)