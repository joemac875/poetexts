import time
import Adafruit_CharLCD as LCD
import threading
import pyxhook

key_mapping = {'P_End':1, 'P_Down':2, 'P_Next':3, 'P_Left':4, 'P_Begin':5, \
	       'P_Right':6, 'P_Home':7, 'P_Up':8, 'P_Page_Up':9, 'P_Insert':0}

# Raspberry Pi pin configuration:
lcd_rs = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows = 2


class ScreenManager():
    '''
    Manages an LCD screen. Responsible for Sending messages to the screen
    '''
    def __init__(self, base):

        # Initialize the LCD using the pins above.
        self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                                        lcd_columns, lcd_rows, lcd_backlight)
        
        self.lcd.message(base)
        # Create an empty message
        self.message = ''
        # All the following used for continually grabbing input
        self.new_hook = pyxhook.HookManager()
        self.new_hook.KeyDown = self.OnKeyPress
        #hook the keyboard
        self.new_hook.HookKeyboard()
        self.new_hook.start()
        

    def OnKeyPress(self, event):
        '''
        Checks to see if any key is being pressed and changes the message on the screen
        :return: None
        '''
        
        c = event.Key
        print(c)
        if c == 'BackSpace':
            # Delete a  character
            self.message = self.message[:-1]
            self.lcd.clear()
            self.lcd.message(self.message)
            # Some other key has been pressed
        else:
            try:
                # Add the Character
                c = str(key_mapping[c])
                self.message = self.message + c
                self.lcd.clear()
                self.lcd.message(self.message)
            except:
                print("Non Number Entered")
        if event.Ascii==96: #96 is the ascii value of the grave key (`)
            fob.close()
            new_hook.cancel()
            
    def clear_and_write(self, message):
        '''
        Clears the screen and prints a message to the screen
        :return: None
        '''
        self.lcd.clear()
        # Reset the user inputted message
        self.message = ''
        self.lcd.message(message)

    def get_message(self):
        '''
        :return: The current message
        '''
        return str(self.message)


class ScreenThread(threading.Thread):
    def __init__(self, threadID, name, screen_manager):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.manager = screen_manager

    def run(self):
        print ("Starting " + self.name)
        self.screen_manager.new_hook.start()
        print ("Exiting " + self.name)

    def clear_and_write(self, message):
        self.manager.clear_and_write(message)

    def get_message(self):
        return self.manager.get_message()
#print('start')
#bob = ScreenManager()

