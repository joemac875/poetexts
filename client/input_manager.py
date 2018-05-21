import serial
import time
import threading


class InputManager():
    def __init__(self, connection, baud_rate):
        self.ser = serial.Serial(connection, baud_rate)
        self.inputs = {}
        self.separator = "/"

    def read_raw_inputs(self):
        # Read in all the info waiting in the serial connection
        serial_content = self.ser.read(self.ser.inWaiting())
        # print(serial_content)
        try:
            serial_content = serial_content.decode()
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

    def add_input(self, pin_number, features, label, reading_range):
        self.inputs[pin_number] = Input(features, label, reading_range)

    def get_inputs(self):
        inputs = {}
        raw = self.read_raw_inputs()
        try:
            for key in raw:
                reading = raw[key]
                param, value = self.inputs[key].select_feature(reading)
                inputs[param] = value
            return inputs
        except Exception as e:
            print(e)
            return None


class Input():
    def __init__(self, features, label, reading_range):
        self.features = features
        self.label = label
        self.reading_range = reading_range
        self.features_len = len(features)

    def select_feature(self, reading):
        # I need to map this to smaller values and choose a feature
        index = int(float(reading) * self.features_len / self.reading_range)
        return self.label, self.features[index]


class InputThread(threading.Thread):
    def __init__(self, threadID, name, counter, inputs):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.inputs = inputs
        self.counter = counter
        self.input_readings = {}

    def run(self):
        print ("Starting " + self.name)
        self.continuous_read()
        print ("Exiting " + self.name)

    def continuous_read(self):
        while True:
            time.sleep(.1)
            # print (self.inputs.get_inputs())
            self.input_readings = self.inputs.get_inputs()

    def get_readings(self):
        return self.input_readings
