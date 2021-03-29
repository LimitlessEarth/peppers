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

# API:
#     Relay name + timing or trigger CRUD
#     Relay on/off
#     Fan timing or triggers CRUD

import random
import time
import logging
import json
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, request
from flask_restplus import Api, Resource
from prometheus_client import start_http_server, Summary, Gauge, Counter
import relay.relay_ft245r as relay 
import sensors.sensors as sensors

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('peppers_request_processing_seconds', 'Time spent processing request')

VISIBLE_GAUGE = Gauge('peppers_visible_lux', 'Visible light lux')
INFRARED_GAUGE = Gauge('peppers_infrared_lux', 'Infrared light lux')
UV_INDEX_GAUGE = Gauge('peppers_uv_index', 'Ultraviolet index')

HUMIDITY_GAUGE = Gauge('peppers_air_humidity_percentage', 'Air humidity percentage')
AIR_TEMP_GAUGE = Gauge('peppers_air_temperature_celcius', 'Air temperature incelcius')
SOIL_MOISTURE_GAUGE = Gauge('peppers_soil_mosture_number', 'Soild moisture number')
SOIL_TEMP_GAUGE = Gauge('peppers_soil_temperature_celcius', 'Soild temperature in celcius')

RELAY_STATUS_GUAGE = Gauge('peppers_relay_status', 'Status of the labeled relay switch on/off', ['relay_name'])
RELAY_ON_TIME_COUNTER = Counter('peppers_relay_on_ms', 'Total time a relay switch is on', ['relay_name'])

relay_names = ['re_pump', 'airator', 'lights', 'stir_pump', 'relay_5', 'relay_6', 'relay_7', 'relay_8']

executor = ThreadPoolExecutor(1)

r = relay.FT245R()
s = sensors.Sensors()
r.init()

flask_app = Flask(__name__)
app = Api(app=flask_app)

# first parameter will be used as the url after our base url
# second parameter will be used as the title name in your swagger documentation
ns = app.namespace('peppers', description='Environmental control API')

@ns.route("/relay/<int:index>")
class PeppersRelay(Resource):

    @REQUEST_TIME.time()
    def get(self, index):  # will be used to see one particular log detail
        return {
            "state": str(r.getstatus(index+1)),
            "name": relay_names[index]
        }

    @REQUEST_TIME.time()
    def post(self, index):  # will be used to see one particular log detail
        state = r.getstatus(index + 1)
        if state == 1:
            r.switchoff(index + 1)
        else:
            r.switchon(index + 1)
        return {
            "state": str(r.getstatus(index+1)),
            "name": relay_names[index]
        }

    @REQUEST_TIME.time()
    @app.doc(responses={200: 'OK', 422: 'Unprocessable Entity', 500: 'Internal Server Error'},
            params={'id': 'Log id we will update'})
    def put(self, index):  # will be used to update particular log
        return {
            "status": "Updated log with id " + str(index)
        }

    @REQUEST_TIME.time()
    def delete(self, index):  # will be used to delete particular log
        return {
            "status": "Deleted log with id " + str(index)
        }


@ns.route("/relay")
class Peppers(Resource):

    @REQUEST_TIME.time()
    def get(self):  # will be used to see one particular log detail
        payload = {
            "relays": []
        }

        for index in range(0,8):
            payload['relays'].append({
                "state": str(r.getstatus(index+1)),
                "name": relay_names[index]
            })

        return payload

def monitor():
        while True:
            vis, IR, UV = s.get_light_info()
            VISIBLE_GAUGE.set(vis)
            INFRARED_GAUGE.set(IR)
            UV_INDEX_GAUGE.set(UV)

            humidity, air_temp = s.get_air_info()
            HUMIDITY_GAUGE.set(humidity)
            AIR_TEMP_GAUGE.set(air_temp)

            soil_moisture, soil_temp = s.get_soil_info()
            SOIL_MOISTURE_GAUGE.set(soil_moisture)
            SOIL_TEMP_GAUGE.set(soil_temp)

            # d = {'visible_light': vis, 'infrared_light': IR, 'uv_inex': UV, 'air_humidity': humidity, 'air_temp': air_temp, 'soil_moisture': soil_moisture, 'soil_temp': soil_temp}

            logging.info('measurement taken')
            print('measurement taken')

            for i in range(1, 9):
                RELAY_STATUS_GUAGE.labels(relay_name=relay_names[i-1]).set(r.getstatus(i))
            
            time.sleep(15)

def read_relays_file(path):
    with open(path) as f:
        data = json.load(f)

    return data

def update_relay_file(path, payload):
    with open(path, 'w') as json_file:
        json.dump(payload, json_file)

if __name__ == '__main__':
    print('Starting thing')

    logging.basicConfig(level = logging.INFO)

    # Start up the server to expose the metrics.
    start_http_server(19000)

    p = Peppers()

    executor.submit(monitor)
    flask_app.run(host= '0.0.0.0', port=19001, debug=False)