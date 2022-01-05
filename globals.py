import imagefunctions

global threadAbort
global finalPixelMatrix
global finalPixelMatrixAA

global packTime

def initialize():
    global threadAbort
    threadAbort = False

    global finalPixelMatrix
    finalPixelMatrix = imagefunctions.generatePixels()

    global finalPixelMatrixAA
    finalPixelMatrixAA = imagefunctions.generatePixels()

    global packTime
    packTime = 0
