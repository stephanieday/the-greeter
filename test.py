#from naoqi import ALProxy
#motion = ALProxy("ALMotion", "10.0.7.100", 9559)
#motion.setStiffnesses("Body", 1.0)
#motion.moveInit()
#motion.moveTo(0.5, 0, 0)

# -*- encoding: UTF-8 -*-

import sys
import time
import datetime

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser

from PIL import Image

NAO_IP = "10.0.7.13"
NAO_PORT = 9559

# Global variable to store the HumanGreeter module instance
HumanGreeter = None
memory = None


class HumanGreeterModule(ALModule):
    """ A simple module able to react
    to facedetection events

    """
    def __init__(self, name):
        self.fd = False
        ALModule.__init__(self, name)
        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to the FaceDetected event:
        global memory
        memory = ALProxy("ALMemory")
        # global sound
        # memory.subscribeToEvent("SoundDetected", "HumanGreeter", "onSoundDetected")
        global face
        memory.subscribeToEvent("FaceDetected", "HumanGreeter", "takePicture")

        global camProxy
        camProxy = ALProxy("ALVideoDevice", NAO_IP, NAO_PORT)
        # motion = ALProxy("ALMotion")
        # motion.setStiffnesses("Body", 1.0)
        # motion.moveInit()
        # while not self.fd:
        #    time.sleep(5)
        # motion.moveTo(1, 0, 0) #((2*3.141)/360)*45)

    def onOnSoundDetected(self):
        sound = True

    def onFaceDetected(self, *_args):
        """ This will be called each time a face is
        detected.

        """
        self.fd = True
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("FaceDetected",
            "HumanGreeter")

        self.tts.say("Hello") #, i detected a face" if self.fd else "Hello i did not detect a face")

        # Subscribe again to the event
        # memory.subscribeToEvent("FaceDetected",
        #     "HumanGreeter",
        #     "onFaceDetected")

    def takePicture(self, *_args):
        memory.unsubscribeToEvent("FaceDetected", "HumanGreeter")
        self.tts.say("Hello, i detected a face")

        resolution = 2    # VGA
        colorSpace = 11   # RGB

        videoClient = camProxy.subscribe("python_client", resolution, colorSpace, 5)

        for i in range(0,5):
            t0 = time.time()

            # Get a camera image.
            # image[6] contains the image data passed as an array of ASCII chars.
            naoImage = camProxy.getImageRemote(videoClient)

            t1 = time.time()

            # Time the image transfer.
            print("acquisition delay ", t1 - t0)

            camProxy.unsubscribe(videoClient)

            ## Now we work with the image returned and save it as a PNG  using ImageDraw
            # package.

            # Get the image size and pixel array.
            imageWidth = naoImage[0]
            imageHeight = naoImage[1]
            print(imageHeight)
            array = naoImage[6]

            # Create a PIL Image from our pixel array.
            im = Image.frombytes("RGB", (imageWidth, imageHeight), array)

            # Save the image.
            im.save("images/camImage_"+str(datetime.datetime.now())+".png", "PNG")

            im.show()
            time.sleep(5)


def main():
    """ Main entry point

    """
    parser = OptionParser()
    parser.add_option("--pip",
        help="Parent broker port. The IP address or your robot",
        dest="pip")
    parser.add_option("--pport",
        help="Parent broker port. The port NAOqi is listening to",
        dest="pport",
        type="int")
    parser.set_defaults(
        pip=NAO_IP,
        pport=NAO_PORT)

    (opts, args_) = parser.parse_args()
    pip   = opts.pip
    pport = opts.pport

    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       pip,         # parent broker IP
       pport)       # parent broker port


    # Warning: HumanGreeter must be a global variable
    # The name given to the constructor must be the name of the
    # variable
    global HumanGreeter
    HumanGreeter = HumanGreeterModule("HumanGreeter")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print()
        print("Interrupted by user, shutting down")
        myBroker.shutdown()
        sys.exit(0)

if __name__ == "__main__":
    main()
