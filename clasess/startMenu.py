import sys
import os
import pygame as pg

class StartMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pg.font.Font(None, 74)
        self.running = True

        # Завантаження зображень для анімації з папки assets/start_screen
        self.background_frames = []
        start_screen_path = os.path.join("assets", "start_screen")
        for filename in sorted(os.listdir(start_screen_path)):
            if filename.endswith(".png"):
                image_path = os.path.join(start_screen_path, filename)
                image = pg.image.load(image_path).convert_alpha()
                self.background_frames.append(image)
        if not self.background_frames:
            raise ValueError("Не знайдено зображень у assets/start_screen")

        self.current_frame_index = 0
        self.frame_timer = 0.0
        self.animation_speed = 0.3

        # Ініціалізація мікшера та завантаження музики для головного меню
        try:
            pg.mixer.init()
        except pg.error as e:
            print("Помилка ініціалізації мікшера:", e)

        # Завантаження однієї пісні для головного меню
        music_file = os.path.join( "assets", "music", "start-menu.ogg")
        if music_file:
            try:
                pg.mixer.music.load(music_file)
                pg.mixer.music.set_volume(0.1)  # Гучність від 0.0 до 1.0
                pg.mixer.music.play(-1)         # Відтворення в циклі (-1)
            except pg.error as e:
                print("Помилка відтворення музики:", e)
        else:
            print("Музичний файл не знайдено:", music_file)

    def display_menu(self, delta_time):
        # Оновлення таймера анімації
        self.frame_timer += delta_time
        if self.frame_timer >= self.animation_speed:
            self.frame_timer = 0.0
            self.current_frame_index = (self.current_frame_index + 1) % len(self.background_frames)

        # Масштабування поточного кадру фону до розміру екрану
        background = self.background_frames[self.current_frame_index]
        background_scaled = pg.transform.scale(background, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background_scaled, (0, 0))
        pg.display.flip()

    def handle_events(self):
        clock = pg.time.Clock()
        while self.running:
            delta_time = clock.tick(60) / 1000.0  # Час у секундах
            self.display_menu(delta_time)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_RETURN:
                        # Натискання Enter запускає гру та зупиняє музику
                        self.running = False
                        pg.mixer.music.stop()
                    elif event.key == pg.K_ESCAPE:
                        pg.quit()
                        sys.exit()
