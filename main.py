from clasess.level import Level
from clasess.player import Player
from clasess.playerbar import PlayerBar
from clasess.startMenu import StartMenu
from clasess.pauseMenu import PauseMenu
from clasess.storm import Storm
from clasess.miniMap  import Minimap

import os
import sys
import pygame as pg

def main_game(game_screen):
    current_level = 0
    level = Level("map/map.tmx", game_screen, current_level)
    player = Player(x=3100, y=2700, speed=4, assets_path="assets")
    bar = PlayerBar(assets_path="assets", screen=game_screen)

    pause_menu = PauseMenu(game_screen)
    storm = Storm(assets_path="assets", screen=game_screen)
    clock = pg.time.Clock()

    # Відтворення фонового музичного супроводу гри (основна музика)
    base_path = os.path.dirname(os.path.abspath(__file__))
    game_music_path = os.path.join(base_path, "assets", "music", "game_beck_m.ogg")
    try:
        pg.mixer.music.load(game_music_path)
        pg.mixer.music.set_volume(0.1)  # Налаштування гучності (від 0.0 до 1.0)
        pg.mixer.music.play(-1)         # Відтворення у циклі
    except pg.error as e:
        print("Помилка відтворення музики гри:", e)

    storm_timer = 0
    strom_bonus = False

    # Рівні гри
    levels = [
        {"duration": 90, "freezing_rate": 3, "fire_decay_rate": 2.5},
        {"duration": 120, "freezing_rate": 3.7, "fire_decay_rate": 3},
        {"duration": 180, "freezing_rate": 4.5, "fire_decay_rate": 3.7},
    ]

    level_timer = 0  # Лічильник часу для рівня



    paused = False
    running = True

    base_freezing_rate = levels[current_level]["freezing_rate"]
    base_fire_decay_rate = levels[current_level]["fire_decay_rate"]

    minimap = Minimap(level, scale_factor=0.07, position=(0, 0))

    while running:
        delta_time = clock.tick(60) / 1000.0
        level_timer += delta_time
        storm_timer += delta_time

        # Перевіряємо, чи рівень завершився
        if level_timer >= levels[current_level]["duration"]:
            if current_level < len(levels) - 1:
                print(f"Час рівня закінчився! Переходимо на рівень {current_level + 1}")

                # Завантажуємо заставку переходу рівня
                show_level_transition(game_screen, current_level + 1)

                # Відновлюємо музику після заставки
                try:
                    pg.mixer.music.load(game_music_path)
                    pg.mixer.music.set_volume(0.1)
                    pg.mixer.music.play(-1)
                except pg.error as e:
                    print("Помилка відтворення музики гри:", e)

                # Оновлюємо рівень
                current_level += 1
                level_timer = 0  # Скидаємо таймер рівня
                apply_level_changes(level, player, levels[current_level], current_level)
                base_freezing_rate = levels[current_level]["freezing_rate"]
                base_fire_decay_rate = levels[current_level]["fire_decay_rate"]

            else:
                print("Гра завершена! Відображаємо екран перемоги.")
                show_victory_screen(game_screen)
                return

        # Перевірка смерті
        if player.is_frozen:
            show_death_screen(game_screen)
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
                        # Завантажуємо заставку переходу рівня
                        show_level_transition(game_screen, current_level + 1)
                        # Після завершення заставки повертаємо основну музику
                        try:
                            pg.mixer.music.load(game_music_path)
                            pg.mixer.music.set_volume(0.1)
                            pg.mixer.music.play(-1)
                        except pg.error as e:
                            print("Помилка відтворення музики гри:", e)
                        current_level += 1
                        level_timer = 0
                        apply_level_changes(level, player, levels[current_level], current_level)
                        base_freezing_rate = levels[current_level]["freezing_rate"]
                        base_fire_decay_rate = levels[current_level]["fire_decay_rate"]
                    else:
                        show_victory_screen(game_screen)
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

            game_screen.fill((0, 0, 0))
            pause_menu.display_menu()
            pg.display.flip()

        if not storm.is_active and storm_timer >= 15:  # Перевіряємо кожні 15 секунд
            storm_timer = 0
            storm.try_start()
        storm.update(delta_time)

        # Під час шторму
        if storm.is_active:
            fire_decay_rate = storm.get_fire_decay_rate()
            freezing_rate = storm.get_player_freezing_rate()

            if not strom_bonus:
                for fire in level.fire_group:
                    fire.decrease_point = base_fire_decay_rate + fire_decay_rate
                player.cold_increase_amount = base_freezing_rate + freezing_rate
                strom_bonus = True
        else:
            for fire in level.fire_group:
                fire.decrease_point = base_fire_decay_rate
            player.cold_increase_amount = base_freezing_rate
            strom_bonus = False

        # Оновлення стану гри
        in_lighting_zone = level.is_player_in_lighting_zone(player)
        player.update(level.map_width, level.map_height, delta_time, in_lighting_zone)
        level.handle_collisions(player)
        level.update(player, delta_time)
        bar.update(player.cold_progress)

        # Відображення гри
        game_screen.fill((0, 0, 0))
        level.render(player)
        player.draw(game_screen, level.camera, bar)

        if storm.is_active:
            storm.draw()

        if current_level < len(levels):
            draw_level_timer(game_screen, level_timer, levels[current_level]["duration"])

        minimap.draw(game_screen, player)
        pg.display.flip()

    pg.mixer.music.stop()




def apply_level_changes(level, player, level_data, current_level):
    for fire in level.fire_group:
        fire.progress = 100  # Скидаємо прогрес костра
        fire.decrease_point = level_data["fire_decay_rate"]  # Встановлюємо новий темп згасання
        fire.lighting_radius = max(70, fire.lighting_radius - (current_level * 50))  # Зменшуємо радіус освітлення
        fire.lighting_surface = fire.create_lighting_surface()  # Оновлюємо поверхню освітлення
        fire.progress_bar.update(fire.progress)  # Оновлюємо прогрес-бар костра

    player.cold_progress = 0  # Скидаємо рівень холоду
    player.cold_increase_amount = level_data["freezing_rate"]  # Встановлюємо новий темп замерзання

    level.brevno_group.empty()
    level.load_brevno_points()


def show_death_screen(game_screen):
    """Показує екран смерті, коли гравець замерзає, та відтворює відповідну музику."""
    # Формування абсолютного шляху до музичного файлу death.ogg
    base_path = os.path.dirname(os.path.abspath(__file__))
    death_music_path = os.path.join(base_path, "assets", "music", "death.ogg")

    # Завантаження та відтворення музики для екрану смерті
    try:
        pg.mixer.music.load(death_music_path)
        pg.mixer.music.set_volume(0.1)  # Гучність від 0.0 до 1.0
        pg.mixer.music.play(loops=0)  # Відтворення лише один раз (без циклу)
    except pg.error as e:
        print("Помилка відтворення музики:", e)

    # Налаштування текстових повідомлень
    font = pg.font.Font(None, 74)
    message = "Arbius is frozen..."
    instructions = "Press Enter to exit"

    # Відображення екрану смерті
    game_screen.fill((0, 0, 0))
    text = font.render(message, True, (255, 0, 0))  # Червоний текст
    sub_text = font.render(instructions, True, (200, 200, 200))
    game_screen.blit(text, (game_screen.get_width() // 2 - text.get_width() // 2, game_screen.get_height() // 2 - 100))
    game_screen.blit(sub_text, (game_screen.get_width() // 2 - sub_text.get_width() // 2, game_screen.get_height() // 2))
    pg.display.flip()

    # Очікування, поки користувач не натисне Enter
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                waiting = False



def show_victory_screen(game_screen):
    """Показує екран перемоги з анімацією кадрів від 0 до 15."""
    clock = pg.time.Clock()
    running = True

    win_frames = []
    win_path = os.path.join("assets", "win")

    base_path = os.path.dirname(os.path.abspath(__file__))
    game_music_path = os.path.join(base_path, "assets", "music", "win.ogg")
    try:
        pg.mixer.music.load(game_music_path)
        pg.mixer.music.set_volume(0.1)  # Налаштування гучності (від 0.0 до 1.0)
        pg.mixer.music.play(-1)  # -1 означає безкінечне повторення
    except pg.error as e:
        print("Помилка відтворення музики гри:", e)

    for i in range(16):
        frame_path = os.path.join(win_path, f"{i}.png")
        try:
            frame = pg.image.load(frame_path).convert_alpha()
            win_frames.append(frame)
        except Exception as e:
            print(f"Не вдалося завантажити {frame_path}: {e}")

    if not win_frames:
        raise ValueError("Не знайдено зображень у папці assets/win!")

    # Налаштування текстових повідомлень
    font = pg.font.Font(None, 74)
    message = font.render("Arbius survived! Congratulations!", True, (0, 255, 0))
    instructions = font.render("Press Enter to exit", True, (200, 200, 200))

    # Налаштування анімації
    frame_index = 0
    last_frame_time = pg.time.get_ticks()
    frame_delay = 300

    while running:
        # Обробка подій
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                running = False

        # Оновлення кадра згідно з часом
        current_time = pg.time.get_ticks()
        if current_time - last_frame_time >= frame_delay:
            frame_index = (frame_index + 1) % len(win_frames)
            last_frame_time = current_time

        # Масштабування поточного кадру під розмір екрану
        current_frame = win_frames[frame_index]
        current_frame_scaled = pg.transform.scale(current_frame, (game_screen.get_width(), game_screen.get_height()))

        # Відображення кадру та тексту
        game_screen.fill((0, 0, 0))
        game_screen.blit(current_frame_scaled, (0, 0))
        text_rect = message.get_rect(center=(game_screen.get_width() // 2, game_screen.get_height() // 2 - 100))
        instructions_rect = instructions.get_rect(center=(game_screen.get_width() // 2, game_screen.get_height() // 2))
        game_screen.blit(message, text_rect)
        game_screen.blit(instructions, instructions_rect)

        pg.display.update()
        clock.tick(60)

    pg.quit()
    sys.exit()



def draw_level_timer(game_screen, level_timer, level_duration):
    """Малює таймер рівня у правому верхньому куті."""
    font = pg.font.Font(None, 36)
    time_left = max(0, int(level_duration - level_timer))  # Час, що залишився
    timer_text = font.render(f"Час: {time_left} сек", True, (255, 255, 255))  # Білий текст
    text_rect = timer_text.get_rect(topright=(game_screen.get_width() - 20, 20))  # Правий верхній кут з відступом
    game_screen.blit(timer_text, text_rect)


def show_level_transition(game_screen, _level_number):
    """Показує заставку перед початком нового рівня."""
    clock = pg.time.Clock()

    black_screen = pg.Surface(game_screen.get_size())
    black_screen.fill((0, 0, 0))

    base_path = os.path.dirname(os.path.abspath(__file__))
    game_music_path = os.path.join(base_path, "assets", "music", "level_complate.ogg")
    try:
        pg.mixer.music.load(game_music_path)
        pg.mixer.music.set_volume(0.1)  # Налаштування гучності (від 0.0 до 1.0)
        pg.mixer.music.play(-1)  # -1 означає безкінечне повторення
    except pg.error as e:
        print("Помилка відтворення музики гри:", e)


    # Створюємо шрифт і повідомлення
    font = pg.font.Font(None, 74)
    message1 = font.render("The night is over!", True, (255, 255, 255))
    message2 = font.render("Arbius sleeps all day long", True, (255, 255, 255))

    # Центруємо повідомлення
    message1_rect = message1.get_rect(center=(game_screen.get_width() // 2, game_screen.get_height() // 2 - 40))
    message2_rect = message2.get_rect(center=(game_screen.get_width() // 2, game_screen.get_height() // 2 + 40))

    # Малюємо повідомлення на чорному екрані
    black_screen.blit(message1, message1_rect)
    black_screen.blit(message2, message2_rect)

    game_screen.blit(black_screen, (0, 0))
    pg.display.flip()

    start_ticks = pg.time.get_ticks()
    while (pg.time.get_ticks() - start_ticks) < 3000:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()

        clock.tick(60)

    #Завантаження зображень для анімації заставки з папки assets/sleepy
    sleepy_frames = []
    sleepy_path = os.path.join("assets", "sleepy")
    for filename in sorted(os.listdir(sleepy_path)):
        if filename.endswith(".png"):
            image_path = os.path.join(sleepy_path, filename)
            image = pg.image.load(image_path).convert_alpha()
            sleepy_frames.append(image)

    if not sleepy_frames:
        raise ValueError("not found")

    # 3. Анімація заставки до натискання Enter
    frame_index = 0
    frame_timer = 0.0
    animation_speed = 0.5  # Час у секундах на один кадр

    waiting = True
    while waiting:
        delta_time = clock.tick(60) / 1000.0  # Час, що минув з останнього кадру
        frame_timer += delta_time
        if frame_timer >= animation_speed:
            frame_timer = 0.0
            frame_index = (frame_index + 1) % len(sleepy_frames)

        # Масштабуємо поточний кадр заставки до розміру екрану
        current_frame = sleepy_frames[frame_index]
        current_frame_scaled = pg.transform.scale(current_frame, (game_screen.get_width(), game_screen.get_height()))
        game_screen.blit(current_frame_scaled, (0, 0))
        pg.display.flip()

        # Обробка подій
        for event in pg.event.get():
            if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                waiting = False
                break



pg.init()
screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)
pg.display.set_caption("Arbius-fire at night")

# Запускаємо стартове меню
start_menu = StartMenu(screen)
start_menu.handle_events()

# Після виходу зі стартового меню запускається гра
main_game(screen)

pg.quit()

