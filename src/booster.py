import pygame
from settings import BLUE, YELLOW, GREEN, PURPLE, HEIGHT

class Booster(pygame.sprite.Sprite):
    def __init__(self, x, y, type):
        super().__init__()
        self.type = type
        if type == 'speed':
            self.image = pygame.Surface((30, 30))
            self.image.fill(BLUE)
        elif type == 'fire_rate':
            self.image = pygame.Surface((30, 30))
            self.image.fill(YELLOW)
        elif type == 'health':
            self.image = pygame.Surface((30, 30))
            self.image.fill(GREEN)
        else:
            self.image = pygame.Surface((30, 30))
            self.image.fill(PURPLE)
            
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 2
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()
    
    def apply(self, player, shoot_sounds):
        if self.type == 'speed':
            player.speed = 8
            player.booster_time = 500
        elif self.type == 'fire_rate':
            player.shoot_delay = max(50, player.shoot_delay - 50)
            player.booster_time = 500
        elif self.type == 'health':
            player.health = min(player.max_health, player.health + 20)
        elif self.type == 'weapon' and player.weapon_type < 3:
            player.weapon_type += 1
            player.booster_time = 750
        
        player.booster_type = self.type
        if shoot_sounds and player.weapon_type < len(shoot_sounds):
            shoot_sounds[player.weapon_type].play()
