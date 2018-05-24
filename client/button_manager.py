import RPi.GPIO as GPIO
import time
import simpleaudio as sa

class ButtonManager():
    '''
    Handles the input of a two buttons and corresponding LEDS
    '''
    def __init__(self, go_pin, reset_pin, go_ahead_light, stop_light, reset_time, go_sound, reset_sound):
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
        GPIO.setup(self.go_ahead_light, GPIO.OUT)
        GPIO.setup(self.stop_light, GPIO.OUT)
        # Create sounds
        self.go_sound = sa.WaveObject.from_wave_file(go_sound)
        self.reset_sound = sa.WaveObject.from_wave_file(reset_sound)

    def check(self):
        '''
        :return:
            0 - The go pin hasn't been activated and hasn't been reset
            1 - The go pin has just been activated
            2 - The  reset pin has just been activated
        '''
        go = GPIO.input(self.go_pin)
        reset = GPIO.input(self.reset_pin)
        if go == False:
            if self.pressed == False:
                if time.time() - self.time_since_trigger > self.button_reset:
                    # print('Button Pressed')
                    GPIO.output(self.go_ahead_light, GPIO.LOW)
                    GPIO.output(self.stop_light, GPIO.HIGH)
                    self.time_since_trigger = time.time()
                    play_obj = self.go_sound.play()
                    #play_obj.wait_done()
                    self.pressed = True
                    return 1
        if reset == False:
            if time.time() - self.time_since_trigger > self.button_reset:
                GPIO.output(self.go_ahead_light, GPIO.HIGH)
                GPIO.output(self.stop_light, GPIO.LOW)
            if self.pressed == True:
                # print('Button Reset')
                play_obj = self.reset_sound.play()
                play_obj.wait_done()
                self.pressed = False
                return 2
        return 0

    def flash_leds(self, pin, repeat_number, frequency):
        '''
        Flash LEDs
        '''
        state = GPIO.input(pin)
        for x in range(0, repeat_number):
            GPIO.output(pin, GPIO.HIGH)
            time.sleep(frequency)
            GPIO.output(pin, GPIO.LOW)
            time.sleep(frequency)
            
        if state:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)
