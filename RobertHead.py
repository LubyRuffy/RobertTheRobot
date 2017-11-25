import RPi.GPIO as GPIO
import time
##horizontal: Straight is 6, left max is 2.5, right max is 11
##vertical: straight is 7, down is max 10, up is max 4

#define pin numbers
horisontalPin = 7
verticalPin = 12
#set mode of pi gpio
GPIO.setmode(GPIO.BOARD)
#assign gpio pins for head
GPIO.setup(verticalPin,GPIO.OUT) 
GPIO.setup(horisontalPin,GPIO.OUT)

#assign pwm to pins
headvert = GPIO.PWM(verticalPin,50)
headhor = GPIO.PWM(horisontalPin,50)

#setup start direction
currentHor = 6 ########change this back!!!!!
currentVert = 7 #7?
#start them
headvert.start(7.5)
headhor.start(7.5)


def moveheadleft(l):
    headhor.ChangeDutyCycle(currentHor-l)
    time.sleep(1)
    
def moveheadright(r):
    headhor.ChangeDutyCycle(currentHor+r)
    time.sleep(1)
    
def moveheaddown(d):
    headvert.ChangeDutyCycle(currentVert+d)
    time.sleep(1)
    
def moveheadup(u):
    headvert.ChangeDutyCycle(currentVert-u)
    time.sleep(1)
    
try:
    headhor.ChangeDutyCycle(currentHor)
    headvert.ChangeDutyCycle(currentVert)
    while True:
        print("move")
        moveheadleft(2)
        moveheadright(2)
        moveheaddown(2)
        moveheadup(2)
        

except KeyboardInterrupt:
    print("abort")
    headhor.stop()
    headvert.stop()
    GPIO.cleanup()



