#!/usr/bin/python3

import os
import Adafruit_DHT
import time
import busio
import board
import si1145
import datetime
from adafruit_seesaw.seesaw import Seesaw

# hardware interfaces for Soil and Light Sensor
i2c_bus = busio.I2C(board.SCL, board.SDA)
sensor = si1145.SI1145()

HUMIDITY_GPIO = 17
DHT_SENSOR = Adafruit_DHT.DHT22

# Humidity Sensor
humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, HUMIDITY_GPIO)
while humidity > 100:
  humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, HUMIDITY_GPIO)

tf = ((temperature * 9) / 5) + 32

# Soil Sensor
ss = Seesaw(i2c_bus, addr=0x36)
soil_moisture = ss.moisture_read()
soil_temp = int(ss.get_temp() * 100) / 100
stf = int((((soil_temp * 9) / 5) + 32) * 100) / 100

# Light Sensor
vis = sensor.readVisible()
IR = sensor.readIR()
UV = sensor.readUV()
uvIndex = UV / 100.0

output = 'HUMIDITY=' + str(humidity) + "\nTEMPERATURE=" + str(tf) + "\nSOIL_MOISTURE=" + str(soil_moisture) + "\nVISIBLE_LIGHT=" + str(vis) + "\nINFRARED=" + str(IR) + "\nUV_INDEX=" + str(uvIndex) + "\n"

filename = '/home/pi/Peppers/webcam/measurements'
filetemp = filename + '.tmp'
f = open(filetemp, 'w')
f.write(output)
f.close()
os.rename(filetemp, filename)

dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


output = "{\n \"timestamp\":\"" + dt + " MDT\",\n \"humidity\":" + str(humidity) + ",\n \"temp_c\":" + str(temperature) + ",\n \"temp_f\":" + str(tf) + ",\n \"soil_moisture\":" + str(soil_moisture) +",\n \"soil_temp_c\":" + str(soil_temp) + ",\n \"soil_temp_f\":" + str(stf) +  ",\n \"visible_light\":" + str(vis) + ",\n \"infrared\":" + str(IR) + ",\n \"uv_index\":" + str(uvIndex) + "\n}\n"

filename = '/home/pi/Peppers/webcam/images/measurements.json'
filetemp = filename + '.tmp'
f = open(filetemp, 'w')
f.write(output)
f.close()

os.rename(filetemp, filename)
