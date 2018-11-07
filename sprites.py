# SPRITE CLASS
import pygame as pg
import math

from random import uniform, choice
from settings import *
from tilemap import collide_hit_rect

vec = pg.math.Vector2

# killedMobPos = vec(0, 0)
# GET ANGLE TO PLAYER OR MOUSE
def get_angle(sprite):
    mouse_x, mouse_y = pg.mouse.get_pos()
    rel_x, rel_y = mouse_x - WIDTH/2, mouse_y - HEIGHT/2
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    return angle

# COLLISION BETWEEN SPRITES
def sprite_collision(sprite, group, dir):
    """Call this when player or mob collides with a wall."""
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width/2
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width/2
            sprite.vel.x = 0
            sprite.hit_rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
        if hits:
            if hits[0].rect.centery > sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height/2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height/2
            sprite.vel.y = 0
            sprite.hit_rect.centery = sprite.pos.y

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
        self.rect.center = vec(x, y)
        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.mouse_pos = pg.mouse.get_pos()
        self.rot = 0
        self.last_shot = 0
        self.hp = PLAYER_HP
        self.zombies_killed = ZOMBIES_KILLED
        self.zombies_killed_updated = 0

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
        if keys[pg.K_SPACE]:
            now = pg.time.get_ticks()
            if now - self.last_shot > BULLET_RATE:
                self.last_shot = now
                dir = vec(1, 0).rotate(-get_angle(self))
                pos = self.pos + BULLET_OFFSET.rotate(-get_angle(self))
                Bullet(self.game, pos, dir)
                self.vel = vec(-KNOCKBACK, 0).rotate(-get_angle(self))

    def rotate_player(self):
        """Rotating the player to point where the mouse is, without using vectors"""
        mouse_x, mouse_y = pg.mouse.get_pos()
        rel_x, rel_y = mouse_x - WIDTH/2, mouse_y - HEIGHT/2
        angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
        self.image = pg.transform.rotate(self.orig_image, int(angle))
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def update(self):
        """Updates for the loop."""
        self.get_keys()
        self.pos += self.vel * self.game.dt
        self.hit_rect.centerx = self.pos.x
        sprite_collision(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        sprite_collision(self, self.game.walls, 'y')
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

################################################################################
# GLOBAL MOB FUNCTIONS
def avoid_mobs(sprite):
    for mob in sprite.game.mobs:
        if mob != sprite:
            distance = sprite.pos - mob.pos
            if 0 < distance.length() < AVOID_RADIUS:
                sprite.acc += distance.normalize()

def draw_hp(sprite):
    if sprite.hp > 0.60 * sprite.mob_hp:
        colour = GREEN
    elif sprite.hp > 0.30 * sprite.mob_hp:
        colour = YELLOW
    else:
        colour = RED
    width = int(sprite.rect.width * sprite.hp / sprite.mob_hp)
    sprite.hp_bar = pg.Rect(0, 0, width, 7)
    if sprite.hp < sprite.mob_hp:
        pg.draw.rect(sprite.image, colour, sprite.hp_bar)
    sprite.hit_rect.centerx = sprite.pos.x
    sprite_collision(sprite, sprite.game.walls, 'x')
    sprite.hit_rect.centery = sprite.pos.y
    sprite_collision(sprite, sprite.game.walls, 'y')
    sprite.rect.center = sprite.hit_rect.center

class Mob(pg.sprite.Sprite):
    """The Mob class: the mobs that chase after the player (zombie)."""

    def __init__(self, game, x, y):
        """Initialize a Mob and it's attributes."""
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = vec(x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0
        self.mob_hp = MOB_HP
        self.hp = self.mob_hp
        self.speed = choice(MOB_SPEEDS)
        self.target = game.player

    def update(self):
        """Updates the position etc for the loop."""
        target_dist = self.target.pos - self.pos
        if target_dist.length_squared() < MOB_DETECT**2:
            self.rot = target_dist.angle_to(vec(1, 0))
            self.image = pg.transform.rotate(self.game.mob_img, self.rot)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            self.acc = vec(1, 0).rotate(-self.rot)
            avoid_mobs(self)
            self.acc.scale_to_length(self.speed)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.rect.center = self.pos
        draw_hp(self)
        if self.hp <= 0:
            self.kill()
            self.game.player.zombies_killed += 1
            # killedMobPos = self.pos
            # self.game.drawBlood()

class Mob2(pg.sprite.Sprite):
    """The Mob2 class: the mobs that chase after the player (zombie)."""

    def __init__(self, game, x, y):
        """Initialize a Mob2 and it's attributes."""
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob2_img
        self.rect = self.image.get_rect()
        self.rect.center = vec(x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0
        self.mob_hp = MOB_HP2
        self.hp = self.mob_hp
        self.speed = choice(MOB_SPEEDS)

    def update(self):
        """Updates the position etc for the loop."""
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob2_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        avoid_mobs(self)
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.rect.center = self.pos
        draw_hp(self)
        if self.hp <= 0:
            self.kill()
            self.game.player.zombies_killed += 1

class Mob3(pg.sprite.Sprite):
    """The Mob2 class: the mobs that chase after the player (zombie)."""

    def __init__(self, game, x, y):
        """Initialize a Mob2 and it's attributes."""
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob3_img
        self.rect = self.image.get_rect()
        self.rect.center = vec(x, y)
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.pos = vec(x, y) * TILESIZE
        self.rect.center = self.pos
        self.rot = 0
        self.mob_hp = MOB_HP3
        self.hp = self.mob_hp
        self.speed = choice(MOB_SPEEDS)

    def update(self):
        """Updates the position etc for the loop."""
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob3_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(1, 0).rotate(-self.rot)
        avoid_mobs(self)
        self.acc.scale_to_length(self.speed)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        self.rect.center = self.pos
        draw_hp(self)
        if self.hp <= 0:
            self.kill()
            self.game.player.zombies_killed += 1

################################################################################

class Bullet(pg.sprite.Sprite):
    """The Bullet class: the bullets for the gun."""

    def __init__(self, game, pos, dir):
        """Initialize a bullet and it's attributes."""
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_img
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.pos = vec(pos)
        self.rect.center = pos
        self.hit_rect = self.rect
        spread = uniform(-GUN_SPREAD, GUN_SPREAD)
        self.vel = dir.rotate(spread) * BULLET_SPEED
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        # self.rotate_bullet()
        if pg.time.get_ticks() - self.spawn_time > BULLET_TRAVEL:
            self.kill()

################################################################################

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
