#!/usr/bin/python
 
import time
import RPi.GPIO as GPIO
import Adafruit_DHT

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17
POWER_PIN = 27

def reset_sensor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(POWER_PIN, GPIO.OUT)
    GPIO.output(POWER_PIN, GPIO.LOW)
    time.sleep(2)
    GPIO.output(POWER_PIN, GPIO.HIGH)
    time.sleep(2)

if __name__ == '__main__':
    while True:
        try:
            humidity, temperature_c = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
            temperature_f = temperature_c * (9 / 5) + 32

            print(
                "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                    temperature_f, temperature_c, humidity
                )
            )
    
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            print("RuntimeError:", error.args[0])
            reset_sensor()
            time.sleep(2.0)
            continue
        except Exception as error:
            raise error
    
        time.sleep(2.0)