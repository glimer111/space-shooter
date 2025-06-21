import pygame
from game import main

if __name__ == "__main__":
    pygame.init()
    try:
        main()
    finally:
        pygame.quit()