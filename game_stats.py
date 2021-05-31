class GameStats():
    def __init__(self , setting):
        self.setting = setting
        self.game_active = False
        self.max_score = 0
        self.joystick_isavailable = False
        self.reset_stats()

    def reset_stats(self):
        self.ship_left = self.setting.ship_number
        self.score = 0
        self.grade = 1
        self.break_record = False
