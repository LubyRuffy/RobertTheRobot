from RobertGrblSettings import *
#from Robert import tprint
######## Wheel movements settings ########

xp=0.0#x wheel position, forward is +
zp=0.0#z wheel position, forward is -


fd = "" #falling direction -> string, forward | backwards
pfd = "" #previous falling direction -> string, forward | backwards
addition = 0. #added speed from fd

# example of full line: "$J=X1 Z1 1500"
feedRate = "F1500"

############Wheels##################

def moveWheels(line):
    l = line.strip() # Strip all EOL characters for consistency
    #dp( 'Sending: ' + l)
    s.write(l + '\n') # Send g-code block to grbl
    #grbl_out = s.readline() # Wait for grbl response with carriage return
    #dp( ' : ' + grbl_out.strip())

def move(speed):
    #print(speed)
    global xp,zp
    xp = -speed
    zp = speed
    moveWheels("$J=X"+str(xp)+" Z"+str(zp)+feedRate)

def moveforward(speed): #Speed must be >= 0 
    tprint(speed)
    global xp,zp
    xp = speed
    zp = -speed
    moveWheels("$J=X"+str(xp)+" Z"+str(zp)+feedRate)

def movebackwards(speed): #Speed must be >= 0 
    tprint(speed)
    global xp,zp
    xp = -speed
    zp = speed
    moveWheels("$J=X"+str(xp)+" Z"+str(zp)+feedRate)

def moveright(speed):    
    global zp
    zp = -speed*2
    moveWheels("$J=Z"+str(zp)+feedRate)

def moveleft(speed):    
    global xp
    xp = speed*2
    moveWheels("$J=X"+str(xp)+feedRate)

moveWheels("x0 z0")# reset wheels
