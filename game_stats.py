from settings import Settings


class GameStats():
    """Track statistics for Alien Invasion"""
    def __init__(self, ai_settings: Settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        
    
    def reset_stats(self):
        self.ship_left = self.ai_settings.ship_limit