from input_manager import InputManager, InputThread
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
inputs.add_input('16', ['sonnet', 'free','haiku'], 'form',1024)
inputs.add_input('15', ['happy', 'sad','indifferent'], 'tone', 1024)
inputs.add_input('14', ['love', 'war', 'environment', 'education', 'history'], 'topic', 1024)

# Create new threads
thread1 = InputThread(1, "Input Manager Thread", 1, inputs)

# Start new Threads
thread1.start()




while(1):
    number = input("enter a phone number\n")

    clean_number = '+1' + re.sub("[^0-9]", "", number)
    readings = thread1.get_readings()
    print (readings, "\nSending a text to {}\n==============".format(clean_number))

    r = requests.get(poem_server+'/poem', params=readings)
    poem_json = r.json()
    matches = set(readings.items()) & set(poem_json.items())

    # Craft the message
    message = ''
    message += poem_json['title']
    message += '\n'
    message += 'by ' + poem_json['author']
    message += '\n'
    message += 'tags: '
    for attribute,tag in matches:
        message += tag + ' '
    message += '\n============\n'
    message += poem_json['text']

    # Send your sms message.
    client.publish(
        PhoneNumber=clean_number,
        Message=message
    )




