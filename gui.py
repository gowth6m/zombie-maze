import pygame as pg
from settings import *

# GAME UI & HUD
def draw_player_hp(surf, x, y, p):
    if p < 0:
        pct = 0
    BAR_WIDTH = 100
    BAR_HEIGHT = 20
    fill = p * BAR_WIDTH
    outline_rect = pg.Rect(x, y, BAR_WIDTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    if p > 0.6:
        colour = GREEN
    elif p > 0.3:
        colour = YELLOW
    else:
        colour = RED
    pg.draw.rect(surf, colour, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
