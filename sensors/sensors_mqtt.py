#!/usr/bin/python

import os
import time
import datetime
import sensors, time
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
PORT = 1883
TIMEOUT = 10

MEASUREMENTS_FILE = '/home/pi/Peppers/webcam/measurements'
MEASUREMENTS_JSON_FILE = '/home/pi/Peppers/webcam/images/measurements.json'

SOIL_SENSORS = [0x36, 0x38]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("peppers/sensors/#")

def on_publish(client,userdata,result):             #create function for callback
    pass

if __name__ == '__main__':
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_publish = on_publish 

    client.connect(MQTT_HOST, PORT, TIMEOUT)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_start()

    s = sensors.Sensors(SOIL_SENSORS)

    while True:
        vis, ir, uv_index = s.get_light_info()
        try:
            humidity, air_temp = s.get_air_info()
        except Exception as e:
            print(e)
            s.reset_dht()
            time.sleep(0.5)
            humidity, air_temp = s.get_air_info()
        air_temp_f = ((air_temp * 9) / 5) + 32


        for i in range(0, len(SOIL_SENSORS)):
            soil_moisture, soil_temp = s.get_soil_info(i)
            client.publish("peppers/sensors/soil/moisture/"+str(i), soil_moisture)
            client.publish("peppers/sensors/soil/temp/"+str(i), soil_temp)

        soil_temp_f = ((soil_temp * 9) / 5) + 32

        client.publish("peppers/sensors/light/visual", vis)
        client.publish("peppers/sensors/light/ir", ir)
        client.publish("peppers/sensors/light/uv_index", uv_index)

        client.publish("peppers/sensors/air/humidity", humidity)
        client.publish("peppers/sensors/air/temp", air_temp)

        output = 'HUMIDITY=' + str(humidity) + "\nTEMPERATURE=" + str(air_temp_f) + "\nSOIL_MOISTURE=" + str(soil_moisture) + "\nVISIBLE_LIGHT=" + str(vis) + "\nINFRARED=" + str(ir) + "\nUV_INDEX=" + str(uv_index) + "\n"

        filename = '/home/pi/Peppers/webcam/measurements'
        filetemp = filename + '.tmp'
        f = open(filetemp, 'w')
        f.write(output)
        f.close()
        os.rename(filetemp, filename)

        dt = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


        output = "{\n \"timestamp\":\"" + dt + " MDT\",\n \"humidity\":" + str(humidity) + ",\n \"temp_c\":" + str(air_temp) + ",\n \"temp_f\":" + str(air_temp_f) + ",\n \"soil_moisture\":" + str(soil_moisture) +",\n \"soil_temp_c\":" + str(soil_temp) + ",\n \"soil_temp_f\":" + str(soil_temp_f) +  ",\n \"visible_light\":" + str(vis) + ",\n \"infrared\":" + str(ir) + ",\n \"uv_index\":" + str(uv_index) + "\n}\n"

        filename = '/home/pi/Peppers/webcam/images/measurements.json'
        filetemp = filename + '.tmp'
        f = open(filetemp, 'w')
        f.write(output)
        f.close()

        os.rename(filetemp, filename)

        time.sleep(15)