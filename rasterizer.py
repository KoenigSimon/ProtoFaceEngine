import datastructures as ds
import imagefunctions as imag
import config as conf
from skimage.draw import line, line_aa
import numpy as np

matrixX, matrixY = conf._MatrixSizeX, conf._MatrixSizeY
targetcolor = (0, 255, 255)

def skLineRast(vecs: [ds.Vector]):
    #draw line into numpy array for support
    img = np.zeros((matrixX, matrixY), dtype=np.uint8)
    for i in range(len(vecs) - 1):
        rr, cc = line(vecs[i].x, vecs[i].y, vecs[i+1].x, vecs[i+1].y)
        img[rr, cc] = 1

    #convert to own datatype
    fullPixelMatrix = imag.generatePixels()
    for x in range(matrixX):
        for y in range(matrixY):
            if img[x, y] != 0:
                fullPixelMatrix[x * matrixY + y] = targetcolor
    return fullPixelMatrix

def skLineRastAA(vecs: [ds.Vector]):
    #draw line into numpy array for support
    img = np.zeros((matrixX, matrixY), dtype=np.float64)
    for i in range(len(vecs) - 1):
        rr, cc, val = line_aa(vecs[i].x, vecs[i].y, vecs[i+1].x, vecs[i+1].y)
        img[rr, cc] = val

    #convert to own datatype
    fullPixelMatrix = imag.generatePixels()
    for x in range(matrixX):
        for y in range(matrixY):
            if img[x, y] != 0:
                fullPixelMatrix[x * matrixY + y] = tuple([round(v * img[x, y]) for v in targetcolor])
    return fullPixelMatrix
