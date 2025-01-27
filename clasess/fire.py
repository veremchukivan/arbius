import os
import pygame as pg

class Fire(pg.sprite.Sprite):
    def __init__(self, pos, assets_path, group, scale_factor=1.5, animation_speed=0.1, izona_radius=64, lighting_radius=232):
        super().__init__(group)
        self.scale_factor = scale_factor
        self.assets_path = os.path.join(assets_path, "fire")
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.izona_radius = izona_radius  # Радіус взаємодії
        self.lighting_radius = lighting_radius  # Радіус освітлення
        self.progress = 100.0  # Початковий прогрес бару костра (100%)
        self.decrease_interval = 3.0
        self.timer = 0.0

        # Завантаження анімаційних кадрів
        self.frames = self.load_frames()

        # Завантаження прогрес-барів
        self.bar_images = self.load_bar_images(os.path.join(assets_path, "bars", "fireB"))
        self.current_bar_image = None

        # Активність освітлення
        self.is_lighting_active = True

        # Встановлення початкового зображення
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)

        # Створення маски для костра
        self.mask = pg.mask.from_surface(self.image)

        # Оновлюємо прогрес-бар відповідно до початкового стану
        self.update_bar_image()

    def load_frames(self):
        """Завантаження анімаційних кадрів з папки."""
        frames = []
        for filename in sorted(os.listdir(self.assets_path)):
            if filename.endswith('.png'):
                frame_path = os.path.join(self.assets_path, filename)
                frame_image = pg.image.load(frame_path).convert_alpha()
                if self.scale_factor != 1:
                    frame_image = pg.transform.scale(
                        frame_image,
                        (int(frame_image.get_width() * self.scale_factor),
                         int(frame_image.get_height() * self.scale_factor))
                    )
                frames.append(frame_image)
        if not frames:
            raise ValueError(f"Не знайдено жодного кадру анімації в папці {self.assets_path}")
        return frames

    def load_bar_images(self, bars_path):
        """Завантаження зображень прогрес-бару."""
        bar_images = {}
        for filename in os.listdir(bars_path):
            if filename.endswith('.png'):
                try:
                    percentage = int(filename.replace('bar.png', ''))
                    bar_image = pg.image.load(os.path.join(bars_path, filename)).convert_alpha()
                    bar_images[percentage] = bar_image
                except ValueError:
                    print(f"Не вдалося визначити відсоток з файлу {filename}")
        return bar_images

    def update(self, delta_time):
        """Оновлення кадру анімації та стану костра."""
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.frame_index = 0
        old_center = self.rect.center
        self.image = self.frames[int(self.frame_index)]
        self.rect = self.image.get_rect(center=old_center)
        self.mask = pg.mask.from_surface(self.image)

        # Якщо прогрес більше 0, зменшуємо його з часом
        self.timer += delta_time
        if self.timer >= self.decrease_interval:  # Якщо минуло 3 секунди
            self.timer = 0.0
            if self.progress > 0:
                self.progress -= 3
                if self.progress < 0:
                    self.progress = 0
                print(f"Fire progress decreased to {self.progress}%")
            if self.progress == 0:
                self.is_lighting_active = False

        self.update_bar_image()

    # Оновлюємо зображення бару

    def update_bar_image(self):
        """Оновлення зображення прогрес-бару."""
        rounded_progress = int(self.progress // 10) * 10
        if rounded_progress > 100:
            rounded_progress = 100
        elif rounded_progress < 0:
            rounded_progress = 0
        self.current_bar_image = self.bar_images.get(rounded_progress, None)

    def draw(self, surface, camera):
        """Малювання костра та його прогрес-бару."""
        # Малюємо костер
        screen_center = camera.apply_point(self.rect.center)
        scaled_image = camera.scale_surface(self.image)
        scaled_rect = scaled_image.get_rect(center=screen_center)
        surface.blit(scaled_image, scaled_rect.topleft)

        # Малюємо прогрес-бар над костром
        self.draw_progress_bar(surface, scaled_rect)

    def draw_progress_bar(self, surface, scaled_rect):
        """Малювання прогрес-бару над костром."""
        if self.current_bar_image:
            bar_width = self.current_bar_image.get_width()
            bar_height = self.current_bar_image.get_height()
            bar_x = scaled_rect.centerx - bar_width // 2
            bar_y = scaled_rect.top - bar_height - 10  # Відступ 10 пікселів над костром
            surface.blit(self.current_bar_image, (bar_x, bar_y))
