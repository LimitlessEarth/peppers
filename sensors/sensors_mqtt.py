#!/usr/bin/python

import sensors, time
import paho.mqtt.client as mqtt

MQTT_HOST = "localhost"
PORT = 1883
TIMEOUT = 10

SOIL_SENSORS = [0x36, 0x38]

s = sensors.Sensors(SOIL_SENSORS)

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

    while True:

        vis, ir, uv_index = s.get_light_info()
        humidity, air_temp = s.get_air_info()

        for i in range(0, len(SOIL_SENSORS)):
            moisture, soil_temp = s.get_soil_info(i)
            client.publish("peppers/sensors/soil/moisture/"+str(i), moisture)
            client.publish("peppers/sensors/soil/temp/"+str(i), soil_temp)

        client.publish("peppers/sensors/light/visual", vis)
        client.publish("peppers/sensors/light/ir", ir)
        client.publish("peppers/sensors/light/uv_index", uv_index)

        client.publish("peppers/sensors/air/humidity", humidity)
        client.publish("peppers/sensors/air/temp", air_temp)

        time.sleep(15)