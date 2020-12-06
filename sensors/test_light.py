#!/usr/bin/python

import si1145

sensor = si1145.SI1145()

vis = sensor.readVisible()
IR = sensor.readIR()
UV = sensor.readUV()
uvIndex = UV / 100.0
print('Vis:             ' + str(vis))
print('IR:              ' + str(IR))
print('UV Index:        ' + str(uvIndex))
