###########IMPORTS#############
import RPi.GPIO as GPIO
import cv2
import imutils
import numpy as np
import argparse
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


#ball tracking#
# construct the argument parse and parse the arguments

greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

searchStep = 0
# if a video path was not supplied, grab the reference
# to the webcams
camera = cv2.VideoCapture(0)

def moveheadleft(l):
    global currentHor
    if(currentHor+l > 10): #stop if reached max
        return
    #dp("move left"+str(currentHor)+str(l))
    headhor.ChangeDutyCycle(currentHor+l)
    currentHor = currentHor + l
    #time.sleep(swt)
    
    
def moveheadright(r):
    global currentHor
    if(currentHor - r < 2.5): #stop if reached max
        return
    #dp("move right"+str(currentHor)+str(r))
    headhor.ChangeDutyCycle(currentHor-r)
    currentHor = currentHor - r
    #time.sleep(swt)
    
def moveheaddown(d):
    global currentVert
    if(currentVert+d > 10): #stop if reached max
        return
    #dp("move down"+str(currentVert)+str(d))
    headvert.ChangeDutyCycle(currentVert+d)
    currentVert = currentVert+d
    #time.sleep(swt)
    
def moveheadup(u):
    global currentVert
    if(currentVert-u < 4): #stop if reached max
        return
    #dp("move up"+str(currentVert)+str(u))
    headvert.ChangeDutyCycle(currentVert-u)
    currentVert = currentVert-u
    #time.sleep(swt)

def lookAtSomething(x,y):
    #print("found something!")
    #dp(x)
    #dp(y)
    
    if(x < middlehorScreen-40):
        moveheadleft(headChange*((middlehorScreen-x)/middlehorScreen))
    elif (x > middlehorScreen+40):
        moveheadright(headChange*((x-middlehorScreen)/middlehorScreen))
    if(y < middleVertScreen-20):
        moveheadup(headChange*((middleVertScreen-y)/middleVertScreen))
    elif(y > middleVertScreen+20):
        moveheaddown(headChange*((y-middleVertScreen)/middleVertScreen))

    #moveToSomething()




#Code used is from pydevsearch's blog on openCV
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
    
    # only proceed if at least one contour was found
    if len(cnts) > 0:
            # find the largest contour in the mask, then use
            # it to compute the minimum enclosing circle and
            # centroid
            c = max(cnts, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            # only proceed if the radius meets a minimum size
            if radius > 10:
                    lookAtSomething(x,y) #Look at the thing you found
##    else: #try to find it
##        searchForSomething()

    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
            return False
    return True
