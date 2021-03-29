#!/usr/bin/python

import relay_ft245r, time
import paho.mqtt.client as mqtt
import logging, sys

MQTT_HOST = "localhost"
PORT = 1883
TIMEOUT = 10
RELAY_COUNT = 8

rb = relay_ft245r.FT245R()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("Connected with result code "+str(rc))
    sys.stdout.flush()

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("peppers/relay/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    relay_num = int(msg.topic.split('/')[-1])
    if int(msg.payload) == 0:
        rb.switchoff(relay_num)
    else:
        rb.switchon(relay_num)

    time.sleep(0.01)

    client.publish("peppers/relays/state/"+str(relay_num), rb.getstatus(relay_num))

def on_publish(client,userdata,result):             #create function for callback
    pass

def connect_to_device():
    global rb
    rb = relay_ft245r.FT245R()
    dev_list = rb.list_dev()

    # list of FT245R devices are returned
    if len(dev_list) == 0:
        print('No FT245R devices found')
        sys.stdout.flush()
        return False

    # Show their serial numbers
    for dev in dev_list:
        print("Device:", dev.serial_number)
        sys.stdout.flush()

    # Pick the first one for simplicity
    dev = dev_list[0]
    print('Using device with serial number ' + str(dev.serial_number))

    rb.connect(dev)

    return True

def update_all_status(client):
    for relay_num in range(1,RELAY_COUNT+1):
        client.publish("peppers/relays/state/"+str(relay_num), rb.getstatus(relay_num))


if __name__ == '__main__':
    client = mqtt.Client()

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish 

    client.connect(MQTT_HOST, PORT, TIMEOUT)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    while True:
        try:
            success = connect_to_device()
            if not success:
                logging.error("Failed to  connect to usb device")
                time.sleep(1)
                continue
            else:
                update_all_status(client)
            client.loop_forever()
        except Exception as ex:
            logging.error("There was an exception: " + str(ex))
            sys.stdout.flush()
            try:
                rb.disconnect()
            except:
                pass
            time.sleep(1)