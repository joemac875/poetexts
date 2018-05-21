# Client

The Raspberry Pi client that reads inputs from an Arduino, manages a switch and LEDS, prints output to an LCD screen, and finally sends poems to users' phone numbers.

## Usage

To run the client on the Raspberry Pi

`python3 main.py`

In `main.py` make sure that the 

* `aws_access_key_id`
* `aws_secret_access_key`
* `poem_server`

are all set to legal values.

# Adding Inputs

In `main.py` 

```python
inputs.add_input('14', ['love', 'war', 'environment', 'education', 'history'], 'topic', 1024)
```
is an example of what needs to be done to add inputs. The first parameter is the corresponding pin number of the potentiometer on the Arduino (keep in mind A0 = 14, A1 = 15, etc.). The second parameter is the tag values it should map to. The third parameter is the  tag key. Leave the fourth parameter alone.

