import globals
import helperfunctions as funcs
import imagefunctions
import imagefunctions as imfuncs
import json
import paho.mqtt.client as paho
import debugdraw as draw
import threading
import time
import config

broker="192.168.0.32"
port=1883

def updateDisplay():
    #MQTT config
    mqClient = paho.Client("FaceDataProvider")  # create client object
    mqClient.connect(broker, port)  # establish connection

    while not globals.threadAbort:
        pixels = globals.finalPixelMatrixAA if config._UseAntiAlising else globals.finalPixelMatrix

        data = (funcs.generateJSON(imfuncs.getSubPanels(pixels),
                                 [1, 1, 1, 1, 1, 1],
                                 [True, True, True, True, True, True],
                                 [False, False, False, False, False, False]))
        mqClient.publish("dev/faceImage", json.dumps(data))
        time.sleep(1 / config._TargetUpdatesPerSecond)


    #flush display pixels
    data = (funcs.generateJSON(imfuncs.getSubPanels(imfuncs.generatePixels()),
                               [0, 0, 0, 0, 0, 0],
                               [False, False, False, False, False, False],
                               [False, False, False, False, False, False]))
    mqClient.publish("dev/faceImage", json.dumps(data))
    #wait for safe thread exit
    time.sleep(0.5)
    return

if __name__ == '__main__':
    globals.initialize()

    #Dispatch debug draw thread
    debugDrawThread = threading.Thread(target=draw.drawDebugWindow)
    debugDrawThread.start()

    #Dispatch display updating thread
    dispUpdateThread = threading.Thread(target=updateDisplay)
    dispUpdateThread.start()

    #join threads and disable hardware
    debugDrawThread.join()
    dispUpdateThread.join()



