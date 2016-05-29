import os, sys
import io
import Tkinter
import Image, ImageTk
from time import sleep
import cStringIO
import paho.mqtt.client as mqtt


host = "test.mosquitto.org"
#host = "localhost"
qos = 0
sensors_topic = "/rtmsg/d25638bb-17c2-46ac-b26e-ce1f67268088/sensors/"
camera_topic = sensors_topic + "camera1"

imgcnt = 0

def on_message(client, userdata, message):
    global imgcnt
    global old_label_image 
    global root
    try:
        image1 = Image.open(cStringIO.StringIO(message.payload))
        root.geometry('%dx%d' % (image1.size[0],image1.size[1]))
        tkpi = ImageTk.PhotoImage(image1)
        label_image = Tkinter.Label(root, image=tkpi)
        label_image.place(x=0,y=0,width=image1.size[0],height=image1.size[1])
        imgcnt += 1
        root.title(str(imgcnt))
        if old_label_image is not None:
            old_label_image.destroy()
        old_label_image = label_image
        root.update() # wait until user clicks the window
    except Exception, e:
        # This is used to skip anything not an image.
        # Image.open will generate an exception if it cannot open a file.
        print(e)
        mqttc.disconnect()


mqttc = mqtt.Client("zatoichi" + str(os.getpid()))
print('Connecting...')
mqttc.connect(host)
print('Connected')

mqttc.on_message = on_message
mqttc.subscribe(camera_topic)

root = Tkinter.Tk()
root.geometry('+%d+%d' % (128, 128))
old_label_image = None

mqttc.loop_forever()

