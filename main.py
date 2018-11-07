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
from gui import *
from time import sleep
from random import randint
from random import randrange, uniform

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
        self.map = Map(path.join(game_folder, 'map_small.txt'))
        self.player_img = pg.image.load(path.join(img_folder, PLAYER_IMG)).convert_alpha()
        self.bullet_img = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.mob2_img = pg.image.load(path.join(img_folder, MOB_IMG2)).convert_alpha()
        self.mob3_img = pg.image.load(path.join(img_folder, MOB_IMG3)).convert_alpha()
        self.pausedScreen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.pausedScreen.fill((0,0,0,180))
        # self.blood = pg.image.load(path.join(img_folder, BLOOD)).convert_alpha()
        # self.blood = pg.transform.scale(self.blood, (TILESIZE, TILESIZE))

        # self.wall_img = pg.image.load(path.join(img_folder, BG)).convert_alpha()
        # self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))

    def new(self):
        """Initilize all variables and set up for new game."""
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        for row, tiles in enumerate(self.map.map_data):
            for col, tile in enumerate(tiles):
                self.map_row = row
                self.map_col = col
                if tile == '1':
                    Wall(self, col, row)
                if tile == '2':
                    Wall2(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
                if tile == 'H':
                    Mob2(self, col, row)
                if tile == 'T':
                    Mob3(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

    def run(self):
        """Runs the game, setup conditions for when to run and when not."""
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
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
        # MOBS HITTING PLAYER
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.hp -= MOB_DAMAGE
            hit.vel = vec(0, 0)
            if self.player.hp <= 0:
                self.playing = False
            if hits:
                self.player.pos += vec(MOB_KNOCKBACK, 0).rotate(-hits[0].rot)
        # BULLET HITTING MOBS
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            hit.hp -= BULLET_DAMAGE
            hit.vel = vec(0, 0)

    # def drawBlood(self):
    #     self.screen.blit(self.blood, self.player.pos)

    def draw(self):
        """Draws things on the screen."""
        self.screen.blit(BACKGROUND, (0, 0))
        # self.screen.fill(BLACK)
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                draw_hp(sprite)
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # position = FONT.render("X: "+str(int(self.player.pos.x)), True, WHITE)
        # self.screen.blit(position, (10, 30))
        # position = FONT.render("Y: "+str(int(self.player.pos.y)), True, WHITE)
        # self.screen.blit(position, (10, 50))
        info = FONT.render("Press 'P' to pause the game.", True, WHITE)
        self.screen.blit(info, (WIDTH - 250, HEIGHT - 25))

        hpfont = FONT.render("Health: ", True, WHITE)
        self.screen.blit(hpfont, (WIDTH-190, 10))

        mouse = FONT.render("Zombies alive: "+str(len(self.mobs)), True, RED)
        self.screen.blit(mouse, (10, 30))

        fps = FONT.render("FPS: "+str(round(self.clock.get_fps(), 2)), True, GREEN)
        self.screen.blit(fps, (10, 10))

        score = FONT.render("Zombies Killed: " + str(self.player.zombies_killed), True, GREEN)
        self.screen.blit(score, (WIDTH-160, 40))

        draw_player_hp(self.screen, WIDTH-120, 10, self.player.hp / PLAYER_HP)

        if self.player.zombies_killed != self.player.zombies_killed_updated:
            x = random.randint(0, self.map_col)
            y = random.randint(0, self.map_row)
            x1 = random.randint(0, self.map_col)
            y1 = random.randint(0, self.map_row)
            self.check_col = 0
            self.check_row = 0

            for row, tiles in enumerate(self.map.map_data):
                for col, tile in enumerate(tiles):
                    if tile == '1':
                        self.check_col = col
                        self.check_row = row

            if (self.map_col, self.map_row) != (self.check_col, self.check_row):
                mob = Mob(self, x, y)
                mob2 = Mob2(self, x1, y1)

                self.mobs.add(mob)
                self.all_sprites.add(mob)
                self.mobs.add(mob2)
                self.all_sprites.add(mob2)
                self.player.zombies_killed_updated += 1

        if self.paused:
            self.screen.blit(self.pausedScreen, (0, 0))
            p_screen = FONT2.render("PAUSED!", True, GREEN)
            self.screen.blit(p_screen, (WIDTH/2 - 75, HEIGHT/2 - 20))

        pg.display.flip()

    def events(self):
        """Part of the main game loop - has game events."""
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        """Call this at the start of the game."""
        pass

    def show_go_screen(self):
        """Call this when game is over."""
        pass

# CREATE GAME OBJECT
g = Game() # MAKING AN INSTANCE OF YOUR GAME CLASS (THEN CALLING THE FUNCTIONS.)
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
# THE END #
