import pygame
from settings import GREEN, BLUE, YELLOW, RED, HEIGHT

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, weapon_type):
        super().__init__()
        self.weapon_type = weapon_type
        colors = [GREEN, BLUE, YELLOW, RED]
        sizes = [(5, 15), (4, 12), (3, 10), (10, 30)]
        
        self.image = pygame.Surface(sizes[weapon_type])
        self.image.fill(colors[weapon_type])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speeds = [10, 12, 15, 8]
        self.speed = self.speeds[weapon_type]
        self.damage = [1, 1, 1, 3][weapon_type]

    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom < 0:
            self.kill()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.damage = 0.5
        self.lifetime = 30

    def update(self):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()