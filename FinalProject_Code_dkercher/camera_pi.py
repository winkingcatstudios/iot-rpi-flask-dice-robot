#!/usr/bin/env python
#Program name: piCamera.py
#Author: Dan Kercher
#Credit: Modified version of Miguel Grinberg's pi camera hangling script
#Date last updated: 12/4/2020
#Purpose: Gets data from Raspberry Pi camera and turns it into a feed the flask server can stream

import time
import io
import threading
import picamera

class Camera(object):
    # thread reads the frames from the camera and stores them in frame, last access tracks camera access times
    thread = None  
    frame = None  
    last_access = 0 

    # Start the background thread (see note aboce) then wait for frame data to generate
    def initialize(self):
        if Camera.thread is None:
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            while self.frame is None:
                time.sleep(0)

    # Initialize, update access time and return frame data
    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # Set up the camera and define resolution, lower res is desired since we are just reading dice faces
            camera.resolution = (320, 240)
            camera.hflip = True
            camera.vflip = True

            # Delay to give the camera time to adjust
            camera.start_preview()
            time.sleep(2)

            # Use camera campture library to get jpegs and store them as frames
            stream = io.BytesIO()
            for x in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                stream.seek(0)
                cls.frame = stream.read()

                # Prepare for next frame by resetting stream
                stream.seek(0)
                stream.truncate()

                # Stop the stream if feed is no longer been requested
                # Here we use last access time and define an inactive period as 10 seconds
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
