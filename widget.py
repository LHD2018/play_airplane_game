import pygame.font
from elements import Ship
from pygame.sprite import Group

class Button():
    def __init__(self , screen , msg):
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.width , self.height = 200 , 50
        self.button_color = (0 , 255 , 0)
        self.text_color = (255 , 255 ,255)
        self.font = pygame.font.SysFont(None , 48)

        self.rect = pygame.Rect(0 , 0 , self.width , self.height)
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom - 80
        self.prep_msg(msg)

    def prep_msg(self , msg):
        self.msg_image = self.font.render(msg , True , self.text_color , self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color , self.rect)
        self.screen.blit(self.msg_image , self.msg_image_rect)



class Scoreboard():
    def __init__(self , setting , screen , stats):
        self.setting = setting
        self.stats = stats
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.score_color = (30 , 30 , 30)
        self.max_score_color = (255 , 255 , 0)
        self.font = pygame.font.SysFont(None , 48)
        self.prep_score()
        self.prep_max_score()


    def prep_score(self):
        score_str = "{:,}".format(int(self.stats.score))
        self.score_image = self.font.render(score_str , True , self.score_color  , self.setting.bg_color)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_max_score(self):
        max_score = int (self.stats.max_score)
        max_score_str = "{:,}".format(max_score)
        self.max_score_image = self.font.render(max_score_str , True , self.max_score_color , self.setting.bg_color)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.centerx = self.screen_rect.centerx
        self.max_score_rect.top = self.screen_rect.top



    def show_score(self):
        self.screen.blit(self.score_image , self.score_rect)
        self.screen.blit(self.max_score_image , self.max_score_rect)

