# SPRITE CLASS
import pygame as pg
import math
from settings import *
from tilemap import collide_hit_rect
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    """The Player class: the main player of the game."""

    def __init__(self, game, x, y):
        """Initialize the Player and it's attributes."""
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.mouse_pos = pg.mouse.get_pos()

    def get_keys(self):
        """Gets keyboard inputs and moves the players according to that."""
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
        """Call this when player collides with a wall."""
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.x > 0:
                    self.pos.x = hits[0].rect.left - self.hit_rect.width/2
                if self.vel.x < 0:
                    self.pos.x = hits[0].rect.right + self.hit_rect.width/2
                self.vel.x = 0
                self.hit_rect.centerx = self.pos.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False, collide_hit_rect)
            if hits:
                if self.vel.y > 0:
                    self.pos.y = hits[0].rect.top - self.hit_rect.height/2
                if self.vel.y < 0:
                    self.pos.y = hits[0].rect.bottom + self.hit_rect.height/2
                self.vel.y = 0
                self.hit_rect.centery = self.pos.y

    def rotate_player(self):
        """Rotating the player to point where the mouse is, without using vectors"""
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - WIDTH/2, mouse_y - HEIGHT/2
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pg.transform.rotate(self.orig_image, int(angle))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    # def player_rotate(self):  TESTING WITH VECTORS
    #     player_dir = pg.mouse.get_pos() - self.pos
    #     radius, angle = player_dir.as_polar()
    #     self.image = pg.transform.rotate(self.orig_image, -angle * PLAYER_ROT_SPEED)
        # self.rect = self.image.get_rect(center=self.rect.center)

    def update(self):
        """Updates for the loop."""
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        self.collide_with_walls('x')
        self.hit_rect.centery = self.pos.y
        self.collide_with_walls('y')
        self.rotate_player()
        self.rect.center = self.hit_rect.center

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
    """The Wall class: the first type of wall in the game."""

    def __init__(self, game, x, y):
        """Initialize Wall and it's attributes."""
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = game.wall_img
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.blit(BG, (0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Wall2(pg.sprite.Sprite):
    """The Wall class: the second type of wall in the game."""

    def __init__(self, game, x, y):
        """Initialize Wall2 and it's attributes."""
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.blit(BG2, (0, 0))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    """The Mob class: the mobs that chase after the player (zombie)."""

    def __init__(self, game, x, y):
        """Initialize a Mob and it's attributes."""
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0

    def update(self):
        """Updates the position etc for the loop."""
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
