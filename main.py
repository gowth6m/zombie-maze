##########################
######## THE MAZE ########
##########################
import pygame as pg
import random
import math

from settings import *
from sprites import *

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
        self.player = Player()
        self.all_sprites.add(self.player)
        self.run()

    def run(self):
        # GAME LOOP
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    # font = pg.font.SysFont(None, 25)
    # def message_to_screen(self, msg, colour):
    #     screen_text = FONT.render(msg, True, colour)
    #     self.gameDisplay.blit(screen_text, [SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2])
    #
    # def draw_text(self, surf, text, size, x, y):
    #     font = pg.font.Font(FONT, size)
    #     text_surface = font.render(text, True, WHITE)
    #     text_rect = text_surface.get_rect()
    #     text_rect.midtop = (x, y)
    #     surf.blit(text_surface, text_rect)

    def update(self):
        # GAME LOOP - UPDATE
        self.all_sprites.update()
        # self.message_to_screen("TESTING", WHITE)
        # self.draw_text(self.gameDisplay, "str(score)", 18, SCREEN_SIZE[0]/2, 100)

    def events(self):
        # GAME LOOP - EVENTS
        for event in pg.event.get():
            # CHECK FOR CLOSING WINDOW
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False

    def draw(self):
        # GAME LOOP - DRAW
        self.gameDisplay.fill(BLACK)
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
