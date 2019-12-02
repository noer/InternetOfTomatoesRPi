from gpiozero import PWMLED
from time import sleep

class LEDStrip:
    def __init__(self, pin):
        self.led = PWMLED(17)

    def fade(self, fade_to):
        fade_from = int(round(self.led.value * 100))
        step = 1
        if fade_from > fade_to:
            step = -1
        for i in range(fade_from, fade_to, step):
            self.led.value = i/100.0
            sleep(0.05)

