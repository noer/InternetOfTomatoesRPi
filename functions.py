import time
import json
from config import Config
import global_settings as gs
from mqtt import MQTT

mqtt = MQTT(Config.mqtt_user, Config.mqtt_pass)

def led_on_message(message):
    print("message received ", str(message.payload.decode("utf-8")))
    value = int(message.payload)
    gs.led.fade(value)


def gen_json_message(name, value):
    data = {
        'id': Config.ID,
        'timestamp': round(time.time()),
        'name': name,
        'value': value
    }
    return json.dumps(data)


# Convert to percent and invert value
def convert_light_value(value):
    percent = round((value - gs.light_max) * 100 / (gs.light_min - gs.light_max))
    return percent * -1 + 100


def convert_soil_value(value):
    percent = round((value - gs.soil_max) * 100 / (gs.soil_min - gs.soil_max))
    return percent * -1 + 100
