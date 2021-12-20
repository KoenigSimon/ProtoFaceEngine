import helperfunctions as funcs
import imagefunctions as imfuncs
import json
import paho.mqtt.client as paho
import debugdraw as draw
import threading
import rasterizer as rast

broker="192.168.0.32"
port=1883

#Set lines for rastarization
#ptsUpper = funcs.setPointsRelative(0, 0, 0.5, 0.5, 1, 0.25)

#test zigzag pattern
#ptsUpper = funcs.setPointsRelative(0, 0,
#                                   0.125, 1,
#                                   0.25, 0,
#                                   0.375, 1,
#                                   0.5, 0,
#                                   0.625, 1,
#                                   0.75, 0,
#                                   0.875, 1,
#                                   1, 0)

ptsUpper = funcs.setPointsRelative(0, 0,
                                   0.25, 1,
                                   0.5, 0,
                                   0.75, 1,
                                   1, 0)

#returns only active pixels
linePixels = rast.bresenham(ptsUpper)
linePixelColors = rast.bresenhamToPixelMatrix(linePixels)

#returns all pixels
linePixelsAA = rast.rasterizeXailinWuAlt(ptsUpper)

if __name__ == '__main__':
    #Dispatch debug draw thread
    th = threading.Thread(target=draw.drawDebugWindow)
    th.start()

    for pix in linePixels:
        print(pix, end=" ")
    print("")
    for pix in linePixelColors:
        print(pix, end=" ")

    #generate image pixels
    pixels = imfuncs.generateTestPixelPattern()
    data = (funcs.generateJSON(imfuncs.getSubPanels(linePixelColors),
                             [1, 1, 1, 1, 1, 1],
                             [True, True, True, True, True, True],
                             [False, False, False, False, False, False]))

    #Sending
    mqClient = paho.Client("FaceDataProvider")  # create client object
    mqClient.connect(broker, port)  # establish connection

    ret = mqClient.publish("dev/faceImage", json.dumps(data))

    #join threads and disable hardware
    th.join()
    data = (funcs.generateJSON(imfuncs.getSubPanels(imfuncs.generatePixels()),
                               [0, 0, 0, 0, 0, 0],
                               [False, False, False, False, False, False],
                               [False, False, False, False, False, False]))
    mqClient.publish("dev/faceImage", json.dumps(data))
