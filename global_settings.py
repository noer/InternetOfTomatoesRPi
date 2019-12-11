from config import Config
from mqtt import MQTT


def init():
    global mqtt
    mqtt = MQTT(Config.mqtt_user, Config.mqtt_pass)


light_min = 240
light_max = 50
soil_min = 255
soil_max = 100

led_pin = 17
dht_pin = 13
