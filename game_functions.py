import sys
from time import sleep

import pygame
from pygame import Surface
from pygame.event import Event
from pygame.sprite import Group

from alien import Alien
from bullet import Bullet
from button import Button
from game_stats import GameStats
from settings import Settings
from ship import Ship


def check_events(ai_settings: Settings, screen: Surface, stats: GameStats, button: Button, ship: Ship, aliens: Group, bullets: Group):
    # Watch for keyboard and mouse events.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, stats, ship, aliens, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, button, ship, aliens, bullets, mouse_x, mouse_y)



def check_play_button(ai_settings: Settings, screen: Surface, stats: GameStats, play_button: Button, ship: Ship, aliens: Group, bullets: Group, mouse_x: int, mouse_y: int):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)
        

def start_game(ai_settings: Settings, screen: Surface, stats: GameStats, ship: Ship, aliens: Group, bullets: Group):
    ai_settings.initialize_dynamic_settings()
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    aliens.empty()
    bullets.empty()

    create_fleet(ai_settings, screen, ship, aliens)
    ship.center_ship()


def check_keydown_events(event: Event, ai_settings: Settings, screen: Surface, stats: GameStats, ship: Ship, aliens: Group, bullets: Group):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
    elif event.key == pygame.K_p:
        start_game(ai_settings, screen, stats, ship, aliens, bullets)


def check_keyup_events(event: Event, ship: Ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def update_screen(ai_settings: Settings, screen: Surface, stats: GameStats, ship: Ship, aliens: Group, bullets: Group, button: Button):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    if not stats.game_active:
        button.draw_button()
    # Make the most recently drawn screen visible.
    pygame.display.flip()


def update_bullets(ai_settings: Settings, screen: Surface, ship: Ship, aliens: Group, bullets: Group):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    
    check_bullet_alien_collisions(ai_settings, screen, ship, aliens, bullets)


def check_bullet_alien_collisions(ai_settings: Settings, screen: Surface, ship: Ship, aliens: Group, bullets: Group):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)


def fire_bullet(ai_settings: Settings, screen: Surface, ship: Ship, bullets: Group):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def get_number_rows(ai_settings: Settings, ship_height: float, alien_height: float) -> int:
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def get_number_alines_x(ai_settings: Settings, alien_width: float) -> int:
    available_space = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space / (2*alien_width))
    return number_aliens_x


def create_alien(ai_settings: Settings, screen: Surface, aliens: Group, alien_number: int, row_number: int):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def create_fleet(ai_settings: Settings, screen: Surface, ship: Ship, aliens: Group):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_alines_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def check_fleet_edges(ai_settings: Settings, aliens: Group):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def change_fleet_direction(ai_settings: Settings, aliens: Group):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings: Settings, stats: GameStats, screen: Surface, ship: Ship, aliens: Group, bullets: Group):
    if stats.ship_left > 0:
        stats.ship_left -= 1

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings: Settings, stats: GameStats, screen: Surface, ship: Ship, aliens: Group, bullets: Group):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break


def update_aliens(
    ai_settings: Settings, 
    stats: GameStats, 
    screen: Surface, 
    ship: Ship, 
    aliens: Group,
    bullets: Group
    ):

    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
    
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
