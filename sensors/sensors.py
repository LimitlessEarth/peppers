import Adafruit_DHT
import time
import busio
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw
import si1145

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 17

class Sensors:
    def __init__(self, soil_sensors):
        self.light_sensor = si1145.SI1145()
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.soil_sensors = [Seesaw(self.i2c_bus, addr=x) for x in soil_sensors]

    def get_light_info(self):
        vis = self.light_sensor.readVisible()
        IR = self.light_sensor.readIR()
        UV = self.light_sensor.readUV()
        uvIndex = UV / 100.0
        
        return vis, IR, uvIndex

    def get_air_info(self):
        humidity, temp = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

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
