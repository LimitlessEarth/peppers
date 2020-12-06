#!/usr/bin/python
import Adafruit_DHT

humidity, temperature = Adafruit_DHT.read_retry(11, 17)
print("humidity:", humidity, " temp:",  temperature)
