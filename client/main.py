from input_manager import InputManager, InputThread
from screen_manager import ScreenManager, ScreenThread
from button_manager import ButtonManager
import boto3
import requests
import re

# URL for Poem Server
poem_server = 'http://poembox-dev.us-west-2.elasticbeanstalk.com'
# Create an SNS client
client = boto3.client(
    "sns",
    aws_access_key_id="AKIAIFNKKMPWNMOPPMUQ",
    aws_secret_access_key="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",
    region_name="us-east-1"
)

inputs = InputManager('/dev/ttyACM0', 9600)
inputs.add_input('16', ['sonnet', 'free', 'haiku'], 'form', 1024)
inputs.add_input('15', ['happy', 'sad', 'indifferent'], 'tone', 1024)
inputs.add_input('14', ['love', 'war', 'environment', 'education', 'history'], 'topic', 1024)

button = ButtonManager(go_pin=18, reset_pin=23, go_ahead_light=12, stop_light=17, reset_time=0)
screen = ScreenManager()
# Create new threads
thread1 = InputThread(1, "Input Manager Thread", 1, inputs)
#thread2 = ScreenThread(2, "Screen Manager Thread", ScreenManager())

# Start new Threads
thread1.start()
#thread2.start()

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
            screen.notify_sent(False)
        else:
            readings = thread1.get_readings()
            r = requests.get(poem_server + '/poem', params=readings)
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
            client.publish(
                PhoneNumber=clean_number,
                Message=message
            )
            screen.notify_sent(True)

    # Button reset!
    elif check == 2:
        screen.reset()

