import pygame
import os
from settings import IMAGE_DIR, SOUND_DIR, SOUND_VOLUME, WHITE, RED

import json

def load_image(path, size=None):
    try:
        image = pygame.image.load(path)
        if size:
            image = pygame.transform.scale(image, size)
        return image.convert_alpha() if path.endswith('.png') else image.convert()
    except Exception as e:
        print(f"Ошибка загрузки {path}: {e}")
        placeholder = pygame.Surface((50, 50) if not size else size)
        placeholder.fill(RED if 'enemy' in path.lower() else WHITE)
        return placeholder

def load_sound(path):
    try:
        sound = pygame.mixer.Sound(path)
        sound.set_volume(SOUND_VOLUME)
        return sound
    except:
        print(f"Ошибка загрузки звука {path}")
        return None

def load_high_scores():
    try:
        with open('high_scores.json', 'r') as f:
            return json.load(f)
    except:
        return {"normal": 0, "hard": 0, "insane": 0}

def save_high_scores(scores):
    with open('high_scores.json', 'w') as f:
        json.dump(scores, f)