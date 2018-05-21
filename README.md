# pox

A poem box project that sends users a poem based on features they select using analog inputs on the box.

# Hardware

## Raspberry Pi

The Raspberry Pi is responsible for running a client that grabs poems from poem web service and sends them to users. It uses AWS SNS to send the text messages. 

It prompts users for telephone number inputs using a 16x2 LCD screen.

A DPDT switch connect to the Pi to tell it when to send a message and when to reset for another number. LEDS are also connected to the Pi that light up during these two states (one color can indicate the message is sending, and the other indicates that the Pi is ready to send again).

![Raspberry Pi Pin Diagram](https://image.ibb.co/cPApO8/RPi_Sketch_bb.png)

## Arduino

The Arduino is solely responsible for handling analog input. It is connected to a bunch of potentiometers that set the tag values the users want. **It must be connected to the Raspberry Pi using a USB cable.**

![Arduino Pin Diagram](https://image.ibb.co/fzNxAo/Arduino_Sketch_bb.png)




