import random
import pygame
from settings import WIDTH, HEIGHT

class Enemy(pygame.sprite.Sprite):
    def __init__(self, level, difficulty, enemy_images, boss_img):
        super().__init__()
        self.level = level
        self.difficulty = difficulty
        
        if random.random() < 0.01 and level > 3:
            self.is_boss = True
            self.type = 4
            self.image = boss_img
            self.health = 50 + level * 10
            self.speed = 1 + level * 0.1
            self.score = 500 + level * 100
        else:
            self.is_boss = False
            self.type = random.randint(0, min(level-1, 3))
            self.image = enemy_images[self.type]
            self.health = (self.type + 1) * (1 + level * 0.5)
            self.speed = (self.type + 1) * (0.5 + level * 0.1)
            self.score = (self.type + 1) * 50
        
        if difficulty == "hard":
            self.health *= 1.5
            self.speed *= 1.2
        elif difficulty == "insane":
            self.health *= 2
            self.speed *= 1.5
        
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(-150, -50)
        
        if self.is_boss:
            self.rect.width *= 2
            self.rect.height *= 2
            self.speed *= 0.7

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
            return True
        return False