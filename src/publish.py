#!/usr/bin/env python3

import paho.mqtt.publish as publish

server_host = "10.110.20.90"
server_port = 1883
command_topic = "/rtmsg/d25638bb-17c2-46ac-b26e-ce1f67268098/commands"
sensor_topic = "/rtmsg/d25638bb-17c2-46ac-b26e-ce1f67268098/sensors"
qos = 0
payload = '{"x":0.01,"y":0.0,"z":0.0}'

publish.single(command_topic, payload, hostname=server_host, port=server_port)
