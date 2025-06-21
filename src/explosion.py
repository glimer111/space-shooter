import pygame
import random

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size=1):
        super().__init__()
        self.size = size
        self.images = [
            self.create_explosion_surface(i) for i in range(1, 6)
        ]
        self.image = pygame.transform.scale(self.images[0], 
                                          (int(50*size), int(50*size)))
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def create_explosion_surface(self, i):
        surf = pygame.Surface((50 + i*10, 50 + i*10), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 100 + i*20, 0), (25 + i*5, 25 + i*5), 20 + i*3)
        return surf

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.images):
                self.kill()
            else:
                center = self.rect.center
                self.image = pygame.transform.scale(self.images[self.frame], 
                                                  (int(50*self.size), int(50*self.size)))
                self.rect = self.image.get_rect()
                self.rect.center = center