import pygame
import sys
import game_functions as gf
from setting import *
from game_stats import *
from widget import *
from elements import Ship
from pygame.sprite import Group


def run_game():
    pygame.init()
    setting = Setting()
    screen = pygame.display.set_mode((setting.screen_with, setting.screen_height))
    pygame.display.set_caption(setting.title)
    stats = GameStats(setting)
    stats.max_score = gf.get_record_score()
    gf.check_joystick(stats)


    play_button = Button(screen , 'Play Game')
    score_b = Scoreboard(setting , screen ,stats)

    ship = Ship(setting , screen)
    bullets = Group()
    aliens = Group()
    left_ships = Group()
    gf.creat_left_ships(setting , screen , stats , left_ships)


    while True:
        gf.check_event(setting , screen , stats , play_button , ship , aliens , bullets , score_b)
        if stats.game_active:
            ship.update_place(setting)
            gf.update_bullet(setting , stats , bullets , aliens , score_b)
            gf.update_aliens(setting , screen , stats , ship , aliens , bullets)
        gf.update_screen(setting , screen , stats , ship , aliens , bullets, play_button , score_b , left_ships)



run_game()