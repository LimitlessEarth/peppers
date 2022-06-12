# Automation for Peppers

**IF ANYONE ELSE BESIDES ME IS INTERESTED IN THIS PROJECT PLEASE CONTACT ME**

I have only included rough information about this project. If you are interested in direct reconstructions, etc. I am happy to help, but until there is interest I am not going to document it for now.

## What?
Peppers is a collection of tools, services, etc. that make for automation and remote viewing of pepper plants using a specific set of devices.

## Software
- Lots of python
- Node-RED
- MQTT
- A bit of BASH
- ffmpeg

## Parts
- Raspberry Pi 4
- Pi Cam 2
- [FT245r USB relay](https://www.sainsmart.com/products/8-channel-12v-usb-relay-module)
    - I made an outlet box to house this relay and make the power plugs accessible.
    - 3d printing model available in the models dir.
- [AM2302 also known as a DHT22 temperature and humidity sensor](https://www.adafruit.com/product/393)
- [SI1145 light sensor](https://www.adafruit.com/product/1777)
- [Adafruit STEMMA Soil Sensor](https://www.adafruit.com/product/4026)

## Directories
### models
Contains the 3d models for a box to contain the ft245r relay, which you would then wire into standard square outlets.

### relay
Contains code related to the control of the ft245r usb relay.
There are tests for the relay as well as a device library and an MQTT daemon. 

### sensors
Contains code related to the reading and testing of the AM2302, SI1145 and STEMMA soil sensors.
There are tests for individual sensors, a library, and an MQTT daemon.

### services
Contains service files for the relay and sensors.

### webcam
Contains a script to be called by Node-RED that generates a still image from the Pi Cam 2. Additionally, if there are 10 images present, it will encode the images into an mp4 timelapse. 
