# main.py
import pygame
from clasess.level import Level
from clasess.player import Player

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# Завантаження рівня
level = Level("map/map.tmx", screen)

# Створення гравця
player = Player(x=1250, y=840, width=32, height=32, speed=5, assets_path="assets", scale_factor=4)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Оновлення гравця
    player.update(level.map_width, level.map_height)

    # Оновлення рівня (камера, дерева, інші елементи)
    level.update(player)

    # Малювання
    screen.fill((0, 0, 0))  # Очистка екрану
    level.render()  # Рендеринг рівня
    player.draw(screen, level.camera)  # Малювання гравця
    pygame.display.flip()

    clock.tick(60)

pygame.quit()
