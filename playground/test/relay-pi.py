##17/08/2013
##Khoa DO: testing GPIO with a relay board
##This script will define a GPIO pin as ouput and switch the connect relay on and off
##The loop count and delay/sleep time will be read from the command line interactively.


import RPi.GPIO as GPIO ## Import GPIO library
import time ## Import 'time' library. Allows us to use 'sleep'

myPin = 4
myPin2 = 17

GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(myPin, GPIO.OUT) ## Setup GPIO the Pin to OUT
GPIO.setup(myPin2, GPIO.OUT)

##Define a function named OnandOff()
def OnandOff(numTimes,speed):
        for i in range(0,numTimes):## Run loop numTimes
                print "Iteration " + str(i+1)## Print current loop
		if i%2==0:
                	GPIO.output(myPin,True)## Switch on pin 
		else:
                	GPIO.output(myPin2,True)## Switch on pin 
                time.sleep(speed)## Wait
                GPIO.output(myPin,False)## Switch off pin 
                GPIO.output(myPin2,False)## Switch off pin 
                time.sleep(speed)## Wait
        print "Done" ## When loop is complete, print "Done"
        GPIO.cleanup()

## Ask user for total number of switches and length of each blink
iterations = raw_input("Enter total number of times to switch: ")
speed = raw_input("Enter length of each switch(seconds): ")

## Start OnandOff() function. Convert user input from strings to numeric data types and pass to OnandOff() as parameters
OnandOff(int(iterations),float(speed))
