#!/usr/bin/python

###########DEBUG SETTINGS######

debugprint = 1
testprint = 1
def dp(line): # Debug print
    if(debugprint):
        print(line)
def tprint(line):
    if(testprint):
        print(line)


###########IMPORTS#############
    
from collections import deque
import math

from RobertVision import *
from RobertMotorControl import *
from mpu6050 import mpu6050


###########SETUP###############

#mpu# middle seems to be +0.4
middlePoint = 0.4
mpuOffset = 1.8# offset to activate motor
mpuaccsOffset = 9 #accs offset to activate motor
sensor = mpu6050(0x68)


prevTime = 0
angle = 0
previous_error = 0
integral = 0

angleError = 200

############Helper Functions & filters######### 

def get_time_difference_in_mili():
    global prevTime
	
    oldPrev = prevTime
    prevTime = int(round(time.time() * 1000))
    return float( prevTime - oldPrev )

def get_time_difference_in_mili_PID():
    global prevTimePID
	
    oldPrev = prevTimePID
    prevTimePID = int(round(time.time() * 1000))
    return float( prevTimePID - oldPrev )

def clamp(number): # restrict number on value range
    if(number > 0.01):
        number = 0.01
    elif(number < -0.01):
        number = -0.01
    return number
        
    

Kp = 1./55000. #these values you need to set yourself
Ki = 1./110000.
Ki = 0.
Kd = 0.

def PID():
    global angle, integral,previous_error

    error = 0 - angle
    dt = get_time_difference_in_mili_PID()
    integral = integral + error*dt
    derivative = (error - previous_error)/dt
    output = Kp*error + Ki*integral + Kd*derivative
    previous_error = error
    #dp("force is:" + str(output))
    return output	
    #wait(dt)

def get_angle():
    global angle
    gyro_data = sensor.get_accel_data() #accs and gyro methods seems to be flipped, so accel is acctualy gyro vica versa
    accel_data = sensor.get_gyro_data()
    acc = accel_data['y'] 

    gyro = gyro_data['x']
    dt = get_time_difference_in_mili()
    angle = 0.98 *(angle+gyro*dt) + 0.02*acc # complimentary filter
    #dp("angle is:" + str(angle-angleError))
    return (angle-angleError)


def balancedMotors(): #############################LOOK HERE!!!!!!!!!!#########################################################################################################
    ########GYRO and ACCS settings########    
    get_angle() # get current angle of robot by filter to reduce noice
    force = PID() # get current force that should be applied by using PID to reduce errors
    
    move(force) # negative is falling forward
	




###########MAIN                       LOOP################
prevTime = int(round(time.time() * 1000)) #set start time
prevTimePID = prevTime
# keep looping
try:
    while True:
        #balance motors and stand still
        balancedMotors()
        #findBall()
        #Find the ball
        #if ( not balancedMotors() ):
            #findBall()
            
        

except KeyboardInterrupt:
    ###########CLEANUPS############
    print("\ncleaning up")
    camera.release()
    cv2.destroyAllWindows()
    headhor.stop()
    headvert.stop()
    GPIO.cleanup()
    s.write("$1=0") # <- save power, by turning of wheel lock
    s.write("!\n")

