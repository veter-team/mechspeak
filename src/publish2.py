#!/usr/bin/env python3

import paho.mqtt.client as mqtt
from time import sleep
import os

#server_host = "10.110.20.75"
server_host = "localhost"
server_port = 1883
command_topic = "/rtmsg/d25638bb-17c2-46ac-b26e-ce1f67268088/commands"
sensor_topic = "/rtmsg/d25638bb-17c2-46ac-b26e-ce1f67268088/sensors/"
qos = 0
frames_dir = '/home/pi/flags'

# Connect to mqtt server
mqttc = mqtt.Client(protocol=mqtt.MQTTv311)
mqttc.connect(server_host, port=server_port)
#mqttc.loop_start()

# Container for jpeg frames read from files
frames = []

# Scan directory for jpeg files and build frame data list
for dir_path, subdir_list, file_list in os.walk(frames_dir):
    for fname in file_list:
        if fname[-3:] == 'png':
            full_path = os.path.join(dir_path, fname)
            with open(full_path, "rb") as f:
                frame_data = bytearray(f.read())
                frames.append(frame_data);

camera_topic = sensor_topic + 'camera1'

# Publish frames to mqtt with some delay in between
for frame in frames:
    mqttc.publish(camera_topic, frame)
    print('.', len(frame))
    sleep(1.0 / 10) # FPS


# Disconnect from mqtt server
#mqttc.loop_stop()
mqttc.disconnect()
