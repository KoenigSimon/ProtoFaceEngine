import datastructures as ds
import config as conf

def generateJSON(data: [], rot: [], mirr: [], zigzag: []):
    message = {}
    message['brightnessFactor'] = 0.1
    message['panels'] = []
    print(data)
    for i in range(len(data)):
        panel = {}
        panel["rot"] = rot[i]
        panel["mirr"] = mirr[i]
        panel["zigzag"] = zigzag[i]
        panel["dots"] = data[i]
        message['panels'].append(panel)
    return message

def clamp(x):
  return max(0, min(x, 255))

def pointsToDirections(vecs: [ds.Vector]):
    #TODO: replace with assert
    if len(vecs) < 2:
        raise Exception("Supplied less than two vectors, lines cannot be built")

    dirs = []
    i = 0
    while i < len(vecs) - 1:
        dirs.append(vecs[i+1] - vecs[i])
        i += 1
    return dirs

#point order in x1, y2, x2, y2...
def setPointsAbsolute(*argv):
    points = []
    i = 0
    while i < len(argv):

        tmp = ds.Vector()
        tmp.x = argv[i]
        tmp.y = argv[i + 1]

        if i == 0:
            tmp.x = 0
        elif i is len(argv) - 2:
            tmp.x = conf._MatrixSizeX
        i += 2

        if tmp.x < 0:
            tmp.x = 0
        if tmp.y < 0:
            tmp.y = 0
        if tmp.x > conf._MatrixSizeX:
            tmp.x = conf._MatrixSizeX
        if tmp.y > conf._MatrixSizeY:
            tmp.y = conf._MatrixSizeY

        points.append(tmp)
    return points

#point order in x1, y1, x2, y2...
def setPointsRelative(*argv):
    points = []
    i = 0
    while i < len(argv):

        tmp = ds.Vector()
        tmp.x = argv[i]
        tmp.y = argv[i + 1]

        if i == 0:
            tmp.x = 0
        elif i is len(argv) - 2:
            tmp.x = 1
        i += 2

        if tmp.x < 0:
            tmp.x = 0
        if tmp.y < 0:
            tmp.y = 0
        if tmp.x > 1:
            tmp.x = 1
        if tmp.y > 1:
            tmp.y = 1

        scalingVector = ds.Vector(conf._MatrixSizeX, conf._MatrixSizeY)
        tmp *= scalingVector

        points.append(tmp)
    return points