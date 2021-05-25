import adafruit_dht
import time
import busio
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw
import si1145
import RPi.GPIO as GPIO

DHT_PIN = 17
DHT_POWER_PIN = 27

class Sensors:
    def __init__(self, soil_sensors):
        self.light_sensor = si1145.SI1145()
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.soil_sensors = [Seesaw(self.i2c_bus, addr=x) for x in soil_sensors]
        self.dht_device = adafruit_dht.DHT22(DHT_PIN)

    def reset_dht(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(DHT_POWER_PIN, GPIO.OUT)
        GPIO.output(DHT_POWER_PIN, GPIO.LOW)
        time.sleep(1)
        GPIO.output(DHT_POWER_PIN, GPIO.HIGH)
        time.sleep(1)

    def get_light_info(self):
        try:
            vis = self.light_sensor.readVisible()
            IR = self.light_sensor.readIR()
            UV = self.light_sensor.readUV()
            uvIndex = UV / 100.0
        except:
            self.light_sensor = si1145.SI1145()
            print("D:")
        
        return vis, IR, uvIndex

    def get_air_info(self):
        temp = self.dht_device.temperature
        humidity = self.dht_device.humidity

        if humidity is not None:
            humidity = round(humidity, 3)

        if temp is not None:
            temp = round(temp, 3)

        return humidity, temp

    def get_soil_info(self, index):
        # read moisture level through capacitive touch pad
        moisture = self.soil_sensors[index].moisture_read()

        # read temperature from the temperature sensor
        temp = self.soil_sensors[index].get_temp()

        return moisture, temp

    def cleanup(self):
        GPIO.cleanup()
