import time
import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(17, GPIO.IN)
GPIO.setup(18, GPIO.IN)
GPIO.setup(4, GPIO.IN)
GPIO.setup(22, GPIO.IN)
GPIO.setup(23, GPIO.IN)

prev_input = None
while True:
    input =  None
    if(GPIO.input(17)):
            input = "17"
    if(GPIO.input(18)):
            input = "18"
    if(GPIO.input(4)):
            input = "4"
    if(GPIO.input(22)):
            input = "22"
    if(GPIO.input(23)):
            input = "23"
    if ((not prev_input) and input):
        print "input %s" % input
        print "prev input  %s" % prev_input
    prev_input = input


    time.sleep(0.1)
