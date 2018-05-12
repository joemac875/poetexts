from input_manager import InputManager
import time

inputs = InputManager('/dev/cu.usbmodem1421', 9600)

while True:
    time.sleep(.1)
    inputs.add_input('16', ['Iambic', 'Anapestic', 'Pyrrhic', 'Dimeter', 'Trimeter', 'Spondee'], 1024)
    inputs.add_input('15', ['short','long'], 1024)
    inputs.add_input('14', ['sad','happy','morbid', 'heartwarming'], 1024)

    print(inputs.get_inputs())
