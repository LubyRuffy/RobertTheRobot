#!/usr/bin/env python
import serial
import time

# Open grbl serial port
s = serial.Serial('/dev/ttyUSB0',115200)

# Open g-code file
#f = open('grbl.gcode','r');

# Wake up grbl
s.write("\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize
s.flushInput()  # Flush startup text in serial input
s.write("G91" + '\n')

def readInput():
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print ' : ' + grbl_out.strip()

def moveWheels(line):
    l = line.strip() # Strip all EOL characters for consistency
    print 'Sending: ' + l,
    s.write(l + '\n') # Send g-code block to grbl
    readInput()

def writeByte(bName):
    s.write(b'\x18')
    s.write("\n")
    readInput()

# Stream g-code to grbl
try:
    while(1):
        line = raw_input()
        if(line=="$$"):
            time.sleep(0.5)
            moveWheels(line)
            for i in range(35):
                readInput()
        elif(line=="c"):
            s.write(b'\xC2' + b'\x85')
            s.write("\n")
            readInput()
            s.write("G4P0\n")
            readInput()
        else:
	        moveWheels(line)        


except KeyboardInterrupt:
    # Wait here until grbl is finished to close serial port and file.
    raw_input("  Press <Enter> to exit and disable grbl.")
    # Close serial port
    #s.write(b'\x85')
    s.write('!')
    s.write("\n")
    s.close()
