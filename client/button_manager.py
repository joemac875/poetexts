import RPi.GPIO as GPIO
import time

class ButtonManager():
    def __init__(self, go_pin, reset_pin, go_ahead_light, stop_light, reset_time):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        print ("Button Manager Created!")
        self.go_pin = go_pin
        self.reset_pin = reset_pin
        self.button_reset = reset_time
        self.pressed = False
        self.stop_light = stop_light
        self.go_ahead_light = go_ahead_light
        self.time_since_trigger = time.time()
        GPIO.setup(self.reset_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.go_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.go_ahead_light,GPIO.OUT)
        GPIO.setup(self.stop_light,GPIO.OUT)
        

    def check(self):
        go = GPIO.input(self.go_pin)
        reset = GPIO.input(self.reset_pin)
        if go == False:
            if self.pressed == False:
                if time.time() - self.time_since_trigger > self.button_reset:
                    #print('Button Pressed')
                    GPIO.output(self.go_ahead_light, GPIO.LOW)
                    GPIO.output(self.stop_light, GPIO.HIGH)
                    self.time_since_trigger = time.time()
                    self.pressed = True
                    return 1
        if reset == False:
            if time.time() - self.time_since_trigger > self.button_reset:
                GPIO.output(self.go_ahead_light, GPIO.HIGH)
                GPIO.output(self.stop_light, GPIO.LOW)
            if self.pressed == True:
                #print('Button Reset')
                self.pressed = False
                return 2
        return 0







        

