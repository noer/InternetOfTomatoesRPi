import PCF8591 as ADC
import RPi.GPIO as GPIO

class ADCSensor:
    def __init__(self, sensor_names):
        self.sensors = sensor_names
        ADC.setup(0x48)

    def read_all(self):
        data = {}
        for k, v in self.sensors.items():
            #data[k]['name'] = v
            data[v] = ADC.read(k)
            #data[i]['name'] = self.sensors[i]
            #data[i]['value'] = ADC.read(i)
        return data
