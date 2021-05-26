import sys
import pygame
from ship import Ship
from settings import Settings
import game_functions as gf
from pygame.sprite import Group
from game_stats import GameStats
from button import Button
from game_stats import GameStats
from scoreboard import Scoreboard


def run_game():
    pygame.init()
    upsettings = Settings()
    screen = pygame.display.set_mode((upsettings.screen_width, upsettings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    play_button = Button(upsettings, screen, "Play")
    stats = GameStats(upsettings)
    sb = Scoreboard(upsettings, screen, stats)

    ship = Ship(upsettings, screen)
    bullets = Group()
    aliens = Group()
    gf.creat_fleet(upsettings, screen, ship, aliens)
    # stats.load_highest_score()

    while True:
        gf.check_events(upsettings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(upsettings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(upsettings, stats, sb, screen, ship, aliens,  bullets)
        gf.update_screen(upsettings, screen, stats, sb, ship, aliens, bullets, play_button)


run_game()
