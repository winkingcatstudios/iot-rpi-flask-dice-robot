#!/usr/bin/env python
#Program name: servoController.py
#Author: Dan Kercher
#Date last updated: 12/4/2020
#Purpose: Set a servo to a designated angle, this is the mechanism that pushes the dice roller button
  
from time import sleep
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def setServoAngle(servo, angle):
	# Angle bounds are between 30 and 180 degrees
	assert angle >=30 and angle <= 180
	# Starts pwm and set the angle based on input, then sleeps for a bit to give it time to adjust, then stops pwm
	pwm = GPIO.PWM(servo, 50)
	pwm.start(8)
	dutyCycle = angle / 18. + 3.
	pwm.ChangeDutyCycle(dutyCycle)
	sleep(0.3)
	pwm.stop()

if __name__ == '__main__':
	import sys
	servo = int(sys.argv[1])
	GPIO.setup(servo, GPIO.OUT)
	# Calls function defined above to set to input angle, sleeps for adjustment time
	# then set the angle back to static 145 degrees which is the starting "off" position 
	setServoAngle(servo, int(sys.argv[2]))
	sleep(0.3)
	setServoAngle(servo, 145)
	GPIO.cleanup()

