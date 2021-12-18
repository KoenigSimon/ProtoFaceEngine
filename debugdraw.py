import pygame
from pygame.locals import QUIT
from time import sleep
import numpy

import config
import rasterizer as rast
import helperfunctions as funcs

def drawDebugWindow():
    pygame.init()
    pygame.display.set_caption("Debug View")
    myfont = pygame.font.SysFont('Consolas', 14)
    screen = pygame.display.set_mode((480, 240))
    TextRawView = myfont.render('Raw View', False, 'white')
    textRastView = myfont.render('Rasterized View', False, 'white')

    matX, matY = config._MatrixSizeX, config._MatrixSizeY

    x = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        screen.fill((0, 0, 0))

        #x = x+0.01

        #setup values
        #zigzag test pattern
        ptsUpper = funcs.setPointsRelative(0, 0,
                                           0.25, 1,
                                           0.5, 0,
                                           0.75, 1,
                                           1, 0)

        ptsUpper = funcs.setPointsAbsolute(0, 0,
                                           12, 8,
                                           24, 0,
                                           36, 8,
                                           48, 0)

        #ptsUpper = funcs.setPointsRelative(0, 0,
        #                                   0.125, 1,
        #                                   0.25, 0,
        #                                   0.375, 1,
        #                                   0.5, 0,
        #                                   0.625, 1,
        #                                   0.75, 0,
        #                                   0.875, 1,
        #                                   1, 0)


        #returns only active pixels
        linePixels = rast.bresenham(ptsUpper)

        #returns all pixels
        linePixelsAA = rast.rasterizeXailinWuAlt(ptsUpper)

        #draw raw lines
        #pygame.draw.line(screen, 'cyan', (0, 0), (150, 100), width=5)
        offset = [0, 15]
        scale = [10, 10]
        for i in range(len(ptsUpper) - 1):
            start = numpy.add(numpy.multiply(ptsUpper[i].toArray(), scale), offset)
            end = numpy.add(numpy.multiply(ptsUpper[i+1].toArray(), scale), offset)
            pygame.draw.line(screen, 'cyan', start, end, width=5)

        #draw (disabled) raster pixels to fixed 10x scale
        offset = [0, 135]
        for x in range(matX):
            for y in range(matY):
                pos = numpy.add([x * 10, y * 10], offset)
                pygame.draw.rect(screen, (10, 10, 10), (pos[0], pos[1], 9, 9))

        #draw active pixels over disabled ones
        for pixel in linePixels:
            pos = numpy.add([pixel[0] * 10, pixel[1] * 10], offset)
            #pygame.draw.rect(screen, (0, 255, 255), (pos[0], pos[1], 9, 9))

        for x in range(matX):
            for y in range(matY):
                pos = numpy.add([x * 10, y * 10], offset)
                color = linePixelsAA[x * matY + y]
                if color == (0, 0, 0):
                    continue
                pygame.draw.rect(screen, color, (pos[0], pos[1], 9, 9))


        screen.blit(TextRawView, (0,0))
        screen.blit(textRastView, (0, 120))
        #pygame.draw.rect(screen, (0, 100, 255), (50, 50, 162, 100), 3)  # width = 3
        #pygame.draw.rect(screen, (0, 100, 255), (50, 50, 162, 100), 3)  # width = 3
        sleep(0.05)
        pygame.display.flip()
    pygame.quit()