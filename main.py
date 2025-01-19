import pygame
from clasess.level import Level
from clasess.player import Player

# Ініціалізація Pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("aribius-fire in the night")

# FPS контролер
clock = pygame.time.Clock()
FPS = 60

# Завантаження рівня
level = Level("./map/map.tmx", SCREEN)

# Створення гравця
player = Player(x=400, y=300, width=40, height=40, speed=5)

# Група спрайтів (якщо необхідно)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Оновлення
    player.update()
    level.camera.update(player.rect)

    # Малювання
    SCREEN.fill((0, 0, 0))  # Чорний фон
    level.render()  # Малюємо рівень
    player.draw(SCREEN, level.camera)  # Малюємо гравця

    pygame.display.flip()

pygame.quit()
