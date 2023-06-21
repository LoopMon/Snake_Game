import pygame
from pygame.locals import *


pygame.init()

WIDTH = 500
HEIGHT = 500
canvas = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game')

done = False
while not done:
    canvas.fill('black')
    for event in pygame.event.get():
        if event.type == QUIT:
            done = True

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                done = True

    pygame.display.update()

pygame.quit()