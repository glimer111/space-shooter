import pygame
from settings import WIDTH, HEIGHT
from bullet import Bullet, Laser

class Player(pygame.sprite.Sprite):
    def __init__(self, player_img):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed = 5
        self.weapon_type = 0  
        self.shoot_delay = 300
        self.last_shot = pygame.time.get_ticks()
        self.booster_time = 0
        self.booster_type = None
        self.level = 1
        self.score = 0
        self.enemies_destroyed = 0
        self.health = 100
        self.max_health = 100
        self.weapon_level = 0
        self.difficulty = "normal"

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

        if self.booster_time > 0:
            self.booster_time -= 1
        else:
            self.reset_booster()

    def reset_booster(self):
        self.speed = 5
        self.shoot_delay = 300
        self.booster_type = None

    def shoot(self, shoot_sounds):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            
            # Проверка выхода за границы списка звуков
            if shoot_sounds and 0 <= self.weapon_type < len(shoot_sounds):
                shoot_sounds[self.weapon_type].play()
            
            bullets = []
            if self.weapon_type == 0:  # Одиночная пушка
                bullets.append(Bullet(self.rect.centerx, self.rect.top, self.weapon_type))
            elif self.weapon_type == 1:  # Двойная пушка
                bullets.append(Bullet(self.rect.left + 10, self.rect.top, self.weapon_type))
                bullets.append(Bullet(self.rect.right - 10, self.rect.top, self.weapon_type))
            elif self.weapon_type == 2:  # Тройная пушка
                bullets.append(Bullet(self.rect.left + 10, self.rect.top, self.weapon_type))
                bullets.append(Bullet(self.rect.centerx, self.rect.top, self.weapon_type))
                bullets.append(Bullet(self.rect.right - 10, self.rect.top, self.weapon_type))
            elif self.weapon_type == 3:  # Лазер
                bullets.append(Laser(self.rect.centerx, self.rect.top))
            
            return bullets
        return []

    def check_level_up(self):
        if self.enemies_destroyed >= self.level * 10:
            self.level += 1
            return True
        return False

    def take_damage(self, amount):
        self.health -= amount
        return self.health <= 0