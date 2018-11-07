import pygame as pg
from settings import *

def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)

S_WIDTH = 0
S_WIDTH = 0

class Map:
    """The Map class: the map of the game."""

    def __init__(self, filename):
        """Initialize the Map and it's attributes."""
        self.map_data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.map_data.append(line.strip())

        self.tileWidth = len(self.map_data[0])
        self.tileHeight = len(self.map_data)
        self.width = self.tileWidth * TILESIZE
        self.height = self.tileHeight * TILESIZE
        S_WIDTH = self.tileWidth
        S_HEIGHT = self.tileHeight

class Camera:
    """The Camera class: the camera that follows the player around."""

    def __init__(self, width, height):
        """Initialize the Camera and it's attributes."""
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(WIDTH/2)
        y = -target.rect.centery + int(HEIGHT/2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)

        self.camera = pg.Rect(x, y, self.width, self.height)
