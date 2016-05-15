#Message exchange over web-sockets using MQTT

This project is an example how to exchange messages between publishers and subscribers running withing web-browser. For this purposes we are using MQTT message exchange protocol and test.mosquitto.org public server. In addition, we are using Paho JavaScript MQTT client.

To illustrate our approach we decide to create "cockpit" application where the user can adjust two values - speed alone X and Z axis using sliders. In the middle position, speed is zero. Moving slider to the right will set positive speed, to the left - negative. Here is the screenshot:
![alt cockpit](https://github.com/veter-team/mechspeak/blob/master/images/cockpit.png)

The second application "simulation" shows the 3D scene using ThreeJS. There is a ball, a plane and axis orientation indicator in the middle:
![alt simulation](https://github.com/veter-team/mechspeak/blob/master/images/simulation.png)

The "cockpit" application could be used to control ball movement alone two axis.

It is possible to run multiple "cockpit" and "simulation" applications. As long as they are using the same MQTT topics for communication, they all will exchange events in publish/subscribe style.

To avoid collisions with other users running this example, we suggest to regenerate new UUID using whatever tool you prefere or just by runnning our generateUUID() function from browser's JavaScript console as illustrated on the following screenshot:
![alt generateuuid](https://github.com/veter-team/mechspeak/blob/master/images/generateuuid.png)

After that, you can copy the generated uuid and adjust the command_topic and sensor_topic variables in www/js/utility.js file by replacing UUID with your newly generated one.
