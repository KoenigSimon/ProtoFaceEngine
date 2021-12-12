import pygame
import config
from pygame.locals import QUIT
from time import sleep
import numpy

from main import *

def drawDebugWindow():
    pygame.init()
    pygame.display.set_caption("Debug View")
    myfont = pygame.font.SysFont('Consolas', 14)
    screen = pygame.display.set_mode((480, 240))
    TextRawView = myfont.render('Raw View', False, 'white')
    textRastView = myfont.render('Rasterized View Scaled', False, 'white')

    matX, matY = config._MatrixSizeX, config._MatrixSizeY

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
        screen.fill((0, 0, 0))

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
                pygame.draw.rect(screen, (0, 50, 50), (pos[0], pos[1], 9, 9))

        screen.blit(TextRawView, (0,0))
        screen.blit(textRastView, (0, 120))
        #pygame.draw.rect(screen, (0, 100, 255), (50, 50, 162, 100), 3)  # width = 3
        #pygame.draw.rect(screen, (0, 100, 255), (50, 50, 162, 100), 3)  # width = 3
        sleep(0.05)
        pygame.display.flip()
    pygame.quit()