#!/usr/bin/env python
#Program name: diceRoller.py
#Author: Dan Kercher
#Date last updated: 12/4/2020
#Purpose: Serve the flask serer with data from piCamera and an interface for servoController

import os
from time import sleep
from flask import Flask, render_template, request, Response
from camera_pi import Camera

app = Flask(__name__)

# Variables for the angle and servo GPIO pin
global rollServoAngle
rollServoAngle = 90
rollPin = 25

@app.route('/')
def index():
    """Video streaming home page."""
 
    templateData = {
      'rollServoAngle'	: rollServoAngle,
	}
    return render_template('index.html', **templateData)


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# Look at line 27 in index.html: <a href="/roll/70"class="button">Roll</a>
# Pressing this button will return the route /roll/70 which is "/<servo>/<angle>" below
# This route passes the servo and the angle to set. If extending for second servo, another
# button could be added to the HTML for <a href="/cam/20"class="button">Adjust</a>
# This would be ane example of an ajustment button that changes the camera angle
# Note: this is just an example of extendability, a few more variables and code would need
# to be added to implement the second cam angle servo (my kit only came with one servo)
@app.route("/<servo>/<angle>")
def move(servo, angle):
	global rollServoAngle
	if servo == 'roll':
		rollServoAngle = int(angle)
		os.system("python3 angleServoCtrl.py " + str(rollPin) + " " + str(rollServoAngle))
	# Extendable code example, referenced in above and in my project report. 
    # The idea is to add a second servo that could adjust the camera angle if a die is 
    # difficult to read due to bad lighting or awkward positioning
	#if servo == 'cam':
		#camServoAngle = int(angle)
		#os.system("python3 servoController.py " + str(camPin) + " " + str(camServoAngle))
	
	templateData = {
      'rollServoAngle'	: rollServoAngle,
	}
	return render_template('index.html', **templateData)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)
