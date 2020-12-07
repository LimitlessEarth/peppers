import Adafruit_DHT
import time
import busio
from board import SCL, SDA
from adafruit_seesaw.seesaw import Seesaw
from .si1145 import SI1145

class Sensors:
    def __init__(self):
        self.light_sensor = SI1145()
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.ss = Seesaw(self.i2c_bus, addr=0x36)

    def get_light_info(self):
        vis = self.light_sensor.readVisible()
        IR = self.light_sensor.readIR()
        UV = self.light_sensor.readUV()
        uvIndex = UV / 100.0
        print('Vis:             ' + str(vis))
        print('IR:              ' + str(IR))
        print('UV Index:        ' + str(uvIndex))

    def get_air_info(self):
        humidity, temperature = Adafruit_DHT.read_retry(11, 17)
        print("humidity:", humidity, " temp:",  temperature)

    def get_soil_info(self):
        # read moisture level through capacitive touch pad
        touch = self.ss.moisture_read()

        # read temperature from the temperature sensor
        temp = self.ss.get_temp()

        print("moisture: " + str(touch)+ " temp: " + str(temp))
