

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
    #elif(radius < 30):# move closer
        #moveforward()
