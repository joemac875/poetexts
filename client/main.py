#! /usr/bin/env python3
from input_manager import InputManager, InputThread
from screen_manager import ScreenManager, ScreenThread
from button_manager import ButtonManager
from twilio.rest import Client
import boto3
import requests
import configparser
import re
import os
import configuration
import sys
# read in user configurations
user_config = configparser.ConfigParser()
user_config.read(os.path.join(os.getcwd(), '..') + '/server/pox.ini')

# URL for Poem Server
poem_server = configuration.get_server(user_config) 
print(poem_server)
# Create an Twilio client
twilio_client = Client(configuration.get_account_sid(user_config), configuration.get_auth_token(user_config))

inputs = InputManager('/dev/ttyACM0', 9600)

dials = configuration.get_dial_values(user_config)
dialPins = configuration.get_pins(user_config)

counter = 0
print(dialPins)
print(dials)

for dial in sorted(dials.items()):
    print(dial[0])
    inputs.add_input(dialPins[counter], list(dials[dial[0]]), dial[0], 1024)
    counter += 1

button = ButtonManager(go_pin=18, reset_pin=23, go_ahead_light=12, stop_light=17, reset_time=0, go_sound='/home/pi/pox/client/go.wav', reset_sound='/home/pi/pox/client/reset.wav')
screen = ScreenManager("Enter Phone #\nand Pull Lever")
# Create new threads
thread1 = InputThread(1, "Input Manager Thread", 1, inputs)
#thread2 = ScreenThread(2, "Screen Manager Thread", ScreenManager())

# Start new Threads
thread1.start()
#thread2.start()
if len(sys.argv) == 2 and sys.argv[1] == 'debug':
    while(1):
        print(thread1.get_readings())

while (1):
    check = button.check()
    # Button hasn't been pressed and hasn't been reset
    if check == 0:
        pass
    # BUtton pressed!
    elif check == 1:
        number = screen.get_message()
        clean_number = '+1' + re.sub("[^0-9]", "", number)
        print(clean_number)
        if len(clean_number) != 12:
            screen.clear_and_write("Unusable Phone #")
            button.flash_leds(button.stop_light, 5, .05)
        else:
            readings = thread1.get_readings()
            try:
                r = requests.get(poem_server + '/poem', params=readings)
            except:
                screen.clear_and_write("Couldn't Connect\nTo Poem Server")
                button.flash_leds(button.stop_light, 5, .05)
                continue
            if r.status_code != 200:
               screen.clear_and_write("Bad Request Made")
               button.flash_leds(button.stop_light, 5, .05)
               continue
            if r.headers['Content-Type'] != 'application/json':
                print(r.text)
                screen.clear_and_write("Failure to\nFetch Poem")
                button.flash_leds(button.stop_light, 5, .05)
                continue
                
            poem_json = r.json()
            matches = set(readings.items()) & set(poem_json.items())

            # Craft the message
            message = ''
            message += poem_json['title']
            message += '\n'
            message += 'by ' + poem_json['author']
            message += '\n'
            message += 'tags: '
            for attribute, tag in matches:
                message += tag + ' '
            message += '\n============\n'
            message += poem_json['text']

            # Send your sms message.
            try:
                message_response = twilio_client.messages.create(to=clean_number, from_="+15173431475", body=message)
                status_code = message_response.error_code
                if status_code is None:
                    screen.clear_and_write("Message Sent")
                    button.flash_leds(button.go_ahead_light, 5, .05)
                else:
                    screen.clear_and_write("Twilio Error\n" + str(status_code))
                    button.flash_leds(button.stop_light, 5, .05)
            except:
                screen.clear_and_write("Publish Error!")



            

    # Button reset!
    elif check == 2:
        
        screen.clear_and_write("Enter Phone #\nand Pull Lever")
        

