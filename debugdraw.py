import pygame
import pygame.key as key
from pygame.locals import QUIT, K_DOWN, K_UP,K_LEFT, K_RIGHT
from time import sleep
import time
import numpy

import config
import globals
import rasterizer as rast
import helperfunctions

def drawDebugWindow():

    pygame.init()
    pygame.display.set_caption("Debug View")
    myfont = pygame.font.SysFont('Consolas', 14)
    screen = pygame.display.set_mode((480, 240))
    TextRawView = myfont.render('Raw View', False, 'white')
    textRastView = myfont.render('Rasterized View', False, 'white')


    matX, matY = config._MatrixSizeX, config._MatrixSizeY

    dynval1 = 0.0
    dynval2 = 0.5

    clock = pygame.time.Clock()
    pps = 0

    while not globals.threadAbort:

        ##################################### Event Handling ####################################

        for event in pygame.event.get():
            if event.type == QUIT:
                globals.threadAbort = True

        clock.tick()
        TextFPS = myfont.render('FPS: ' + str(clock.get_fps()), False, 'white')
        if not globals.packTime == 0:
            pps = 1.0 / globals.packTime
        TextPackTime = myfont.render('Json pack: ' + str(pps) + "/s", False, 'white')

        ##################################### Test Logic ####################################

        #generate lines and rasterize
        testLinesRaw = helperfunctions.setPointsRelative(0, 0,
                                               0.25, 1,
                                               dynval2, dynval1,
                                               0.75, 1,
                                               1, 0)

        rastLines = rast.bresenham(testLinesRaw)
        globals.finalPixelMatrix = rast.bresenhamToFullPixelMatrix(rastLines)
        globals.finalPixelMatrixAA = rast.rasterizeXailinWu(testLinesRaw)

        #get input to modify lines
        keys = key.get_pressed()
        if keys[K_DOWN]:
            dynval1 -= 0.05
            #print(dynval1)
        if keys[K_UP]:
            dynval1 += 0.05
            #print(dynval1)

        if keys[K_LEFT]:
            dynval2 -= 0.01
        if keys[K_RIGHT]:
            dynval2 += 0.01

            ##################################### Rendering #####################################
        #draw raw lines
        #pygame.draw.line(screen, 'cyan', (0, 0), (150, 100), width=5)
        screen.fill((0, 0, 0))

        offset = [0, 15]
        scale = [10, 10]

        for i in range(len(testLinesRaw) - 1):
            start = numpy.add(numpy.multiply(testLinesRaw[i].toArray(), scale), offset)
            end = numpy.add(numpy.multiply(testLinesRaw[i+1].toArray(), scale), offset)
            pygame.draw.line(screen, 'cyan', start, end, width=5)

        #draw (disabled) raster pixels to fixed 10x scale
        offset = [0, 135]
        #for x in range(matX):
        #    for y in range(matY):
        #        pos = numpy.add([x * 10, y * 10], offset)
        #        pygame.draw.rect(screen, (10, 10, 10), (pos[0], pos[1], 9, 9))

        for x in range(matX):
            for y in range(matY):
                pos = numpy.add([x * 10, y * 10], offset)
                color = globals.finalPixelMatrixAA[x * matY + y]
                color2 = globals.finalPixelMatrix[x * matY + y]
                #if color2 != (0, 0, 0):
                #    pygame.draw.rect(screen, color2, (pos[0], pos[1], 9, 9))
                if color != (0, 0, 0):
                    pygame.draw.rect(screen, color, (pos[0], pos[1], 9, 9))
                else:
                    pygame.draw.rect(screen, (10, 10, 10), (pos[0], pos[1], 9, 9))

        screen.blit(TextRawView, (0,0))
        screen.blit(TextFPS, (400, 0))
        screen.blit(textRastView, (0, 120))
        screen.blit(TextPackTime, (340, 120))
        #pygame.draw.rect(screen, (0, 100, 255), (50, 50, 162, 100), 3)  # width = 3
        #pygame.draw.rect(screen, (0, 100, 255), (50, 50, 162, 100), 3)  # width = 3
        sleep(1.0 / config._TargetDebugFPS)
        pygame.display.flip()
    pygame.quit()