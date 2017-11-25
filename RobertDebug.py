###########IMPORTS#############
import RPi.GPIO as GPIO
import time
    
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

import serial

from mpu6050 import mpu6050

###########DEBUG SETTINGS######
debugprint = False
def dp(line): # Debug print
    if(debugprint):
        print(line)

###########SETUP###############

#mpu#
sensor = mpu6050(0x68)
mpuSensitivity = 1.4

#GRBL#
# Open grbl serial port
s = serial.Serial('/dev/ttyUSB0',115200)
# Wake up grbl
s.write("\r\n\r\n")
time.sleep(2)   # Wait for grbl to initialize 
s.flushInput()  # Flush startup text in serial input

xp=0.0#x wheel position, forward is +
zp=0.0#z wheel position, forward is -

def moveWheels(line):
    
    l = line.strip() # Strip all EOL characters for consistency
    print( 'Sending: ' + l)
    s.write(l + '\n') # Send g-code block to grbl
    grbl_out = s.readline() # Wait for grbl response with carriage return
    print( ' : ' + grbl_out.strip())

def moveforward():
    global xp,zp
    xp = xp+0.1
    zp = zp-0.1
    moveWheels("X"+str(xp)+" Z"+str(zp))
def movebackwards():
    global xp,zp
    xp = xp-0.1
    zp = zp+0.1
    moveWheels("X"+str(xp)+" Z"+str(zp))

def moveright():    
    global xp,zp
    xp = xp+0.1
    zp = zp-0.2
    moveWheels("X"+str(xp)+" Z"+str(zp))

def moveleft():    
    global xp,zp
    xp = xp+0.2
    zp = zp-0.1
    moveWheels("X"+str(xp)+" Z"+str(zp))
    
def balanceMotors():
    gyro_data = sensor.get_gyro_data()
    y = gyro_data['y']# y direction is forward and backwards, z is up down and x is sideways
    
    print("y: " + str(y))
    

    if(y > mpuSensitivity):
        movebackwards
    elif(y < -mpuSensitivity):
        moveforward()
    time.sleep(0.05)
    
moveWheels("x0 z0")    
#Head#
##horizontal servo settings: Straight is 6, right max is 2.5, left max is 10
##vertical: straight is 7, down is max 10, up is max 4
vertScreen=640 # screen size
horScreen = 480
middleVertScreen = vertScreen/2
middlehorScreen = horScreen/2
headChange = 0.25
swt = 0.005 #servo wait time
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
currentHor = 6.0 ########change this back!!!!!
currentVert = 7.0 #7?
##start them
headvert.start(currentVert)
headhor.start(currentHor)

def moveheadleft(l):
    global currentHor
    if(currentHor+l > 10): #stop if reached max
        return
    dp("move left"+str(currentHor)+str(l))
    headhor.ChangeDutyCycle(currentHor+l)
    currentHor = currentHor + l
    time.sleep(swt)
    
    
def moveheadright(r):
    global currentHor
    if(currentHor - r < 2.5): #stop if reached max
        return
    dp("move right"+str(currentHor)+str(r))
    headhor.ChangeDutyCycle(currentHor-r)
    currentHor = currentHor - r
    time.sleep(swt)
    
def moveheaddown(d):
    global currentVert
    if(currentVert+d > 10): #stop if reached max
        return
    dp("move down"+str(currentVert)+str(d))
    headvert.ChangeDutyCycle(currentVert+d)
    currentVert = currentVert+d
    time.sleep(swt)
    
def moveheadup(u):
    global currentVert
    if(currentVert-u < 4): #stop if reached max
        return
    dp("move up"+str(currentVert)+str(u))
    headvert.ChangeDutyCycle(currentVert-u)
    currentVert = currentVert-u
    time.sleep(swt)

def lookAtSomething(x,y):
    #print("found something!")
    dp(x)
    dp(y)
    
    if(x < middlehorScreen-65):
        moveheadleft(headChange*((middlehorScreen-x)/middlehorScreen))
    elif (x > middlehorScreen+65):
        moveheadright(headChange*((x-middlehorScreen)/middlehorScreen))
    if(y < middleVertScreen-40):
        moveheadup(headChange*((middleVertScreen-y)/middleVertScreen))
    elif(y > middleVertScreen+40):
        moveheaddown(headChange*((y-middleVertScreen)/middleVertScreen))

    #moveToSomething()
    

def searchForSomething():
    #start down right, go to down left, go up left, then to up right
    #if not found, move somewhere random and go there
    dp("searching")
    # do a searching pattern    
    if(searchStep == 0):
        currentHor = 8
        headhor.ChangeDutyCycle(currentHor)

    if(searchStep == 6):
        moveleft()

        
        

def moveToSomething(radius):
    #turn by moving one wheel more than the other, until destination is straight forward, then go forward if ball is too small
    dp("moving to it")
    if(currentHor > 6.5):
        moveleft()
    elif(currentHor < 5.5):
        moveright()
    elif(radius < 30):# move closer
        moveforward()


#ball tracking#
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])
searchStep = 0
# if a video path was not supplied, grab the reference
# to the webcamssss
camera = cv2.VideoCapture(0)
def findBall():
    # grab the current frame
    (grabbed, frame) = camera.read()
    
    
    # resize the frame, blur it, and convert it to the HSV
    # color space
    #frame = imutils.resize(frame, width=600)
    # blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    center = None
    # only proceed if at least one contour was found
    if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            M = cv2.moments(c)
            center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            print("radius is: ",radius)
            # only proceed if the radius meets a minimum size
            if radius > 10:
                    # draw the circle and centroid on the frame,
                    # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius),
                            (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 0, 255), -1)
                    lookAtSomething(x,y) #Look at the thing you found
##    else: #try to find it
##        searchForSomething()
    # update the points queue
    pts.appendleft(center)

    # loop over the set of tracked points
    for i in xrange(1, len(pts)):
            # if either of the tracked points are None, ignore
            # them
            if pts[i - 1] is None or pts[i] is None:
                    continue

            # otherwise, compute the thickness of the line and
            # draw the connecting lines
            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
            cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show the frame to our screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
            return False
    return True
###########LOOP################
# keep looping
try:
    while True:
        #balance motors and stand still
        balanceMotors()
        #Find the ball
        if (findBall() == False):
            break
        

except KeyboardInterrupt:
    ###########CLEANUPS############
    print("cleaning up")
    camera.release()
    cv2.destroyAllWindows()
    headhor.stop()
    headvert.stop()
    GPIO.cleanup()

