# -*- encoding: UTF-8 -*-

import sys
import time

from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser
from threading import Thread


NAO_IP = "10.0.7.113"
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
        self.memory = ALProxy("ALMemory")

        #self.sonarProxy = ALProxy("ALSoundLocalizationProxy")
        #self.sonarProxy.subscribe("soundDetected")

    #def soundDetected(self, eventName, value, subscriberIdentifier):
        #print(str(value))


    #def setSoundDetection(self):
    #    while True:
    #        time.sleep(0.5)

    def setPersonDetection(self):
        ...

    def turnToOrigin(self):
        ...
    def walkToPerson(self):
        ...
    def greetPerson(self):
        ...

    

    def phasing(self):

        #global soundDetecter
        #soundDetecter = Thread(target=self.setSoundDetection)
        #soundDetecter.start()
        #print("Started setSoundDetection Thread")

        global personDetecter
        personDetecter = Thread(target=self.setPersonDetection)
        personDetecter.start()
        print("Started setPersonDetection Thread")

        
        while personDetectionData is None:
            turnThread = Thread(target=self.turnToOrigin)
            turnThread.start()
            turnThread.join()
        
        walkToPersonThread = Thread(target=self.walkToPerson)
        walkToPersonThread.start()
        walkToPersonThread.join()

        greetThread = Thread(target=self.greetPerson)
        greetThread.start()
        greetThread.join()

        


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
    HumanGreeter.phasing()

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
