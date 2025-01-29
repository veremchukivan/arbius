import pygame as pg
from clasess.level import Level
from clasess.player import Player
from clasess.playerbar import playerbar
from clasess.startMenu import StartMenu
from clasess.pauseMenu import PauseMenu
from clasess.storm import Storm  # Імпортуємо клас Storm

def main_game(screen):
    """Основний ігровий цикл з підтримкою рівнів."""

    current_level= 0
    level = Level("map/map.tmx", screen,current_level)
    player = Player(x=1700, y=2300, speed=4, assets_path="assets")
    bar = playerbar(assets_path="assets", screen=screen)

    pause_menu = PauseMenu(screen)
    storm = Storm(assets_path="assets", screen=screen)
    clock = pg.time.Clock()

    # Рівні гри
    levels = [
        {"duration": 90, "freezing_rate": 1, "fire_decay_rate": 3.5},
        {"duration": 120, "freezing_rate": 3.5, "fire_decay_rate": 4.5},
        {"duration": 180, "freezing_rate": 4.2, "fire_decay_rate": 5.5},
    ]

    current_level = 0
    level_timer = 0  # Лічильник часу для рівня
    paused = False
    running = True

    while running:
        delta_time = clock.tick(60) / 1000.0
        level_timer += delta_time

        # Перехід між рівнями
        if current_level < len(levels) and level_timer >= levels[current_level]["duration"]:
            if current_level == len(levels) - 1:
                # Гравець виграв гру після третьої ночі
                show_victory_screen(screen)
                return  # Виходимо з гри після перемоги
            show_level_transition(screen, current_level + 1)
            current_level += 1
            if current_level < len(levels):
                level_timer = 0
                apply_level_changes(level, player, levels[current_level], current_level)

        # Перевірка смерті
        if player.is_frozen:
            show_death_screen(screen)
            return

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f and not player.f_pressed:
                    player.f_pressed = True
                    level.handle_log_to_fire(player)
                elif event.key == pg.K_ESCAPE:
                    paused = True
                elif event.key == pg.K_TAB:
                    if current_level < len(levels) - 1:
                        show_level_transition(screen, current_level + 1)
                        current_level += 1
                        level_timer = 0
                        apply_level_changes(level, player, levels[current_level], current_level)
                    else:
                        show_victory_screen(screen)
                        return

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
            pause_menu.display_menu()
            pg.display.flip()

        # Логіка шторму
        storm.update(delta_time)

        # Під час шторму
        if storm.is_active:
            fire_decay_rate = storm.get_fire_decay_rate()
            freezing_rate = storm.get_player_freezing_rate()

            for fire in level.fire_group:
                fire.decrease_point *= fire_decay_rate

            if not level.is_player_in_lighting_zone(player):
                player.cold_increase_amount *= freezing_rate

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

        if storm.is_active:
            storm.draw()

        # Відображення таймера рівня (перевіряємо, чи рівень ще існує)
        if current_level < len(levels):
            draw_level_timer(screen, level_timer, levels[current_level]["duration"])

        pg.display.flip()

def show_death_screen(screen):
    """Показує екран смерті, коли гравець замерзає."""
    font = pg.font.Font(None, 74)
    message = "Ви замерзли..."
    instructions = "Натисніть Enter, щоб вийти"

    screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 0, 0))  # Червоний текст
    sub_text = font.render(instructions, True, (200, 200, 200))

    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - 100))
    screen.blit(sub_text, (screen.get_width() // 2 - sub_text.get_width() // 2, screen.get_height() // 2))

    pg.display.flip()

    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                waiting = False

def show_victory_screen(screen):
    """Показує екран перемоги, якщо гравець пережив усі 3 ночі."""
    font = pg.font.Font(None, 74)
    message = "Ви вижили! Вітаємо!"
    instructions = "Натисніть Enter, щоб вийти"

    screen.fill((0, 0, 0))
    text = font.render(message, True, (0, 255, 0))  # Зелений текст (перемога)
    sub_text = font.render(instructions, True, (200, 200, 200))

    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - 100))
    screen.blit(sub_text, (screen.get_width() // 2 - sub_text.get_width() // 2, screen.get_height() // 2))

    pg.display.flip()

    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                waiting = False  # Виходимо з циклу
                pg.quit()  # Закриваємо гру
                exit()





def draw_level_timer(screen, level_timer, level_duration):
    """Малює таймер рівня у правому верхньому куті."""
    font = pg.font.Font(None, 36)
    time_left = max(0, int(level_duration - level_timer))  # Час, що залишився
    timer_text = font.render(f"Час: {time_left} сек", True, (255, 255, 255))  # Білий текст
    text_rect = timer_text.get_rect(topright=(screen.get_width() - 20, 20))  # Правий верхній кут з відступом
    screen.blit(timer_text, text_rect)


def apply_level_changes(level, player, level_data, current_level):
    """Застосовує зміни параметрів для поточного рівня."""

    for fire in level.fire_group:
        fire.progress = 100  # Скидаємо прогрес костра
        fire.decrease_point = level_data["fire_decay_rate"]  # Встановлюємо згасання костра згідно з рівнем
        fire.decrease_interval = 1  # Зробимо зменшення стабільним кожну секунду

        # Зменшуємо радіус освітлення з кожним рівнем
        fire.lighting_radius = max(232, fire.lighting_radius - (current_level * 100))
        fire.lighting_surface = fire.create_lighting_surface()  # Оновлення графічного відображення освітлення
        fire.progress_bar.update(fire.progress)  # Оновлення прогрес-бару костра

    # Оновлення швидкості замерзання персонажа
    player.cold_progress = 0  # Скидання холоду
    player.default_cold_increase = level_data["freezing_rate"]  # Базове значення
    player.cold_increase_amount = player.default_cold_increase  # Оновлення активного параметра



def show_level_transition(screen, level_number):
    """Показує заставку перед початком нового рівня."""
    font = pg.font.Font(None, 74)
    message = f"Ніч {level_number} пройдено! Вітаємо!"
    instructions = "Натисніть Enter для продовження..."

    screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 255, 255))
    sub_text = font.render(instructions, True, (200, 200, 200))

    screen.blit(text, (screen.get_width() // 2 - text.get_width() // 2, screen.get_height() // 2 - 100))
    screen.blit(sub_text, (screen.get_width() // 2 - sub_text.get_width() // 2, screen.get_height() // 2))

    pg.display.flip()

    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                waiting = False

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
