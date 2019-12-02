import json
from config import Config
from dht_sensor import DHTSensor
from adc_sensor import ADCSensor
from LED import LEDStrip
import time
from mqtt import MQTT

ID = Config.ID
led = LEDStrip(17)


def led_on_message(message):
    print("message received ", str(message.payload.decode("utf-8")))
    value = int(message.payload)
    led.fade(value)


def gen_json_message(name, value):
    global ID
    data = {
        'id': ID,
        'timestamp': round(time.time()),
        'name': name,
        'value': value
    }
    return json.dumps(data)


mqtt = MQTT(Config.mqtt_user, Config.mqtt_pass)
mqtt.subscribe('/control/led', led_on_message)

dht = DHTSensor(13)
adc = ADCSensor({0: 'light', 2: 'soil'})
while True:
    try:
        for name, value in dht.read().items():
            mqtt.publish('/sensor/air', gen_json_message(name, value))
    except RuntimeError as error:
        pass
    adc_data = adc.read_all()
    for name, value in adc_data.items():
        mqtt.publish('/sensor/'+name, gen_json_message(name, value))
    time.sleep(30.0)

