# PRE-OPTIONS
D_1 = (800, 600)
D_2 = (640, 480)

# GAME OPTIONS & SETTINGS
TITLE = 'The Maze 【ツ】'
WIDTH = 1024
HEIGHT = int((WIDTH / 16) * 9)
SCREEN_SIZE = (D_2)
FPS = 60

TILESIZE = 32
GRIDWIDTH = SCREEN_SIZE[0]/TILESIZE
GRIDHEIGHT = SCREEN_SIZE[1]/TILESIZE

# PLAYER PROPERTIES
PLAYER_ACC = 8.0
PLAYER_FRICTION = -0.3

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SAKURA = (255, 183, 197)
LIGHTGREY = (105, 105, 105)

# FONT
import pygame as pg
pg.init()
pg.font.init()
FONT = pg.font.SysFont("None", 25)

# IMAGES
BG = pg.image.load("img/floor_small.png")
P_IMG = pg.image.load("img/player.png")
