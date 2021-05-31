class Setting():
    def __init__(self):
        self.title = "Alien Invation"
        self.screen_with = 1000
        self.screen_height = 600
        self.bg_color = (230, 230, 230)
        self.ship_number = 4
        self.bullet_with = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullet_num_max = 5
        self.up_speed = 1.1
        self.upscore_speed = 1.3
        self.creat_alien_number = 8

        self.bg_music_path = 'music/bg_1.mp3'
        self.bullet_music_path = 'music/bullet.wav'
        self.hit_music_path = 'music/hit.wav'

        self.init_dynamic_setting()

    def init_dynamic_setting(self):
        self.ship_speed = 0.5
        self.bullet_speed_factor = 0.5
        self.alien_speed = 0.05
        self.alien_drop_speed = 0.05
        self.alien_point = 50

    def increase_speed(self):
        if self.ship_speed < 3:
            self.ship_speed *= self.up_speed
        self.alien_speed *= self.up_speed
        self.bullet_speed_factor *= self.up_speed
        self.alien_drop_speed *= self.up_speed
        self.alien_point *= self.upscore_speed
