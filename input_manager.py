import serial
import time
ser = serial.Serial('/dev/cu.usbmodem1421',9600)

#Potentiometer range
POT_RANGE = 1024

class InputManager():
    def __init__(self, connection, baud_rate):
        self.ser = serial.Serial(connection, baud_rate)
        self.inputs = {}
        self.separator = "/"

    def read_raw_inputs(self):
        # Read in all the info waiting in the serial connection
        serial_content = ser.read(ser.inWaiting())
        try:
            split_content = serial_content.split('\n')
            # Get the second to last set of values sent from Arduino
            raw_info = split_content[-2].rstrip('/\r')
            # Split the raw information into sensor and reading pairs
            raw_pairs = raw_info.split(self.separator)
            input_dict = {}
            for pair in raw_pairs:
                pair_split = pair.split()
                input_dict[pair_split[0]] = pair_split[1]
            return input_dict
        except Exception as e:
            print(e)
            return None

    def add_input(self, pin_number, features, reading_range):
        self.inputs[pin_number] = Input(features, reading_range)

    def get_inputs(self):
        inputs = []
        raw = self.read_raw_inputs()
        try:
            for key in raw:
                reading = raw[key]
                inputs.append(self.inputs[key].select_feature(reading))
            return inputs
        except Exception as e:
            print(e)
            return None

class Input():
    def __init__(self, features, reading_range):
        self.features = features
        self.reading_range = reading_range
        self.features_len = len(features)

    def select_feature(self, reading):
        # I need to map this to smaller values and choose a feature
        index = int(float(reading) * self.features_len / self.reading_range)
        return self.features[index]










