import pygame
import math

pygame.init()

screenWidth = 1024
screenHeight = int((screenWidth / 16) * 9)

gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('The Maze')
clock = pygame.time.Clock()

crashed = False;

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        pygame.display.update()
        clock.tick(60)

pygame.quit()
quit()
