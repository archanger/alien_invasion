import sys
from ship import Ship
from settings import Settings
import pygame
from pygame.event import Event
from pygame import Surface
from bullet import Bullet
from pygame.sprite import Group


def check_events(ai_settings: Settings, screen: Surface, ship: Ship, bullets: Group):
    # Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)


def check_keydown_events(event: Event, ai_settings: Settings, screen: Surface, ship: Ship, bullets: Group):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_events(event: Event, ship: Ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings: Settings, screen: Surface, ship: Ship, bullets: Group):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(bullets: Group):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def fire_bullet(ai_settings: Settings, screen: Surface, ship: Ship, bullets: Group):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)