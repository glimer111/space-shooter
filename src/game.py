import pygame
import sys
import os
import random
from pygame import mixer
from settings import WIDTH, HEIGHT, BLACK, WHITE, GREEN, YELLOW, RED, PURPLE, IMAGE_DIR, SOUND_DIR
from resources import load_image, load_sound, load_high_scores, save_high_scores
from button import Button
from explosion import Explosion
from player import Player
from bullet import Bullet, Laser
from enemy import Enemy
from booster import Booster

def show_menu(screen, high_scores):
    clock = pygame.time.Clock()
    title_font = pygame.font.SysFont(None, 72)
    score_font = pygame.font.SysFont(None, 36)
    
    menu_bg = load_image(os.path.join(IMAGE_DIR, "background.jpg"), (WIDTH, HEIGHT))
    
    buttons = [
        Button(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50, "Обычная", GREEN, (0, 200, 0)),
        Button(WIDTH//2 - 100, HEIGHT//2, 200, 50, "Сложная", YELLOW, (200, 200, 0)),
        Button(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50, "Экстрим", RED, (200, 0, 0)),
        Button(WIDTH//2 - 100, HEIGHT//2 + 120, 200, 50, "Выход", PURPLE, (100, 0, 100))
    ]
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        
        screen.blit(menu_bg, (0, 0))
        
        title = title_font.render("КОСМИЧЕСКИЙ ШУТЕР", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 100))
        screen.blit(title, title_rect)
        
        records = score_font.render(
            f"Рекорды: Обычная - {high_scores['normal']}, Сложная - {high_scores['hard']}, Экстрим - {high_scores['insane']}", 
            True, BLACK)
        records_rect = records.get_rect(center=(WIDTH//2, 180))
        screen.blit(records, records_rect)
        
        for button in buttons:
            button.check_hover(mouse_pos)
            button.draw(screen)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            for button in buttons:
                if button.is_clicked(mouse_pos, event):
                    if button.text == "Обычная":
                        return "normal"
                    elif button.text == "Сложная":
                        return "hard"
                    elif button.text == "Экстрим":
                        return "insane"
                    elif button.text == "Выход":
                        pygame.quit()
                        sys.exit()
        
        clock.tick(60)

def game_loop(difficulty, screen, background, player_img, enemy_images, boss_img, shoot_sounds, explosion_sounds):
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    boosters = pygame.sprite.Group()
    explosions = pygame.sprite.Group()

    player = Player(player_img)
    player.difficulty = difficulty
    all_sprites.add(player)

    enemy_spawn_timer = 0
    font = pygame.font.SysFont(None, 36)
    level_up = False
    level_up_timer = 0
    game_over = False

    running = True
    while running:
        if game_over:
            screen.blit(background, (0, 0))
            
            game_over_text = font.render(f"Игра окончена! Счёт: {player.score}", True, WHITE)
            game_over_rect = game_over_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(game_over_text, game_over_rect)
            
            restart_text = font.render("Нажмите R для рестарта или ESC для выхода", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
            screen.blit(restart_text, restart_rect)
            
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    return player.score
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        return "restart"
                    elif event.key == pygame.K_ESCAPE:
                        running = False
                        return player.score
            
            clock.tick(60)
            continue
        
        dt = clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return player.score
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    return player.score
        
        player.update()
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            new_bullets = player.shoot(shoot_sounds)
            for bullet in new_bullets:
                all_sprites.add(bullet)
                if isinstance(bullet, Laser):
                    lasers.add(bullet)
                else:
                    bullets.add(bullet)
        
        enemy_spawn_timer += 1
        spawn_rate = max(30 - player.level * 2, 10)
        
        if enemy_spawn_timer >= spawn_rate:
            enemy_spawn_timer = 0
            if random.random() < 0.8:
                enemy = Enemy(player.level, difficulty, enemy_images, boss_img)
                all_sprites.add(enemy)
                enemies.add(enemy)
        
        all_sprites.update()
        explosions.update()

        hits = pygame.sprite.groupcollide(enemies, bullets, False, True)
        for enemy, bullet_list in hits.items():
            for bullet in bullet_list:
                enemy.health -= bullet.damage
        
        for laser in lasers:
            hits = pygame.sprite.spritecollide(laser, enemies, False)
            for enemy in hits:
                enemy.health -= laser.damage
        
        for enemy in enemies:
            if enemy.health <= 0:
                explosion_size = 2 if enemy.is_boss else 1
                explosion = Explosion(enemy.rect.center, explosion_size)
                all_sprites.add(explosion)
                explosions.add(explosion)
                
                if explosion_sounds:
                    random.choice(explosion_sounds).play()
                
                player.score += enemy.score
                player.enemies_destroyed += 1
                
                if random.random() < 0.3 or enemy.is_boss:
                    types = ['speed', 'fire_rate', 'health']
                    weights = [0.3, 0.3, 0.4]
                    
                    # Если у игрока не максимальное оружие добавляется бустер оружия
                    if player.weapon_type < 3:
                        types.append('weapon')
                        # Веса с учетом бустера оружия
                        weights = [0.25, 0.25, 0.25, 0.25]  # Равные шансы
                    
                    # Для босса изменяем веса
                    if enemy.is_boss:
                        if 'weapon' in types:
                            weights = [0.1, 0.1, 0.3, 0.5]  # Больший шанс получить оружие от босса
                        else:
                            weights = [0.2, 0.2, 0.6]  # Если оружие максимальное, больше шанс получить здоровье
                    
                    booster_type = random.choices(types, weights=weights)[0]
                    booster = Booster(enemy.rect.centerx, enemy.rect.centery, booster_type)
                    all_sprites.add(booster)
                    boosters.add(booster)
                                
                enemy.kill()
        
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            for hit in hits:
                explosion = Explosion(hit.rect.center, 1.5 if hit.is_boss else 1)
                all_sprites.add(explosion)
                explosions.add(explosion)
                
                if explosion_sounds:
                    random.choice(explosion_sounds).play()
                
                damage = 20 if hit.is_boss else 10
                if player.take_damage(damage):
                    game_over = True
        
        hits = pygame.sprite.spritecollide(player, boosters, True)
        for hit in hits:
            hit.apply(player, shoot_sounds)
        
        if player.check_level_up():
            level_up = True
            level_up_timer = pygame.time.get_ticks()
        
        screen.blit(background, (0, 0))
        all_sprites.draw(screen)
        explosions.draw(screen)
        
        health_bar_width = 200
        health_ratio = player.health / player.max_health
        pygame.draw.rect(screen, RED, (10, 10, health_bar_width, 20))
        pygame.draw.rect(screen, GREEN, (10, 10, health_bar_width * health_ratio, 20))
        
        score_text = font.render(f"Счёт: {player.score}", True, BLACK)
        screen.blit(score_text, (10, 40))
        
        level_text = font.render(f"Уровень: {player.level}", True, BLACK)
        screen.blit(level_text, (10, 70))
        
        weapon_text = font.render(f"Оружие: {['Обычное', 'Двойное', 'Тройное', 'Лазер'][player.weapon_type]}", True, BLACK)
        screen.blit(weapon_text, (10, 100))
        
        if player.booster_type:
            booster_names = {
                'speed': 'Скорость',
                'fire_rate': 'Скорострельность',
                'health': 'Здоровье',
                'weapon': 'Оружие+'
            }
            booster_text = font.render(
                f"Бустер: {booster_names[player.booster_type]} ({(player.booster_time//60)+1}с)", 
                True, YELLOW)
            screen.blit(booster_text, (10, 130))
        
        if level_up and pygame.time.get_ticks() - level_up_timer < 2000:
            level_up_text = font.render(f"УРОВЕНЬ {player.level}!", True, YELLOW)
            text_rect = level_up_text.get_rect(center=(WIDTH//2, HEIGHT//2))
            screen.blit(level_up_text, text_rect)
        
        pygame.display.flip()

    return player.score

def main():
    # Инициализация экрана
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Космический Шутер")
    
    # Загрузка ресурсов
    background = load_image(os.path.join(IMAGE_DIR, "background.jpg"), (WIDTH, HEIGHT))
    player_img = load_image(os.path.join(IMAGE_DIR, "player.png"), (50, 50))
    enemy_images = [
        load_image(os.path.join(IMAGE_DIR, "vrag1.png"), (40, 40)),
        load_image(os.path.join(IMAGE_DIR, "vrag2.png"), (45, 45)),
        load_image(os.path.join(IMAGE_DIR, "vrag3.png"), (50, 50)),
        load_image(os.path.join(IMAGE_DIR, "vrag4.png"), (55, 55))
    ]
    boss_img = load_image(os.path.join(IMAGE_DIR, "vrag4.png"), (100, 100))
    
    shoot_sounds = [
        load_sound(os.path.join(SOUND_DIR, "shoot1.mp3")),
        load_sound(os.path.join(SOUND_DIR, "shoot2.mp3")),
        load_sound(os.path.join(SOUND_DIR, "shoot3.mp3"))
    ]
    
    explosion_sounds = [
        load_sound(os.path.join(SOUND_DIR, "megabooster.wav")),
        load_sound(os.path.join(SOUND_DIR, "megabooster.wav"))
    ]
    
    # Загрузка музыки
    try:
        pygame.mixer.music.load(os.path.join(SOUND_DIR, "bg_music.mp3"))
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print(f"Ошибка загрузки музыки: {e}")
    
    high_scores = load_high_scores()
    
    while True:
        difficulty = show_menu(screen, high_scores)
        
        while True:
            score = game_loop(
                difficulty, 
                screen, 
                background, 
                player_img, 
                enemy_images, 
                boss_img, 
                shoot_sounds, 
                explosion_sounds
            )
            
            if score != "restart":
                if score > high_scores[difficulty]:
                    high_scores[difficulty] = score
                    save_high_scores(high_scores)
                break