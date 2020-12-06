#!/usr/bin/python

# Core:
# Take Measurements:
#     air humidity
#     air temp
#     soil humidity 
#     soil temp
#     UV + Light

# Take Pictures:
#     take piture
#     overlay texts
#     build and append video if enough images present

# Control via relay:
#     8 outlets
#         Water pump for plants
#         Airator to stir oxygen into the Water
#         Lights 
#         Stir pump?

# Control Fan:
#     12v Noctua 200mm

# Prometheus Metrics:
#     All sensor measurements
#     Fan on/off and speed
#     Outlets on/off
#     Amount of time outlet was on
#     Disk and system metrics
#     Image capture success/failure
#     Video generation success/failure
#     HTTP Metrics


import relay

r = relay.Relay()
r.init()

r.swtichon(1)
time.sleep(1.0)
r.switchoff(1)

