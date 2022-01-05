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
import serial

broker="192.168.0.32"
port=1883

def updateDisplayMQTT():
    #MQTT config
    mqClient = paho.Client("FaceDataProvider")  # create client object
    mqClient.connect(broker, port)  # establish connection

    while not globals.threadAbort:
        startTime = time.process_time()
        pixels = globals.finalPixelMatrixAA if config._UseAntiAlising else globals.finalPixelMatrix

        data = (funcs.generateJSON(imfuncs.getSubPanels(pixels),
                                 [1, 1, 1, 1, 1, 1],
                                 [True, True, True, True, True, True],
                                 [False, False, False, False, False, False]))
        mqClient.publish("dev/faceImage", json.dumps(data))

        globals.packTime = (time.process_time() - startTime)
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

def updateDisplaySerial():
    ser = serial.Serial('COM9', 500000, timeout=0.5)
    while not globals.threadAbort:
        startTime = time.process_time_ns()
        pixels = globals.finalPixelMatrixAA if config._UseAntiAlising else globals.finalPixelMatrix
        data = (funcs.generateJSON(imfuncs.getSubPanels(pixels),
                                   [1, 1, 1, 1, 1, 1],
                                   [True, True, True, True, True, True],
                                   [False, False, False, False, False, False]))
        ser.write(json.dumps(data).encode())

        time.sleep(1.0 / config._TargetUpdatesPerSecond)
        globals.packTime = (time.process_time_ns() - startTime) / 1000000000


    time.sleep(0.5)
    # flush display pixels
    data = (funcs.generateJSON(imfuncs.getSubPanels(imfuncs.generatePixels()),
                               [0, 0, 0, 0, 0, 0],
                               [False, False, False, False, False, False],
                               [False, False, False, False, False, False]))
    ser.write(json.dumps(data).encode())
    time.sleep(0.5)
    ser.flushOutput()

    return

if __name__ == '__main__':
    globals.initialize()

    #Dispatch debug draw thread
    debugDrawThread = threading.Thread(target=draw.drawDebugWindow)
    debugDrawThread.start()

    #EITHER SERIAL OR MQTT NOT BOTH!!!
    #Dispatch MQTT display updating thread
    dispUpdateThreadMQTT = threading.Thread(target=updateDisplayMQTT)
    #dispUpdateThreadMQTT.start()

    # Dispatch Serial display updating thread
    dispUpdateThreadSerial = threading.Thread(target=updateDisplaySerial)
    dispUpdateThreadSerial.start()

    #join threads and disable hardware
    debugDrawThread.join()
    #dispUpdateThreadMQTT.join()
    dispUpdateThreadSerial.join()



