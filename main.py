  #Danilo bilspill
import pygame as pg
import random
from os import path
from settings import *
from sprites import *
from Tilemap import *

class Game:
    def __init__(self):
        #initialize game window, etc
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.font_name = pg.font.match_font('8-Bit-Madness')
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        img_dir = path.join(game_folder, 'Images')
        snd_dir = path.join(game_folder, 'Sound')
        music_dir = path.join(game_folder, 'Music')
        self.map = Map(path.join(game_folder, 'map.txt'))
        self.pesos_img = pg.image.load(path.join(img_dir, "PESO.png"))
        self.player_img = pg.image.load(path.join(img_dir, PLAYER_IMG)).convert_alpha()
        self.player_img_2 = pg.image.load(path.join(img_dir, PLAYER_IMG_2)).convert_alpha()
        self.player_img_3 = pg.image.load(path.join(img_dir, PLAYER_IMG)).convert_alpha()
        self.fiende_img_1 = pg.image.load(path.join(img_dir, FIENDE_IMG)).convert_alpha()
        self.fiende_img_2 = pg.image.load(path.join(img_dir, FIENDE_IMG_2)).convert_alpha()
        self.icon = pg.image.load(path.join(img_dir, "danilo uten bil 2.png"))
        self.background = pg.image.load(path.join(img_dir, "background.png"))
        self.background_rect = self.background.get_rect()
        self.c_select = pg.image.load(path.join(img_dir, "character select screen demo.png"))
        self.c_select_rect = self.c_select.get_rect()
        #sound + Music
        self.peso_sound = pg.mixer.Sound(path.join(snd_dir, 'Pickup_Coin6.wav'))
        self.dmg_sound = pg.mixer.Sound(path.join(snd_dir, 'dmg2.wav'))

    def new(self):
        # start a new game
        klasse = "0"
        self.score = 0
        self.lvl_2 = pg.sprite.Group()
        self.Peso = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                if tile == 'M':
                    Fiende(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Peso(self, col, row)
                if tile == 'E':
                    self.player = Player2(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)
        self.paused = False

        self.run()

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def update(self):
        #Game loop - update
        self.camera.update(self.player)
        hits = pg.sprite.spritecollide(self.player, self.Peso, True, False)
        for hit in hits:
            self.score += 1
            self.peso_sound.play()

        hits = pg.sprite.spritecollide(self.player, self.mobs, False)
        if hits:
            self.playing = False
            self.dmg_sound.play()

        self.all_sprites.update()
        level_2_start = pg.sprite.spritecollide(self.player, self.lvl_2, False)
        if level_2_start:
            self.map = Map(path.join(game_folder, 'map_lvl_2.txt'))

    def events(self):
        # Game Loop - events
        for event in pg.event.get():
            # check for closing window
            if event.type == pg.QUIT:
                pg.quit()
            self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    self.player.move(dx = -6)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx = 6)
                if event.key == pg.K_p:
                    self.paused = not self.paused


    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def draw(self):
        # Game Loop - draw
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(LIGHT_GREY)
        pg.display.set_icon(self.icon)
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.draw_grid()
        self.draw_text(str(self.score), 60, WHITE, WIDTH / 2, 20)
        if self.paused:
            self.draw_text("PAUSE", 100, WHITE, WIDTH / 2, HEIGHT / 2)
        #FLip the display
        pg.display.flip()

    def show_start_screen(self):
        self.screen.fill(DARK_GREY)
        self.screen.blit(self.background, self.background_rect)
        self.draw_text("use the arrow keys to move", 62, RED, WIDTH / 2, 600)
        self.draw_text("press any key to start", 62, RED, WIDTH / 2, 650)
        self.draw_text("press P to pause", 62, RED, WIDTH / 2, 550)
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        self.screen.fill(DARK_GREY)
        self.draw_text("GAME OVER", 96, WHITE, WIDTH / 2, HEIGHT / 4)
        self.draw_text("press SPACE for å begynne på nytt", 44, WHITE, WIDTH / 2, HEIGHT / 2)
        pg.display.flip()
        waiting = True
        while waiting:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        waiting = False

    def charcter_select_screen(self):
        self.screen.fill(DARK_GREY)
        self.screen.blit(self.c_select, self.c_select_rect)
        pg.draw.rect(self.screen, GREEN, (50, 650, 200, 80))
        pg.draw.rect(self.screen, GREEN, (400, 650, 200, 80))
        pg.draw.rect(self.screen, GREEN, (750, 650, 200, 80))
        self.draw_text("press 3", 60, DARK_GREEN, 850, 670)
        self.draw_text("Press 2", 60, DARK_GREEN, WIDTH / 2, 670)
        self.draw_text("press 1", 60, DARK_GREEN, 150, 670)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    pg.quit()
                if event.type == pg.KEYUP:
                    waiting = False

    def Shop_screen(self):
        self.screen.fill(LIGHT_GREY)

        pg.display.flip()

    def draw_text(self, text, size, color, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
g.charcter_select_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()
