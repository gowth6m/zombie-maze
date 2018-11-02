##########################################
################ THE MAZE ################
##########################################
import pygame as pg
import random
import math

from settings import *
from sprites import *
from room import *

class Game:
    def __init__(self):
        # INIT WINDOW ETC
        pg.init()
        pg.mixer.init()
        self.gameDisplay = pg.display.set_mode(SCREEN_SIZE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True

    def new(self):
        # START A NEW GAME - RESET
        self.all_sprites = pg.sprite.Group()
        # self.wall = pg.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        # self.wall = Wall(20, 50)
        self.run()

    def run(self):
        # GAME LOOP
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def update(self):
        # GAME LOOP - UPDATE
        self.all_sprites.update()
        # self.message_display("SCORE")

    def events(self):
        # GAME LOOP - EVENTS
        for event in pg.event.get():
            # CHECK FOR CLOSING WINDOW
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw_grid(self):
        for x in range(0, SCREEN_SIZE[0], TILESIZE):
            pg.draw.line(self.gameDisplay, LIGHTGREY, (x, 0), (x, SCREEN_SIZE[1]))
        for y in range(0, SCREEN_SIZE[1], TILESIZE):
            pg.draw.line(self.gameDisplay, LIGHTGREY, (0, y), (SCREEN_SIZE[0], y))

    def draw(self):
        # GAME LOOP - DRAW
        self.gameDisplay.fill(BLACK)
        self.gameDisplay.blit(BG, (0, 0))
        # TEST PURPOSE ONLY
        rendered = FONT.render("X: "+str(int(self.player.pos.x)), True, WHITE)
        self.gameDisplay.blit(rendered, (10, 10))

        rendered2 = FONT.render("Y: "+str(int(self.player.pos.y)), True, WHITE)
        self.gameDisplay.blit(rendered2, (10, 35))

        rendered3 = FONT.render("Wealth: 0", True, GREEN)
        self.gameDisplay.blit(rendered3, (SCREEN_SIZE[0]/2 + 310, 10))
        # TEST PURPOSE ONLY
        self.draw_grid()
        self.all_sprites.draw(self.gameDisplay)
        pg.display.flip()

    def show_start_screen(self):
        # AT THE START OF THE GAME SCREEN
        pass

    def show_go_screen(self):
        # WHEN GAME OVER
        pass

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()
