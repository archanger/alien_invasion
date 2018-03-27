from settings import Settings


class GameStats():
    """Track statistics for Alien Invasion"""
    def __init__(self, ai_settings: Settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0
        self.level = 1
        
    
    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0