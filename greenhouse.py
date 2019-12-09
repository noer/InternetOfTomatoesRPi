from dht_sensor import DHTSensor
from adc_sensor import ADCSensor
import time
import functions as fn

fn.mqtt.subscribe('/control/led', fn.led_on_message)

dht = DHTSensor(13)
adc = ADCSensor({0: 'light', 2: 'soil'})
while True:
    try:
        for name, value in dht.read().items():
            fn.mqtt.publish('/sensor/air', fn.gen_json_message(name, value))
    except RuntimeError as error:
        pass
    adc_data = adc.read_all()
    for name, value in adc_data.items():
        if name == 'light':
            value = fn.convert_light_value(value)
        if name == 'soil':
            value = fn.convert_soil_value(value)
        fn.mqtt.publish('/sensor/'+name, fn.gen_json_message(name, value))
    time.sleep(30.0)

