import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    def __init__(self , setting , screen , ship_type = ''):
        super().__init__()
        self.screen = screen
        self.setting = setting
        if ship_type:
            ship_image = pygame.image.load('images/small_ship.png')
            self.image = pygame.transform.scale(ship_image, (40, 30))
        else:
            ship_image = pygame.image.load('images/ship.png')
            self.image = pygame.transform.scale(ship_image, (80, 60))

        self.rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        self.center = float (self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        self.move_right = False
        self.move_left = False
        self.move_top = False
        self.move_bottom = False

    def blitme(self):
        self.screen.blit(self.image , self.rect)

    def update_place(self , setting):
        if self.move_left and self.rect.left > 0:
            self.center -= setting.ship_speed
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center += setting.ship_speed
        if self.move_top and self.rect.top > 0:
            self.bottom -= setting.ship_speed
        if self.move_bottom and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += setting.ship_speed

        self.rect.centerx = self.center
        self.rect.bottom = self.bottom

    def init_ship(self):
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom

class Bullet(Sprite):
    def __init__(self , setting , screen , ship):
        super().__init__()
        self.screen = screen

        self.rect = pygame.Rect(0 , 0 , setting.bullet_with , setting.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        self.y = float(self.rect.y)
        self.color = setting.bullet_color
        self.speed_factor = setting.bullet_speed_factor

    def update(self):
        self.y -= self.speed_factor
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen , self.color , self.rect)

class Alien(Sprite):
    def __init__(self , setting , screen , alien_type = ''):
        super().__init__()
        self.screen = screen
        self.setting = setting
        if alien_type:
            self.type = 'alien_pro'
            self.move_direction = 1
            alien_image = pygame.image.load('images/alien_pro.png')
            self.image = pygame.transform.scale(alien_image, (35, 35))
        else:
            self.type = ''
            alien_image = pygame.image.load('images/alien.png')
            self.image = pygame.transform.scale(alien_image, (30, 30))
        self.rect = self.image.get_rect()
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.drop_speed = setting.alien_drop_speed


    def blitme(self):
        self.screen.blit(self.image , self.rect)

    def update(self):
        self.y += self.drop_speed
        self.rect.y = self.y

    def move(self):
        self.x += (self.setting.alien_speed * self.move_direction)
        self.rect.x = self.x

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True



