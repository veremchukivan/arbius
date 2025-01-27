import pygame  as pg
from clasess.level import Level
from clasess.player import Player
from clasess.playerbar import playerbar
from clasess.startMenu import StartMenu
from clasess.pauseMenu import PauseMenu



def main_game(screen):
    """Основний ігровий цикл."""
    level = Level("map/map.tmx", screen)
    player = Player(x=1700, y=2300, speed=4, assets_path="assets")
    bar = playerbar(assets_path="assets", screen=screen)

    pause_menu = PauseMenu(screen)
    clock = pg.time.Clock()
    running = True

    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_f and not player.f_pressed:
                    player.f_pressed = True
                    level.handle_log_to_fire(player)
                elif event.key == pg.K_ESCAPE:  # Відкрити меню паузи
                    action = pause_menu.handle_events()
                    if action == "exit":
                        running = False
            elif event.type == pg.KEYUP:
                if event.key == pg.K_f:
                    player.f_pressed = False

        in_lighting_zone = level.is_player_in_lighting_zone(player)
        player.update(level.map_width, level.map_height, delta_time, in_lighting_zone)
        level.update(player, delta_time)
        bar.update(player.cold_progress)

        screen.fill((0, 0, 0))
        level.render(player)
        player.draw(screen, level.camera, bar)
        pg.display.flip()


# Головна функція
def main():
    pg.init()
    screen = pg.display.set_mode((1280, 720))
    pg.display.set_caption("Гра зі стартовим меню і паузою")

    # Запускаємо стартове меню
    start_menu = StartMenu(screen)
    start_menu.handle_events()

    # Після виходу зі стартового меню запускається гра
    main_game(screen)

    pg.quit()


if __name__ == "__main__":
    main()
