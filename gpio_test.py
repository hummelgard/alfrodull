import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #numbering style, will not use pin numbers
GPIO.setup(17,GPIO.OUT)
GPIO.output(17,False)
