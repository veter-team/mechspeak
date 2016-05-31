#!/usr/bin/env python3

import io
import time
import struct
import picamera
import paho.mqtt.client as mqtt

host = "test.mosquitto.org"
#host = "localhost"
qos = 0
sensors_topic = "/rtmsg/d25638bb-17c2-46ac-b26e-ce1f67268088/sensors/"
camera_topic = sensors_topic + "camera1"

mqttc = mqtt.Client("zatoichipy")
print('Connecting...')
mqttc.connect(host)
print('Connected')
mqttc.loop_start()

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    # Start a preview and let the camera warm up for 2 seconds
    camera.start_preview()
    time.sleep(2)

    framecnt = 0
    stream = io.BytesIO()
    for foo in camera.capture_continuous(stream, 'jpeg', resize=(128, 128), use_video_port=True):
    #while True:
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        frame_data = bytearray(stream.read())
        framecnt += 1
        print(framecnt, len(frame_data), end='\r')
        mqttc.publish(camera_topic, frame_data, qos=qos)
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        time.sleep(1.0 / 10) # FPS

mqttc.loop_stop()
mqttc.disconnect()

