/*
 * Joe MacInnes 
 * May 2018
 * Purpose: Read analog inputs from any number of inputs and send them along a serial connection
 */

String message;
String separator;

/*
 * If you want to add potentiometers for more tags, just do it using the following two lines
 */
int sensorPins[3] = {A0,A1, A2}; // Change sensorPins[x] to sensorPins[x+1] and add the pin number to the list
int num_sensors = 3; // Increase the num_sensors by 1


void setup() {
  Serial.begin(9600);
  separator = "/" ; // This string separates each sensor pin and value pair
}

void loop() {
  message = ""; // Initialize an empty message
  // Go through each sensor
  for (int i = 0; i < num_sensors; i++){
    message =  message + ((String)sensorPins[i] + " " + analogRead(sensorPins[i]) + separator); // add a pin - value pair to the message
  }
  Serial.println(message);
}
