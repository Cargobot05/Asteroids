import sys
import pygame
import random

from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

pygame.init()
SCREEN_SIZE = (560, 560)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("ASTEROIDS")
BG_IMAGE = pygame.image.load("space.png")

WHITE = [255, 255, 255, 255]
RED = [255, 0, 0, 255]
THRUST = 2
velocity_cap = 4
global_velocity = 2

SHIP_SIZE = (32, 64)

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.image.load("ship.png")
        self.vel_x = 0
        self.vel_y = 0
        
        self.cockpit_hitbox = self.image.get_rect()
        self.cockpit_hitbox.height -= 20
        self.cockpit_hitbox.width -= 20
        self.cockpit_hitbox.center = (pos_x, pos_y)
        self.cockpit_hitbox.top -= 8
        
        self.wings_hitbox = self.image.get_rect()
        self.wings_hitbox.height -= 35
        self.wings_hitbox.center = (pos_x, pos_y)
        self.wings_hitbox.top = self.cockpit_hitbox.bottom
       
        self.rect = self.image.get_rect()
        self.rect.centerx = pos_x
        self.rect.centery = pos_y
    
    def move(self):
        self.rect.centerx += self.vel_x
        self.rect.centery += self.vel_y
        self.cockpit_hitbox.centerx += self.vel_x
        self.cockpit_hitbox.centery += self.vel_y
        self.wings_hitbox.centerx += self.vel_x
        self.wings_hitbox.centery += self.vel_y

        key = pygame.key.get_pressed()
        if (self.rect.top >= 0):
            if key[pygame.K_UP] and self.vel_y >= -velocity_cap:
                self.vel_y -= THRUST
        else: 
            self.vel_y = 0
            self.rect.top = 0
            self.cockpit_hitbox.top = 2
            self.wings_hitbox.top = self.cockpit_hitbox.bottom

        if (self.rect.bottom <= SCREEN_SIZE[0]):
            if key[pygame.K_DOWN] and self.vel_y <= velocity_cap:
                self.vel_y += THRUST
        else: 
            self.vel_y = 0
            self.rect.bottom = SCREEN_SIZE[1]
            self.wings_hitbox.bottom = SCREEN_SIZE[1] - 13
            self.cockpit_hitbox.bottom = self.wings_hitbox.top
        
        if (self.rect.left >= 0):
            if key[pygame.K_LEFT] and self.vel_x >= -velocity_cap:
                self.vel_x -= THRUST
        else: 
            self.vel_x = 0
            self.rect.left = 0
            self.wings_hitbox.left = 0
            self.cockpit_hitbox.centerx = self.wings_hitbox.centerx

        if (self.rect.right <= SCREEN_SIZE[1]):
            if key[pygame.K_RIGHT] and self.vel_x <= velocity_cap:
                self.vel_x += THRUST
        else: 
            self.vel_x = 0
            self.rect.right = SCREEN_SIZE[0]
            self.wings_hitbox.right = SCREEN_SIZE[1]
            self.cockpit_hitbox.centerx = self.wings_hitbox.centerx

    def drag(self):
        if (self.vel_x != 0): 
            if (self.vel_x > 0): self.vel_x -= 1
            else: self.vel_x += 1
        if (self.vel_y != 0):
            if (self.vel_y > 0): self.vel_y -= 1
            else: self.vel_y += 1

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, type):
        super().__init__()       
        self.image = pygame.image.load(f"asteroid_type_{type}.png")
        self.rect = self.image.get_rect()

        self.rect.centerx = pos_x
        self.rect.centery = pos_y

        rotation = random.randint(0, 3)
        if rotation == 1:
            self.image = pygame.transform.rotate(self.image, 90)
        if rotation == 2:
            self.image = pygame.transform.rotate(self.image, 180)
        if rotation == 3:
            self.image = pygame.transform.rotate(self.image, 270)


def generate(asteroid_field: pygame.sprite.Group):

    random_pick = random.randint(1, 100)
    if random_pick <= 40:
        asteroid_type = 1
    if random_pick > 40 and random_pick <= 80:
        asteroid_type = 2
    if random_pick > 80:
        asteroid_type = 3

    offset = random.randint(0, 32)
    overlap = True
    itterations = 0
    while(overlap):
        itterations += 1
        if asteroid_type == 1:
            asteroid = Asteroid(random.randint(0, SCREEN_SIZE[0]), -64 - offset, asteroid_type)
        if asteroid_type == 2:
            asteroid = Asteroid(random.randint(0, SCREEN_SIZE[0]), -64 - offset, asteroid_type)
        if asteroid_type == 3:
            asteroid = Asteroid(random.randint(0, SCREEN_SIZE[0]), -64 - offset, asteroid_type)
        if pygame.sprite.spritecollideany(asteroid, asteroid_field):
            if itterations < 512:
                overlap = True
            else:
                asteroid.kill()
                overlap = False
        else:
            overlap = False
            asteroid_field.add(asteroid)

def move_world_sprites(asteroid_field: pygame.sprite.Group):
    for asteroid in asteroid_field:
        asteroid.rect.centery += global_velocity + boost
    

ship = Ship(280, 280)

asteroid_field = pygame.sprite.Group()
for i in range(3): 
    generate(asteroid_field)
ref_asteroid = asteroid_field.sprites()[-1]

large_font = pygame.font.SysFont('Bahnschrift', 32, False, False)
medium_font = pygame.font.SysFont('Bahnschrift', 24, False, False)
small_font = pygame.font.SysFont('Bahnschrift', 16, False, False)

tutorial = True
game_start = False
game_over = False
difficulty = 3
running = True

bg_offset = 0
score = 0
high_score = 0
boost = 0

clock = pygame.time.Clock()

while running:
    key = pygame.key.get_pressed()

    if key[pygame.K_SPACE]: boost = difficulty - 1
    if not game_start:
        if key[pygame.K_1]: difficulty = 2
        if key[pygame.K_2]: difficulty = 3
        if key[pygame.K_3]: difficulty = 4
    
    global_velocity = difficulty
    velocity_cap = (difficulty-1)*2
    
    screen.fill("black")
    screen.blit(BG_IMAGE, (0, bg_offset))
    screen.blit(BG_IMAGE, (0, bg_offset - SCREEN_SIZE[1]))
    screen.blit(ship.image, (ship.rect.x, ship.rect.y))
    asteroid_field.draw(screen)

    text = medium_font.render(f"SCORE: {score}" , False, WHITE)
    backdrop_size = text.get_rect()
    backdrop = pygame.Surface([backdrop_size.width, backdrop_size.height])
    backdrop.fill("black")
    screen.blit(backdrop, [0, 0])
    screen.blit(text, [0, 0])
    
    text = medium_font.render(f"BEST: {high_score}" , False, WHITE)
    backdrop_size = text.get_rect()
    backdrop = pygame.Surface([backdrop_size.width, backdrop_size.height])
    backdrop.fill("black")
    screen.blit(backdrop, [SCREEN_SIZE[0] - backdrop_size.width, 0])
    screen.blit(text, [SCREEN_SIZE[0] - backdrop_size.width, 0])

    if game_start:
        ship.move()
        ship.drag()
        move_world_sprites(asteroid_field)
        bg_offset += global_velocity - 1 + boost
        if bg_offset >= SCREEN_SIZE[1]:
            bg_offset = 0
        
        if ref_asteroid.rect.top > 32:
            for i in range(3):
                generate(asteroid_field)
            ref_asteroid = asteroid_field.sprites()[-1]
            score += difficulty
        
        for asteroid in asteroid_field:
            if asteroid.rect.top > SCREEN_SIZE[0]:
                asteroid.kill()
            if (pygame.Rect.colliderect(ship.cockpit_hitbox, asteroid.rect)):
                game_over = True
                game_start = False
            if (pygame.Rect.colliderect(ship.wings_hitbox, asteroid.rect)):
                game_over = True
                game_start = False
        
    if game_over:
        text = large_font.render("GAME OVER", True, RED)
        backdrop_size = text.get_rect()
        backdrop = pygame.Surface([backdrop_size.width, backdrop_size.height])
        backdrop.fill("black")
        text_offset_x = backdrop_size.width // 2
        text_offset_y = backdrop_size.height // 2
        screen.blit(backdrop, [SCREEN_SIZE[0] // 2 - text_offset_x,  SCREEN_SIZE[1] // 2 - text_offset_y])
        screen.blit(text, [SCREEN_SIZE[0] // 2 - text_offset_x, SCREEN_SIZE[1] // 2- text_offset_y])
        
        text = small_font.render(f"DIFFICULTY: {difficulty - 1}", True, WHITE)
        backdrop_size = text.get_rect()
        backdrop = pygame.Surface([backdrop_size.width, backdrop_size.height])
        backdrop.fill("black")
        text_offset_x = backdrop_size.width // 2
        text_offset_y = backdrop_size.height // 2
        screen.blit(backdrop, [SCREEN_SIZE[0] // 2 - text_offset_x,  SCREEN_SIZE[1] // 2 + 2*text_offset_y])
        screen.blit(text, [SCREEN_SIZE[0] // 2 - text_offset_x, SCREEN_SIZE[1] // 2 + 2*text_offset_y])
    
    if tutorial:
        text = medium_font.render("MOVE: ARROW KEYS" , False, WHITE)
        backdrop_size = text.get_rect()
        backdrop = pygame.Surface([backdrop_size.width, backdrop_size.height])
        backdrop.fill("black")
        screen.blit(backdrop, [16, 32])
        screen.blit(text, [16, 32])

        text = medium_font.render("BOOST: SPACE" , False, WHITE)
        backdrop_size = text.get_rect()
        backdrop = pygame.Surface([backdrop_size.width, backdrop_size.height])
        backdrop.fill("black")
        screen.blit(backdrop, [16, 64])
        screen.blit(text, [16, 64])
        
        text = medium_font.render("DIFFICULTY: 1/2/3" , False, WHITE)
        backdrop_size = text.get_rect()
        backdrop = pygame.Surface([backdrop_size.width, backdrop_size.height])
        backdrop.fill("black")
        screen.blit(backdrop, [16, 96])
        screen.blit(text, [16, 96])

        text = medium_font.render("PRESS SPACE TO START" , False, WHITE)
        backdrop_size = text.get_rect()
        backdrop = pygame.Surface([backdrop_size.width, backdrop_size.height])
        backdrop.fill("black")
        screen.blit(backdrop, [16, 128])
        screen.blit(text, [16, 128])

    if key[pygame.K_SPACE]:
        if game_over == True:
            game_over = False
            game_start = True
            if score > high_score:
                high_score = score
            score = 0
            ship = Ship(280, 280)
            asteroid_field.empty()
            for i in range(3): 
                generate(asteroid_field)
            ref_asteroid = asteroid_field.sprites()[-1]
        if tutorial == True:
            tutorial = False
            game_start = True
    
    boost = 0

    pygame.display.flip()
    clock.tick(64)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()