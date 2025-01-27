# main.py

import pygame
from clasess.level import Level
from clasess.player import Player
from clasess.playerbar import playerbar

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

level = Level("map/map.tmx", screen)
player = Player(
    x=1700,
    y=2300,
    speed=8,
    assets_path="assets",
    scale_factor=3,
)

bar = playerbar(assets_path="assets", screen=screen)  # Ініціалізуємо HUD

running = True
while running:
    delta_time = clock.tick(60) / 1000.0  # Час у секундах, що минув з останнього кадру

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f and not player.f_pressed:
                player.f_pressed = True
                print("Клавіша 'f' натиснута")

                # Обробка додавання бревна до костра
                level.handle_log_to_fire(player)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_f:
                player.f_pressed = False

    # Визначаємо, чи гравець знаходиться в зоні освітлення
    in_lighting_zone = level.is_player_in_lighting_zone(player)

    # Оновлення логіки гравця (рух, холод, замерзання)
    player.update(level.map_width, level.map_height, delta_time, in_lighting_zone)

    # Оновлення кострів та зони освітлення
    level.update(player, delta_time)

    # Оновлення прогрес-бару HUD (відображає стан холоду)
    bar.update(player.cold_progress)

    # Обробка колізій
    level.handle_collisions(player)

    # Оновлення камери після руху гравця
    level.camera.update(player.rect)

    # Очищення екрану
    screen.fill((0, 0, 0))

    # Малюємо рівень (карта, бревна, костри тощо) та передаємо гравця
    level.render(player)

    # Малюємо гравця
    player.draw(screen, level.camera, bar)

    # Малюємо HUD поверх всіх інших елементів
    bar.draw()

    pygame.display.flip()

pygame.quit()
