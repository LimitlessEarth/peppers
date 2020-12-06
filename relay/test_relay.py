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

# Connect and turn on relay 2 and 4, and turn off
rb.connect(dev)
rb.switchon(1)    
time.sleep(0.5)
rb.switchon(2)
time.sleep(0.5)
rb.switchon(3)    
time.sleep(0.5)
rb.switchon(4)    
time.sleep(0.5)
rb.switchon(5)    
time.sleep(0.5)
rb.switchon(6)    
time.sleep(0.5)
rb.switchon(7)    
time.sleep(0.5)
rb.switchon(8)    
time.sleep(0.5)



rb.switchoff(1)    
time.sleep(0.5)
rb.switchoff(2)
rb.switchoff(3)    
time.sleep(0.5)
rb.switchoff(4)    
time.sleep(0.5)
rb.switchoff(5)    
time.sleep(0.5)
rb.switchoff(6)    
time.sleep(0.5)
rb.switchoff(7)    
time.sleep(0.5)
rb.switchoff(8)    
