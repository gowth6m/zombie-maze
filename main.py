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
    """The main game class: Contains main game loop."""

    def __init__(self):
        """Initialize the game and it's attributes."""
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(30, 30)
        self.load_data()

    def load_data(self):
        """Loads data from file, such as images etc."""
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'img')
        self.map = Map(path.join(game_folder, 'map_level1.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()

        # self.wall_img = pg.image.load(path.join(img_folder, BG)).convert_alpha()
        # self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

    def new(self):
        """Initilize all variables and set up for new game."""
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == '2':
                    Wall2(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        """Runs the game, setup conditions for when to run and when not."""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):
        """Call this when you quit the game."""
        pg.quit()
        sys.exit()

    def update(self):
        """Updates the loop for every frame, etc."""
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw(self):
        """Draws things on the screen."""
        self.screen.blit(GRASS, (0, 0))
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        rendered = FONT.render("X: "+str(int(self.player.pos.x)), True, WHITE)
        self.screen.blit(rendered, (10, 10))
        rendered = FONT.render("Y: "+str(int(self.player.pos.y)), True, WHITE)
        self.screen.blit(rendered, (10, 30))
        rendered2 = FONT.render("MousePos: "+str(pg.mouse.get_pos()), True, WHITE)
        self.screen.blit(rendered2, (10, 50))

        rendered4 = FONT.render("FPS: "+str(round(self.clock.get_fps(), 2)), True, GREEN)
        self.screen.blit(rendered4, (10, 80))

        rendered3 = FONT.render("Zombies Killed: 0", True, GREEN)
        self.screen.blit(rendered3, (WIDTH-160, 10))
        # UPDATE
        pg.display.flip()

    def events(self):
        """Part of the main game loop - has game events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    def show_start_screen(self):
        """Call this at the start of the game."""
        pass

    def show_go_screen(self):
        """Call this when game is over."""
        pass

# CREATE GAME OBJECT
g = Game() # MAKING AN INSTANCE OF YOUR GAME CLASS (THEN CALLING THE FUNCTIONS OF THE NEXT INSTANCE.)
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
