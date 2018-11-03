##########################################
################ THE MAZE ################
##########################################
import pygame as pg
import sys
import random
from os import path
from settings import *
from sprites import *
from tilemap import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(30, 30)
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map_small.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()

    def new(self):
        # INIT ALL VARIABLES AND SETUP FOR NEW GAME
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        # GAME LOOP - playing = False to end game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # # GAME LOOP - update
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.screen.blit(GRASS, (0, 0))
        self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # self.all_sprites.draw(self.screen)

        # TEST CODE TO SEE COORDINATES
        rendered = FONT.render("X: "+str(int(self.player.pos.x)), True, WHITE)
        self.screen.blit(rendered, (10, 10))
        rendered = FONT.render("Y: "+str(int(self.player.pos.y)), True, WHITE)
        self.screen.blit(rendered, (10, 30))
        rendered3 = FONT.render("Wealth: 0", True, GREEN)
        self.screen.blit(rendered3, (WIDTH-100, 10))
        # UPDATE
        pg.display.flip()

    def events(self):
        # GAME LOOP - events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

# CREATE GAME OBJECT
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
