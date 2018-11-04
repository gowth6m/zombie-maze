# SPRITE CLASS
import pygame as pg
import math
from settings import *
# from main import Game
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        # self.image.fill(WHITE)
        self.orig_image = self.image
        # self.image.blit(P_IMG, (0, 0))
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.mouse_pos = pg.mouse.get_pos()
        # self.p_angle = math.atan2(self.mouse_pos[0], self.mouse_pos[1])
        # self.player_rot = pg.transform.rotate(self.image, 360 - self.p_angle * 57.29)

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -PLAYER_SPEED
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = PLAYER_SPEED
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -PLAYER_SPEED
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = PLAYER_SPEED
        if self.vel.x != 0 and self.vel.y != 0:
            self.vel *= 0.85

    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y

    def rotate_player(self): #JUST NORMAL COORDs
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - WIDTH/2, mouse_y - HEIGHT/2
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pg.transform.rotate(self.orig_image, int(angle))
        # self.rect = self.image.get_rect(center=self.pos)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    # def player_rotate(self):  TESTING WITH VECTORS
    #     player_dir = pg.mouse.get_pos() - self.pos
    #     radius, angle = player_dir.as_polar()
    #     self.image = pg.transform.rotate(self.orig_image, -angle * PLAYER_ROT_SPEED)
        # self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rotate_player()
        # self.player_rotate()

        # WRAP AROUND SCREEN SIDE
        # if self.x > WIDTH:
        #     self.x = 0
        # if self.x < 0:
        #     self.x = WIDTH
        # if self.y > HEIGHT:
        #     self.y = 0
        # if self.y < 0:
        #     self.y = HEIGHT

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.image.blit(BG, (0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
