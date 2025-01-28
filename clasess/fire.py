import random

import pygame as pg
import os

from clasess.firebar import Firebar

class Fire(pg.sprite.Sprite):
    def __init__(self, pos, assets_path, group, scale_factor=1.5, animation_speed=0.1, izona_radius=64,
                 lighting_radius=232):
        super().__init__(group)
        self.scale_factor = scale_factor
        self.assets_path = os.path.join(assets_path, "fire")
        self.static_image_path = os.path.join(assets_path, "fire", "stat/ugol.png")
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.izona_radius = izona_radius
        self.lighting_radius = lighting_radius
        self.progress = 100
        self.decrease_interval = 1
        self.decrease_point = 0.5
        self.timer = 0.0

        # Завантаження анімаційних кадрів
        self.frames = self.load_frames()

        # Завантаження статичного зображення
        self.static_image = self.load_static_image()

        # Ініціалізація прогрес-бару
        bars_path = os.path.join(assets_path, "bars", "fireB")
        self.progress_bar = Firebar(bars_path)

        # Активність освітлення
        self.is_lighting_active = True

        # Встановлення початкового зображення
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center=pos)
        self.visual_rect = self.rect.copy()  # Додаємо visual_rect

        # Створення маски для костра
        self.mask = pg.mask.from_surface(self.image)

        # Оновлюємо прогрес-бар відповідно до початкового стану
        self.progress_bar.update(self.progress)

    def load_frames(self):
        """Завантаження анімаційних кадрів з папки."""
        frames = []
        for filename in sorted(os.listdir(self.assets_path)):
            if filename.endswith('.png') and filename != "static.png":  # Виключаємо статичне зображення
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

    def load_static_image(self):
        """Завантаження статичного зображення для костра."""
        if os.path.exists(self.static_image_path):
            static_image = pg.image.load(self.static_image_path).convert_alpha()
            if self.scale_factor != 1:
                static_image = pg.transform.scale(
                    static_image,
                    (int(static_image.get_width() * self.scale_factor),
                     int(static_image.get_height() * self.scale_factor))
                )
            return static_image
        else:
            raise FileNotFoundError(f"Не знайдено статичного зображення: {self.static_image_path}")

    def update(self, delta_time):
        """Оновлення кадру анімації та стану костра."""
        if self.progress > 1:
            # Оновлюємо анімацію, якщо прогрес > 0
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]
        else:
            # Переключаємо на статичне зображення, якщо прогрес == 0
            self.image = self.static_image
            self.is_lighting_active = False

        old_center = self.rect.center
        self.rect = self.image.get_rect(center=old_center)
        self.mask = pg.mask.from_surface(self.image)

        # Якщо прогрес більше 0, зменшуємо його з часом
        self.timer += delta_time
        if self.timer >= self.decrease_interval:
            self.timer = 0.0
            if self.progress > 0:
                self.progress -= self.decrease_point
                if self.progress < 0:
                    self.progress = 0

        # Оновлюємо прогрес-бар
        self.progress_bar.update(self.progress)

    def draw(self, surface, camera):
        """Малювання костра та його прогрес-бару."""
        # Малюємо костер
        screen_center = camera.apply_point(self.rect.center)
        scaled_image = camera.scale_surface(self.image)
        scaled_rect = scaled_image.get_rect(center=screen_center)

        # Перевіряємо, чи костер знаходиться у видимій зоні
        if surface.get_rect().colliderect(scaled_rect):
            surface.blit(scaled_image, scaled_rect.topleft)

            # Малюємо прогрес-бар над костром, якщо прогрес більше 0
            if self.progress > 0:
                self.progress_bar.draw(surface, scaled_rect)

    def add_progress(self):
        """Збільшує прогрес бар на основі відстані до костра."""

        added_progress = random.randint(1,20)
        if self.progress >0:
            self.progress += added_progress
            if self.progress > 100:
                self.progress = 100
            self.is_lighting_active = True
            print(added_progress)


