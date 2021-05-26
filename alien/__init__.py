import pygame
from pygame.sprite import Sprite


class Alien(Sprite):

    def __init__(self, upsettings, screen):
        super(Alien, self).__init__()
        self.screen = screen
        self.upsettings = upsettings

        self.image = pygame.transform.scale(pygame.image.load('alien/alien_frog1.png'), (50, 50))
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        self.x += (self.upsettings.alien_speed_factor * self.upsettings.fleet_direction)
        self.rect.x = self.x

