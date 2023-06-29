# -*- encoding: UTF-8 -*-

# This is just an example script that shows how images can be accessed
# through ALVideoDevice in python.
# Nothing interesting is done with the images in this example.

from naoqi import ALProxy
import vision_definitions
import time
import json

IP = "10.0.7.100"  # Replace here with your NAOqi's IP address.
PORT = 9559

####
# Create proxy on ALVideoDevice

print "Creating ALVideoDevice proxy to ", IP

camProxy = ALProxy("ALVideoDevice", IP, PORT)

####
# Register a Generic Video Module

resolution = vision_definitions.kQQVGA
colorSpace = vision_definitions.kRGBColorSpace
fps = 2

nameId = camProxy.subscribe("python_GVM", resolution, colorSpace, fps)

naoImages = []
print 'getting images in remote'
for i in range(0, fps):
  print "getting image " + str(i)
  naoImages.append(camProxy.getImageRemote(nameId))
  print "With data:"
  for ii in range(0,5):
    print naoImages[i][ii]
  # Save the image.
  time.sleep(0.05)

camProxy.unsubscribe(nameId)


for i in range(0,fps):
  with open('roboimage'+str(i)+'.txt', 'w') as f:
    f.write(naoImages[i][6])
    f.close()
