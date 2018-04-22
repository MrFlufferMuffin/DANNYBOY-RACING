import pygame
import random
import os
import math

WIDTH = 800
HEIGHT = 700
FPS = 30

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_GREEN = (34, 177, 76)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dannyboy racing")
clock = pygame.time.Clock()

#fil med bildene
Game_folder = os.path.dirname(__file__)
img_dir = os.path.join(Game_folder, 'Images')
Player_img = pygame.image.load(os.path.join(img_dir, "Danilo bil.png"))
Player_img_2 = pygame.image.load(os.path.join(img_dir, "Eivind bil.png"))
Player_img_3 = pygame.image.load(os.path.join(img_dir, "Danilo bil.png"))
Fiende_img_1 = pygame.image.load(os.path.join(img_dir, "Fiende bil 1.png"))
Fiende_img_2 = pygame.image.load(os.path.join(img_dir, "fiende 2.png"))
icon = pygame.image.load(os.path.join(img_dir, "danilo uten bil 2.png"))
#ikonet i venstre hjørne
pygame.display.set_icon(icon)
#Definerer Tekst type og draw_text

font_name = pygame.font.match_font('8-Bit-Madness')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, False, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Player_img, (100, 170))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 60
        self.speedx = 0

    #Controlls
    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_a]:
            self.speedx = -25
        if keystate[pygame.K_d]:
            self.speedx = 25
        self.rect.x += self.speedx
        if self.rect.right > WIDTH - 150:
            self.rect.right = WIDTH - 150
        if self.rect.left < 150:
            self.rect.left = 150
#mobs
class Mob(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(Fiende_img_1, (100, 160))
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 1000
        self.speedy = 12

    def update(self):
        self.rect.y += self.speedy


# Start skjerm


def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "Dannyboy Racing", 100, WIDTH / 2, HEIGHT / 8)
    draw_text(screen, "Press any key to start", 80, 400, 210)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False
# Load Graphic
background = pygame.image.load(os.path.join(img_dir, "background.png"))
background_rect = background.get_rect()
m = Mob()
m2 = Mob_2()
m3 = Mob_3()

p = Player()
p2 = Player_2()
p3 = Player_3()
# Må kanskje forandre på dette om man skal ha mulighet til å bytte karakter
#Må sikkert gi vær player en gruppe og så oppdatere gruppen om man velger den


# Game loop
L1P1 = False
game_over = True
running = True
while running:
    if game_over:

        show_go_screen()
        game_over = False
        mobs = pygame.sprite.Group()
        Players = pygame.sprite.Group()

        Level_1_P1 = pygame.sprite.Group()

        Players.add(p)

        mobs.add(m)

        #Level 1, 2 og 3 player 1
        Level_1_P1.add(m)
        Level_1_P1.add(p)

    # keep loop running at the right speed

    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():

        # check for closing window
        if event.type == pygame.QUIT:
            running = False

    # Update


    # collison
    hits = pygame.sprite.spritecollide(p, mobs, False)
    if hits:
        game_over = True
    # Draw / render
    screen.blit(background, background_rect)
    Level_1_P1.update()
    Level_1_P1.draw(screen)
    # *after* drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
