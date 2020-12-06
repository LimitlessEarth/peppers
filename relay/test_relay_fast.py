#!/usr/bin/python

import relay_ft245r
import sys
import time

rb = relay_ft245r.FT245R()
dev_list = rb.list_dev()

# list of FT245R devices are returned
if len(dev_list) == 0:
    print('No FT245R devices found')
    sys.exit()

# Show their serial numbers
for dev in dev_list:
    print(dev.serial_number)

# Pick the first one for simplicity
dev = dev_list[0]
print('Using device with serial number ' + str(dev.serial_number))

rb.connect(dev)

for i in range(1,9):
    print(i)
    rb.switchon(i)
    time.sleep(0.05)


for i in range(1,9):
    print(i)
    rb.switchoff(i)
    time.sleep(0.05)


