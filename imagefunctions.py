import config as conf
import helperfunctions as funcs

panelSizeX, panelSizeY = conf._PanelSizeX, conf._PanelSizeY
matrixSizeX, matrixSizeY = conf._MatrixSizeX, conf._MatrixSizeY
panelCount = int((matrixSizeX / panelSizeX) * (matrixSizeY / panelSizeY))
panelPixelCount = panelSizeX * panelSizeY

def getSubPanels(pixels: []):
    subpanels = []
    for i in range(panelCount):
        subPanel = []
        for x in range(panelSizeX):
            for y in range(panelSizeY):
                subPanel.append(pixels[(i * panelPixelCount) + ((x * panelSizeX) + (y))])

        if conf._CompressDisplayStream:
            convPanel = convertTileCompress(subPanel)
        else:
            convPanel = convertTile(subPanel)

        subpanels.append(convPanel)
    return subpanels

def convertTile(pixels: []):
    result = []
    for p in pixels:
        result.append("0x{0:02x}{1:02x}{2:02x}".format(funcs.clamp(p[0]), funcs.clamp(p[1]), funcs.clamp(p[2])))
    return result

def convertTileCompress(pixels: []):
    result = []
    for p in pixels:
        if p == (0, 0, 0):
            result.append("f")
        else:
            result.append("0x{0:02x}{1:02x}{2:02x}".format(funcs.clamp(p[0]), funcs.clamp(p[1]), funcs.clamp(p[2])))
    return result

def generatePixels():
    pixels = []
    for x in range(matrixSizeX):
        for y in range(matrixSizeY):
            pixels.append((0, 0, 0))
    return pixels

def generateTestPixelPattern():
    pixels = []
    for x in range(matrixSizeX):
        for y in range(matrixSizeY):
            # pixels.append(( int((x / sizeX) * 255 ), int((y / sizeY) * 255), 0))
            # pixels.append((4, 1, 0))
            if y == 4:
                pixels.append((255, 0, 0))
            elif x == 5:
                pixels.append((0, 255, 0))
            elif x == 13:
                pixels.append((0, 255, 0))
            elif x == 21:
                pixels.append((0, 255, 0))
            elif x == 29:
                pixels.append((0, 255, 0))
            elif x == 37:
                pixels.append((0, 255, 0))
            elif x == 45:
                pixels.append((0, 255, 0))
            else:
                pixels.append((0, 0, 0))
    return pixels