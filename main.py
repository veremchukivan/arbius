import random
import pygame as pg
from clasess.level import Level
from clasess.player import Player
from clasess.playerbar import playerbar
from clasess.startMenu import StartMenu
from clasess.pauseMenu import PauseMenu
from clasess.storm import Storm  # Імпортуємо клас Storm

def main_game(screen):
    """Основний ігровий цикл."""
    level = Level("map/map.tmx", screen)
    player = Player(x=1700, y=2300, speed=4, assets_path="assets")
    bar = playerbar(assets_path="assets", screen=screen)

    pause_menu = PauseMenu(screen)
    storm = Storm(assets_path="assets", screen=screen)  # Ініціалізація шторму
    clock = pg.time.Clock()

    running = True
    paused = False
    storm_timer = 0  # Лічильник часу до можливого запуску шторму

    while running:
        delta_time = clock.tick(60) / 1000.0
        storm_timer += delta_time

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f and not player.f_pressed:
                    player.f_pressed = True
                    level.handle_log_to_fire(player)
                elif event.key == pg.K_ESCAPE:  # Відкрити меню паузи
                    paused = True
            elif event.type == pg.KEYUP:
                if event.key == pg.K_f:
                    player.f_pressed = False

        # Пауза
        while paused:
            action = pause_menu.handle_events()
            if action == "resume":
                paused = False
            elif action == "exit":
                running = False
                paused = False

            screen.fill((0, 0, 0))
            pause_menu.draw()
            pg.display.flip()

        # Логіка шторму
        if not storm.is_active and storm_timer >= 15:  # Перевіряємо кожні 15 секунд
            storm_timer = 0
            storm.try_start()

        storm.update(delta_time)

        # Під час шторму
        if storm.is_active:
            fire_decay_rate = storm.get_fire_decay_rate()
            freezing_rate = storm.get_player_freezing_rate()

            # Прискорене зменшення прогресу костра
            for fire in level.fire_group:
                fire.decrease_point *=   fire_decay_rate

            # Якщо герой поза зоною освітлення, він замерзає швидше
            if not level.is_player_in_lighting_zone(player):
                player.cold_increase_amount *=  freezing_rate

        else:
            # Скидання бонусів після завершення шторму
            for fire in level.fire_group:
                fire.decrease_point = fire.decrease_interval  # Повертаємо до звичайного зменшення
            player.cold_increase_amount = player.cold_increase_amount  # Скидаємо замерзання

        # Оновлення стану гри
        in_lighting_zone = level.is_player_in_lighting_zone(player)
        player.update(level.map_width, level.map_height, delta_time, in_lighting_zone)

        level.handle_collisions(player)
        level.update(player, delta_time)
        bar.update(player.cold_progress)

        # Відображення гри
        screen.fill((0, 0, 0))
        level.render(player)
        player.draw(screen, level.camera, bar)

        # Малювання анімації шторму, якщо він активний
        if storm.is_active:
            storm.draw()

        pg.display.flip()


# Головна функція
def main():
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Arbius-fire at night")

    # Запускаємо стартове меню
    start_menu = StartMenu(screen)
    start_menu.handle_events()

    # Після виходу зі стартового меню запускається гра
    main_game(screen)

    pg.quit()


if __name__ == "__main__":
    main()
