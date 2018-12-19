# Poetexts

A system to text users poems that match desired tags. Combination of a RESTful API implemented in Python to serve poems and a physical client comprising a box, dials, Raspberry Pi, Arduino, LEDs, LCD screen, keypad, and speakers. The client box requests poems from the RESTful web service and then sends the poem to users over SMS using the Twilio API.

# Hardware

## Raspberry Pi

The Raspberry Pi is responsible for running a client that grabs poems from poem web service and sends them to users. It uses AWS SNS to send the text messages. 

It prompts users for telephone number inputs using a 16x2 LCD screen.

A DPDT switch connect to the Pi to tell it when to send a message and when to reset for another number. LEDS are also connected to the Pi that light up during these two states (one color can indicate the message is sending, and the other indicates that the Pi is ready to send again).

![Raspberry Pi Pin Diagram](https://image.ibb.co/cPApO8/RPi_Sketch_bb.png)

## Arduino

The Arduino is solely responsible for handling analog input. It is connected to a bunch of potentiometers that set the tag values the users want. **It must be connected to the Raspberry Pi using a USB cable.**

![Arduino Pin Diagram](https://image.ibb.co/fzNxAo/Arduino_Sketch_bb.png)


# Usage

1. Upload the Arduino sketch to an Arduino
2. Connect the Arduino to the Raspberry Pi with a USB cable
3. Deploy the poem web service 
4. Make sure the correct URL of the web service is in `main.py` of the client ( see the readme in client directory)
5. Make sure legal Twilio credentials are in `pox.ini` 
6. Run the client/main.py on the Raspberry Pi 

