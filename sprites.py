# SPRITE CLASS
import pygame as pg
from settings import *
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((32, 32))
        self.image.fill(SAKURA)
        self.image.blit(P_IMG, (0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
        self.pos = vec(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        # self.wealth = 0

    def update(self):
        self.acc = vec(0, 0)
        keys = pg.key.get_pressed()
        if (keys[pg.K_LEFT] or keys[pg.K_a]):
            self.acc.x = -PLAYER_ACC
        if (keys[pg.K_RIGHT] or keys[pg.K_d]):
            self.acc.x = PLAYER_ACC
        if (keys[pg.K_UP] or keys[pg.K_w]):
            self.acc.y = -PLAYER_ACC
        if (keys[pg.K_DOWN] or keys[pg.K_s]):
            self.acc.y = PLAYER_ACC

        # FRICTION
        self.acc += self.vel * PLAYER_FRICTION
        # PHYSICS TINGS
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        # WRAP AROUND SCREEN SIDE
        #WIDTH
        if self.pos.x > SCREEN_SIZE[0]:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = SCREEN_SIZE[0]
        #HEIGHT
        if self.pos.y > SCREEN_SIZE[1]:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = SCREEN_SIZE[1]

        self.rect.center = self.pos
