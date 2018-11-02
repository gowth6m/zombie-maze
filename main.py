import pygame
import math

from classes.item import Item
from classes.room import Room
from classes.player import Player

pygame.init()

gameTitle = 'The Maze'

# SCREEN DIMENSIONS
screenWidth = 1024
screenHeight = int((screenWidth / 16) * 9)

# COLOUR
black = (0, 0, 0)
white = (255, 255, 255)

# PLAYER ATTRIBUTES
x = 50
y = 50
playerWidth = 40
playerHeight = 60
speed = 10

gameDisplay = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption(gameTitle)
clock = pygame.time.Clock()

# GAME LOOP
run = True
while run:
    # pygame.time.delay(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        else:
            keys = pygame.key.get_pressed()

            if(keys[pygame.K_LEFT] or keys[pygame.K_a]):
                x -= speed
            if(keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                x += speed
            if(keys[pygame.K_UP] or keys[pygame.K_w]):
                y -= speed
            if(keys[pygame.K_DOWN] or keys[pygame.K_s]):
                y += speed

        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, white, (x, y, playerWidth, playerHeight))
        pygame.display.flip
        pygame.display.update()
        clock.tick(120)

pygame.quit()
# quit()
