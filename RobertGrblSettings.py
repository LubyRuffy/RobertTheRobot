#########GRBL Settings##############

import serial
import time

def wait(n):
    time.sleep(n)

# Open grbl serial port
s = serial.Serial('/dev/ttyUSB0',115200) # serial to usb from arduino, change it if it is wrong.

# Wake up grbl
s.write("\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize 
s.flushInput()  # Flush startup text in serial input
time.sleep(0.5)
# Set grbl run settings
s.write("G91" + '\n')
s.readline()
s.write("$1=255" + '\n') # <- set to lock wheels
s.readline()
multiplier = 1
