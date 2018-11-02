import pygame as pg

# PRE-OPTIONS
D_1 = (800, 600)
D_2 = (640, 480)
D_3 = (1024, int((1024 / 16) * 9))

# GAME OPTIONS & SETTINGS
TITLE = 'The Maze 【ツ】'
WIDTH = 1024
HEIGHT = int((WIDTH / 16) * 9)
SCREEN_SIZE = (D_1)
FPS = 60

# PLAYER PROPERTIES
PLAYER_ACC = 9.0
PLAYER_FRICTION = -0.25

# COLOURS
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
SAKURA = (255, 183, 197)

# FONT
FONT = pg.font.match_font('arial')
