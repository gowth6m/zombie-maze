# SPRITE CLASS
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((40, 40))
        self.image.fill(SAKURA)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC
        if keys[pg.K_UP]:
            self.acc.y = -PLAYER_ACC
        if keys[pg.K_DOWN]:
            self.acc.y = PLAYER_ACC

        # FRICTION
        self.acc += self.vel * PLAYER_FRICTION
        # PHYSICS TINGS
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        # WRAP AROUND SCREEN SIDE
        if self.pos.x > SCREEN_SIZE[0]:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_SIZE[0]

        if self.pos.y > SCREEN_SIZE[1]:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = SCREEN_SIZE[1]

        self.rect.center = self.pos
