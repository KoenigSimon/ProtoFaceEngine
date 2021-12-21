import datastructures as ds
import imagefunctions as imag
import config as conf

matrixX, matrixY = conf._MatrixSizeX, conf._MatrixSizeY
targetcolor = (0, 255, 255)
_myPixelsMatrix = imag.generatePixels()
pxmax = len(_myPixelsMatrix)


def bresenhamToFullPixelMatrix(pixels: [(float, float)]):
    fullPixelMatrix = imag.generatePixels()
    counter = 0
    for x in range(matrixX):
        for y in range(matrixY):
            if counter < len(pixels):
                if int(pixels[counter][0]) == x:
                    if int(pixels[counter][1]) == y:
                        fullPixelMatrix[ x * matrixY + y ] = targetcolor
                        counter = counter + 1

    return fullPixelMatrix

#Bresenham-Algorythm for rendering lines
def bresenham(vecs: [ds.Vector]):
    #pixels filled with (x, y)
    # startpoint always whole number
    pixels = [(vecs[0].x, vecs[0].y)]

    for i in range(len(vecs) - 1):
        x1, y1 = vecs[i].x, vecs[i].y
        x2, y2 = vecs[i+1].x, vecs[i+1].y

        dx = abs(x2 - x1)
        sx = 1 if x1 < x2 else -1
        dy = -abs(y2 - y1)
        sy = 1 if y1 < y2 else -1
        err = dx + dy

        while x1 < x2:
            if x1 == x2 and y1 == y2: break
            e2 = 2*err
            if e2 >= dy:
                err += dy
                x1 += sx

            if e2 <= dx:
                err += dx
                y1 += sy

            pixels.append((x1, y1))
    return pixels

############################################## Xiaolin Wu ##############################################

def plot(x, y, intensity: float, color: (int, int, int)):
    index = int(matrixY * x + y)
    #ignore out of bounds pixels
    if index > pxmax - 1:
        return
    _myPixelsMatrix[index] = tuple([round(x * intensity) for x in color])
    return

def rasterizeXailinWu(vecs: [ds.Vector]):

    global _myPixelsMatrix
    _myPixelsMatrix = imag.generatePixels()

    for i in range(len(vecs) - 1):
        vec1 = tuple(vecs[i].toArray())
        vec2 = tuple(vecs[i+1].toArray())
        draw_line(vec1, vec2, targetcolor)

    return _myPixelsMatrix


def _fpart(x):
    return x - int(x)

def _rfpart(x):
    return 1 - _fpart(x)

def putpixel(p, color, intensity):
    plot(p[0], p[1], intensity, color)

def draw_line(p1, p2, color):
    """Draws an anti-aliased line in img from p1 to p2 with the given color."""
    x1, y1 = p1
    x2, y2 = p2
    dx, dy = x2 - x1, y2 - y1
    steep = abs(dx) < abs(dy)
    p = lambda px, py: ((px, py), (py, px))[steep]

    if steep:
        x1, y1, x2, y2, dx, dy = y1, x1, y2, x2, dy, dx
    if x2 < x1:
        x1, x2, y1, y2 = x2, x1, y2, y1

    grad = dy / dx
    intery = y1 + _rfpart(x1) * grad

    def draw_endpoint(pt):
        x, y = pt
        xend = round(x)
        yend = y + grad * (xend - x)
        xgap = _rfpart(x + 0.5)
        px, py = int(xend), int(yend)
        putpixel(p(px, py), color, _rfpart(yend) * xgap)
        putpixel(p(px, py + 1), color, _fpart(yend) * xgap)
        return px

    xstart = draw_endpoint(p(*p1)) + 1
    xend = draw_endpoint(p(*p2))

    for x in range(xstart, xend):
        y = int(intery)
        putpixel(p(x, y), color, _rfpart(intery))
        putpixel(p(x, y + 1), color, _fpart(intery))
        intery += grad