class Settings():
       """A class to store all settings for Alien Invasion."""
       def __init__(self):
           """Initialize the game's settings."""
           # Screen settings
           self.screen_width = 640
           self.screen_height = 480
           self.bg_color = (230, 230, 230)
           self.ship_speed_factor = 10