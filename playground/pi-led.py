import RPi.GPIO as GPIO ## Import GPIO library
GPIO.setmode(GPIO.BCM) ## Use board pin numbering
GPIO.setup(23, GPIO.OUT) ## Setup GPIO Pin 7 to OUT
GPIO.output(23,False) ## Turn on GPIO pin 7
