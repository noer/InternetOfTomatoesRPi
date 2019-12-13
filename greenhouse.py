import time
import global_settings as gs
import functions as fn
from config import Config

fn.load_settings()

while True:
    if Config.enable_dht:
        try:
            for name, value in fn.dht.read().items():
                gs.mqtt.publish('/sensor/air', fn.gen_json_message(name, value))
        except RuntimeError as error:
            pass

    if Config.enable_adc:
        adc_data = fn.adc.read_all()
        for name, value in adc_data.items():
            if name == 'light':
                value = fn.convert_light_value(value)
            if name == 'soil':
                value = fn.convert_soil_value(value)
            gs.mqtt.publish('/sensor/'+name, fn.gen_json_message(name, value))

    time.sleep(int(fn.runtime_settings['update_interval']))

