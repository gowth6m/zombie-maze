#  IMPORTS AND FILES
import pygame as pg
import math
pg.init()
pg.font.init()
vec = pg.math.Vector2

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# GAME SETTINGS
TITLE = 'Zombie Maze'
WIDTH = 800
HEIGHT = int(WIDTH/4 * 3)
SCREEN_SIZE = (WIDTH, HEIGHT)
FPS = 60

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# PLAYER PROPERTIES
PLAYER_SPEED = 150
PLAYER_IMG = 'main_player.png'
PLAYER_ROT_SPEED = math.pi
PLAYER_HIT_RECT = pg.Rect(0, 0, 32, 32)

# GUN PROPERTIES
BULLET_OFFSET = vec(10, 10)
BULLET_IMG = 'bullet.png'
BULLET_SPEED = 300
BULLET_TRAVEL = 1000
BULLET_RATE = 200
KNOCKBACK = 25
GUN_SPREAD = 5

# MOB PROPERTIES
MOB_IMG = 'mob1.png'
MOB_SPEED = 50
MOB_S = 2.25
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)

# FONT
FONT = pg.font.SysFont("None", 25)

# IMAGES
BG = pg.image.load("img/thefloor.png")
# BG = "floor_small.png"
BG2 = pg.image.load("img/wall2.jpg")
BACKGROUND = pg.image.load("img/grass.jpg")
