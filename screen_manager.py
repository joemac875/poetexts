import termios, fcntl, sys, os
import time
import Adafruit_CharLCD as LCD
import threading
fd = sys.stdin.fileno()

# Raspberry Pi pin configuration:
lcd_rs        = 26  # Note this might need to be changed to 21 for older revision Pi's.
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 4

# Define LCD column and row size for 16x2 LCD.
lcd_columns = 16
lcd_rows    = 2

class ScreenManager():
    def __init__(self):

        # Initialize the LCD using the pins above.
        self.lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                               lcd_columns, lcd_rows, lcd_backlight)
        # Print a two line message
        base = 'Enter Phone #\nto Get a Poem'
        self.lcd.message(base)
        # Create an empty message
        self.message = ''
        self.oldterm = termios.tcgetattr(fd)
        self.newattr = termios.tcgetattr(fd)
        self.newattr[3] = self.newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, self.newattr)

        self.oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, self.oldflags | os.O_NONBLOCK)
    def wait_for_input(self):
        try:
            c = sys.stdin.read(1)
            if c == '\x7f':
                self.message = self.message[:-1]
                self.lcd.clear()
                self.lcd.message(self.message)
                
            elif c != '':
                self.message = self.message + c
                self.lcd.clear()
                self.lcd.message(self.message)
            
        except IOError: pass
        
    def reset(self):
        self.lcd.clear()
        self.message = ''
        self.lcd.message('Enter Phone #\nto Get a Poem')
    def notify_sent(self, success):
        self.lcd.clear()
        if success:
            self.lcd.message('Message Sent!')
        else:
            self.lcd.message('Unusable Phone #')
    def get_message(self):
        return str(self.message)



class ScreenThread (threading.Thread):
   def __init__(self, threadID, name, screen_manager):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.manager = screen_manager

   def run(self):
      print ("Starting " + self.name)
      self.continuous_read()
      print ("Exiting " + self.name)
   def continuous_read(self):
      while True:
          self.manager.wait_for_input()
   def notify_sent(self, success):
       self.manager.notify_sent(success)
   def reset(self):
       self.manager.reset()
   def get_message(self):
       return self.manager.get_message()



