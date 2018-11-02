import math
import pygame
import pygame.locals

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
player_1 = Player(40, 60, 10, 0, 0, 0)

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

        if event.type == pygame.KEYDOWN:
            keys = pygame.key.get_pressed()

            if((keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_1.x > player_1.speed):
                player_1.x -= player_1.speed
            if((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_1.x < screenWidth - player_1.playerWidth - player_1.speed):
                player_1.x += player_1.speed
            if((keys[pygame.K_UP] or keys[pygame.K_w]) and player_1.y > player_1.speed):
                player_1.y -= player_1.speed
            if((keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_1.y < screenHeight - player_1.playerHeight - player_1.speed):
                player_1.y += player_1.speed

        if event.type == pygame.KEYUP:
            keys = pygame.key.get_pressed()

            if((keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_1.x > player_1.speed):
                player_1.x -= 0
            if((keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_1.x < screenWidth - player_1.playerWidth - player_1.speed):
                player_1.x += 0
            if((keys[pygame.K_UP] or keys[pygame.K_w]) and player_1.y > player_1.speed):
                player_1.y -= 0
            if((keys[pygame.K_DOWN] or keys[pygame.K_s]) and player_1.y < screenHeight - player_1.playerHeight - player_1.speed):
                player_1.y += 0

# lololol
        gameDisplay.fill(black)
        pygame.draw.rect(gameDisplay, white, (player_1.x, player_1.y, player_1.playerWidth, player_1.playerHeight))
        pygame.display.flip
        pygame.display.update()
        clock.tick(60)

pygame.quit()
# quit()
