import adafruit_dht

class DHTSensor:
    def __init__(self, pin):
        self.dhtDevice = adafruit_dht.DHT22(pin)

    def read(self):
        try:
            # Print the values to the serial port
            temperature_c = self.dhtDevice.temperature
            humidity = self.dhtDevice.humidity
            data = {'temperature': temperature_c, 'humidity': humidity}
            return data
            #return "Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity)

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            raise error
            #return error.args[0]
