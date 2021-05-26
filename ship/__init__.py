import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, upsettings, screen):
        super(Ship, self).__init__()
        self.screen = screen
        self.upsettings = upsettings

        self.image = pygame.transform.scale(pygame.image.load('ship/rocket.png'), (25,50))
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        self.moving_right = False
        self.moving_left = False
        self.center = float(self.rect.centerx)

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.upsettings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.upsettings.ship_speed_factor

        self.rect.centerx = self.center

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx


