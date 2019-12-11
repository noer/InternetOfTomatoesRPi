import paho.mqtt.client as client


class MQTT:
    subs = {}

    def __init__(self, user, password):
        self.mqtt = client.Client()
        self.mqtt.username_pw_set(username=user, password=password)
        self.mqtt.connect('mqtt.flespi.io')
        self.mqtt.on_message = self.on_message
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_disconnect = self.on_disconnect
        self.mqtt.loop_start()

    def publish(self, topic, message):
        self.mqtt.publish(topic, message)

    def subscribe(self, topic, callback):
        self.subs[topic] = callback
        self.mqtt.subscribe(topic)

    def on_message(self, client, userdata, message):
        for topic, cb in self.subs.items():
            if topic == message.topic:
                cb(message)

    def on_connect(self, client, userdata, flags, rc=0):
        if rc == 0:
            print('Connected to MQTT')
        else:
            print('Bad connection! Returned code '+str(rc))

    def on_disconnect(self, client, userdata, flags, rc=0):
        print('Disconnected from MQTT. Result code '+str(rc))
