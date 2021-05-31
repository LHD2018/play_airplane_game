import sys
import time
import pygame
import random
from elements import Bullet , Alien , Ship

pygame.init()
pygame.joystick.init()

joystick =pygame.joystick

def check_joystick(stats):
    if pygame.joystick.get_count():
        global joystick
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
        if joystick.get_init():
            stats.joystick_isavailable = True

def get_record_score():
    record_filename = 'record.txt'

    try:
        with open(record_filename) as record_file:
            lastline = record_file.readlines()[-1]
            record_score = lastline.split(' ')[-1]
            return int(record_score)
    except FileNotFoundError:
        return 0

def set_record_score(max_score):
    record_filename = 'record.txt'

    with open(record_filename , 'a') as record_file:
        record_file.write(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())) + '    ' + str(max_score) + '\n')

def check_event(setting , screen , stats , button , ship , aliens , bullets , score_b):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN and stats.game_active:
            check_keydown_event(event , ship , screen , setting , bullets)
        elif event.type == pygame.KEYUP:
           check_keyup_event(event , ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            check_mouse_click(setting ,screen , stats , button , ship , aliens , bullets , score_b)
    if stats.joystick_isavailable:
        check_joystick_down(setting ,screen , stats , ship , aliens , bullets , score_b)


def check_joystick_down(setting ,screen , stats , ship , aliens , bullets , score_b):
        buttons = joystick.get_numbuttons()
        for i in range(buttons):
            button = joystick.get_button(i)
            if i == 1 and button == 1:
                shoot_bullet(setting ,screen , ship , bullets)
            if i == 8 and button == 1:
                sys.exit()
            if i == 9 and button == 1:
                replay_game(setting , screen , stats ,ship , aliens , bullets , score_b)

        hats = joystick.get_numhats()
        for i in range(hats):
            hat = joystick.get_hat(i)
            if hat == (1, 0):
                ship.move_right = True
            if hat == (0, 1):
                ship.move_top = True
            if hat == (-1, 0):
                ship.move_left = True
            if hat == (0, -1):
                ship.move_bottom = True
            if hat == (0,0):
                ship.move_left = False
                ship.move_right = False
                ship.move_top = False
                ship.move_bottom =False


def check_keyup_event(event , ship):
    if event.key == pygame.K_RIGHT or event.key ==pygame.K_d:
        ship.move_right = False
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.move_left = False
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.move_top = False
    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.move_bottom = False

def check_keydown_event(event , ship , screen , setting , bullets):
    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
        ship.move_right = True
    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
        ship.move_left = True
    if event.key == pygame.K_UP or event.key == pygame.K_w:
        ship.move_top = True
    if event.key == pygame.K_DOWN or event.key == pygame.K_s:
        ship.move_bottom = True
    if event.key == pygame.K_SPACE:
        shoot_bullet(setting , screen , ship , bullets)
    if event.key == pygame.K_q:
        sys.exit()


#发射子弹
def shoot_bullet(setting , screen , ship , bullets):
    if len(bullets) < setting.bullet_num_max:
        new_bullet = Bullet(setting, screen, ship)
        bullets.add(new_bullet)
        play_music(setting.bullet_music_path)

def create_alien(setting , screen , aliens):
    alien = Alien(setting , screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    available_space_x = setting.screen_with - 2*alien_width
    x_aliens_number = int(available_space_x/(2*alien_width))

    random_numbers = []
    while(len(random_numbers) < setting.creat_alien_number):
        number = random.randint(1 , x_aliens_number)
        if number not in random_numbers:
            random_numbers.append(number)

    for number in random_numbers:
        if number%3:
            alien = Alien(setting , screen)
        else:
            alien = Alien(setting , screen , 'alien_pro')
        alien.x = 2 * number *(alien.rect.width)
        alien.rect.x = alien.x
        alien.rect.y = alien_height
        aliens.add(alien)


def creat_left_ships(setting , screen , stats , left_ships):
    ship = Ship(setting , screen , 'ico_ship')
    ship_width = ship.rect.width
    for left_ship_number in range(stats.ship_left):
        left_ship = Ship(setting, screen , 'ico_ship')
        left_ship.rect.x = left_ship_number * ship_width
        left_ship.rect.y = 5
        left_ships.add(left_ship)

def update_screen(setting , screen , stats , ship , aliens , bullets , play_button , score_b , left_ships):
    screen.fill(setting.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    left_ship_index = 0
    for left_ship in left_ships.sprites():
        if left_ship_index < stats.ship_left:
            left_ship.blitme()
            left_ship_index += 1
        else:
            break
    aliens.draw(screen)
    score_b.show_score()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def check_fleet_hit(setting ,stats , ship , aliens , bullets):
    hited_alien = pygame.sprite.spritecollideany(ship, aliens)
    if hited_alien:
        # 碰撞逻辑代码
        play_music(setting.hit_music_path)
        stats.ship_left -= 1
        bullets.empty()
        if stats.ship_left > 0:
            aliens.remove(hited_alien)
            ship.init_ship()
            time.sleep(1)
        else:
            stats.game_active = False
            pygame.mouse.set_visible(True)
            pause_music()
            if stats.break_record:
                set_record_score(stats.max_score)



def update_aliens(setting , screen , stats, ship , aliens , bullets):
    for alien in aliens.sprites():
        if alien.type:
            alien.move()
            if alien.check_edges():
                alien.move_direction *= -1
    aliens.update()
    if len(aliens) > 0:
        last_alien = aliens.sprites()[-1]
        if last_alien.rect.y >= (3 * last_alien.rect.height):
            create_alien(setting , screen , aliens)
    else:
        create_alien(setting , screen , aliens)
    check_fleet_hit(setting , stats , ship , aliens , bullets)
    screen_rect = screen.get_rect()
    for alien in aliens.copy():
        if alien.rect.bottom > screen_rect.bottom:
            aliens.remove(alien)
            continue
        break


def update_bullet(setting , stats , bullets , aliens , score_b):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    collisions = pygame.sprite.groupcollide(bullets, aliens , True , True)
    if collisions:
        for aliens in collisions.values():
            stats.score += (len(aliens) * setting.alien_point)
            score_b.prep_score()
            play_music(setting.hit_music_path)
        check_max_score(stats, score_b)
    if setting.alien_drop_speed < 1 and  stats.score > (10000 * stats.grade):
        setting.increase_speed()
        stats.grade += 1



def check_mouse_click(setting , screen , stats , button , ship , aliens , bullets , score_b):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if button.rect.collidepoint(mouse_x , mouse_y) and not stats.game_active:
        replay_game(setting , screen , stats ,ship , aliens ,bullets ,score_b)

def replay_game(setting , screen , stats , ship , aliens , bullets , score_b):
    setting.init_dynamic_setting()
    stats.reset_stats()
    score_b.prep_score()
    aliens.empty()
    bullets.empty()
    create_alien(setting, screen, aliens)
    ship.init_ship()

    time.sleep(0.5)
    # 隐藏光标
    pygame.mouse.set_visible(False)
    stats.game_active = True
    play_bg_music(setting.bg_music_path)

def check_max_score(stats , score_b):
    if stats.score > stats.max_score:
        stats.break_record = True
        stats.max_score = stats.score
        score_b.prep_max_score()

def play_music(path):
    pygame.mixer.init()
    sound = pygame.mixer.Sound(path)
    sound.set_volume(0.1)
    sound.play()

def play_bg_music(path):
    pygame.mixer.init()
    pygame.mixer.music.load(path)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)

def pause_music():
    pygame.mixer.music.pause()



