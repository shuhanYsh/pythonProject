import sys
import pygame
from bullet import Bullet
from alien import Alien
from random import randint
from time import sleep


def check_keydown_events(event, upsettings, screen,stats,  ship, aliens, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(upsettings, screen, ship, bullets)
    elif event.key == pygame.K_p:
        start_game(upsettings, screen, stats, ship, aliens, bullets)
    elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
        stats.save_highest_score()
        sys.exit()


def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def fire_bullet(upsettings, screen, ship, bullets):
    if len(bullets) < upsettings.bullets_allowed:
        new_bullet = Bullet(upsettings, screen, ship)
        bullets.add(new_bullet)


def check_events(upsettings, screen, stats, sb, play_button, ship, aliens, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            stats.save_highest_score()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, upsettings, screen, stats, ship, aliens, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(upsettings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(upsettings, screen, stats, sb, play_button, ship, aliens, bullets,  mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        # upsettings.intitalize_dynamic_setting()
        stats.reset_stats()
        stats.game_active = True
        sb.prep_score()
        sb.prep_highest_score()
        sb.prep_level()
        sb.prep_ships()

        aliens.empty()
        bullets.empty()

        pygame.mouse.set_visible(False)
        start_game(upsettings, screen, stats, ship, aliens, bullets)


def start_game(upsettings, screen, stats, ship, aliens, bullets):
    pygame.mouse.set_visible(False)
    stats.reset_stats()
    stats.game_active = True

    aliens.empty()
    bullets.empty()

    creat_fleet(upsettings, screen, ship, aliens)
    ship.center_ship()




def update_screen(upsettings, screen, stats, sb, ship, aliens, bullets, play_button):
    screen.fill(upsettings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    if not stats.game_active:
        play_button.draw_button()
    pygame.display.flip()


def update_bullets(upsettings, screen, stats, sb, ship, aliens, bullets):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(upsettings, screen, stats, sb, ship, aliens, bullets)


def check_bullet_alien_collisions(upsettings, screen, stats, sb, ship, aliens, bullets):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    if collisions:
        for aliens in collisions.values():
            stats.score += upsettings.alien_points * len(aliens)
            sb.prep_score()
        check_highest_score(stats, sb)

    if len(aliens) == 0:
        bullets.empty()
        upsettings.increase_speed()
        stats.level += 1
        sb.prep_level()
        creat_fleet(upsettings, screen, ship, aliens)


def update_aliens(upsettings, ship, aliens):
    check_fleet_edges(upsettings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        print("Ship hit !!!")


def get_number_aliens_x(upsettings, alien_width):
    avaliable_space_x = upsettings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(upsettings, ship_height, alien_height):
    available_space_y = (upsettings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows


def create_alien(upsettings, screen, aliens, alien_number, row_number):
    alien = Alien(upsettings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)


def creat_fleet(upsettings, screen, ship, aliens):
    alien = Alien(upsettings, screen)
    number_aliens_x = get_number_aliens_x(upsettings, alien.rect.width)
    number_rows = get_number_rows(upsettings, ship.rect.height, alien.rect.height)

    for row_number in range(randint(0, number_rows)):
        for alien_number in range(randint(0, number_aliens_x)):
            create_alien(upsettings, screen, aliens, alien_number, row_number)


def check_fleet_edges(upsettings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(upsettings, aliens)
            break


def change_fleet_direction(upsettings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += upsettings.fleet_drop_speed
    upsettings.fleet_direction *= -1


def ship_hit(upsettings, stats, screen, sb, ship, aliens, bullets):
    if stats.ships_left > 0:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        creat_fleet(upsettings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_aliens_bottoms(upsettings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(upsettings, stats, sb, screen, ship, aliens, bullets)
            break


def update_aliens(upsettings, stats, sb, screen, ship, aliens, bullets):
    check_fleet_edges(upsettings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(upsettings, stats, screen, sb, ship, aliens, bullets)

    check_aliens_bottoms(upsettings, stats, sb, screen, ship, aliens, bullets)

def check_highest_score(stats, sb):
    if stats.score > stats.highest_score:
        stats.highest_score = stats.score
        sb.prep_highest_score()