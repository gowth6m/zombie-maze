#  IMPORTS AND FILES
import pygame as pg
import math
pg.init()
pg.font.init()

# COLOURS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# GAME SETTINGS
TITLE = 'The Maze 【ツ】'
WIDTH = 800
HEIGHT = int(WIDTH/4 * 3)
SCREEN_SIZE = (WIDTH, HEIGHT)
FPS = 60
BGCOLOR = DARKGREY

TILESIZE = 32
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# PLAYER PROPERTIES
# PLAYER_ACC = 8.0
# PLAYER_FRICTION = -0.3
PLAYER_SPEED = 150
# PLAYER_IMG = 'slime.png'
PLAYER_IMG = 'main_player.png'
PLAYER_ROT_SPEED = math.pi

# FONT
FONT = pg.font.SysFont("None", 25)

# IMAGES
BG = pg.image.load("img/floor_small.png")
P_IMG = pg.image.load("img/player.png")
GRASS = pg.image.load("img/grass.jpg")
