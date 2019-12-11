import time
import json
from LED import LEDStrip
from dht_sensor import DHTSensor
from adc_sensor import ADCSensor
from config import Config
import global_settings as gs

gs.init()
led = LEDStrip(gs.led_pin)
dht = DHTSensor(gs.dht_pin)
adc = ADCSensor({0: 'light', 2: 'soil'})
runtime_settings = {
    'update_interval': 30
}


# --- Setup MQTT Subscribes ---
def led_on_message(message):
    #print("message received ", str(message.payload.decode("utf-8")))
    value = int(message.payload)
    led.fade(value)


def conf_on_message(message):
    data = json.loads(message.payload.decode("utf-8"))
    runtime_settings.update(data)
    save_settings()


gs.mqtt.subscribe('/control/' + str(Config.ID) + '/led', led_on_message)
gs.mqtt.subscribe('/conf/' + str(Config.ID), conf_on_message)
# --- Setup MQTT Subscribes ---


# Generate Sensor-data message
def gen_json_message(name, value):
    data = {
        'id': Config.ID,
        'timestamp': round(time.time()),
        'name': name,
        'value': value
    }
    return json.dumps(data)


# Convert light data to percent and invert value. Consider calibration values
def convert_light_value(value):
    percent = round((value - gs.light_max) * 100 / (gs.light_min - gs.light_max))
    return percent * -1 + 100


# Convert soil data to percent and invert value. Consider calibration values
def convert_soil_value(value):
    percent = round((value - gs.soil_max) * 100 / (gs.soil_min - gs.soil_max))
    return percent * -1 + 100


# Load runtime settings
def load_settings():
    global runtime_settings
    with open('config.json') as json_data_file:
        runtime_settings = json.load(json_data_file)


# Save runtime settings
def save_settings():
    global runtime_settings
    with open('config.json', 'w') as outfile:
        json.dump(runtime_settings, outfile)

