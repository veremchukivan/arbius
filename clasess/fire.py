import random
import pygame as pg
import os

from clasess.firebar import Firebar

class Fire(pg.sprite.Sprite):
    def __init__(self, pos, assets_path, group, scale_factor=1.5, animation_speed=0.1, izona_radius=64, lighting_radius=150):
        super().__init__(group)
        self.scale_factor = scale_factor
        self.assets_path = os.path.join(assets_path, "fire")
        self.static_image_path = os.path.join(assets_path, "fire", "stat/ugol.png")
        self.animation_speed = animation_speed
        self.frame_index = 0
        self.izona_radius = izona_radius

        # Автоматичне встановлення lighting_radius, якщо він не переданий
        self.lighting_radius = lighting_radius

        self.progress = 100
        self.decrease_interval = 2
        self.decrease_point = 1
        self.timer = 0

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

        self.lighting_surface = self.create_lighting_surface()

    def create_lighting_surface(self):
        """Створює поверхню для зони освітлення з градієнтом."""
        surface_size = self.lighting_radius * 2
        surface = pg.Surface((surface_size, surface_size), pg.SRCALPHA)  # Прозорий шар

        center = (self.lighting_radius, self.lighting_radius)

        # Малюємо градієнтні кола (від більш світлого центру до темнішого краю)
        for i in range(10, 0, -1):  # 10 шарів градієнта
            alpha = int(64 * (i / 10))  # Прозорість змінюється від 255 до 25
            color = (255, 140, 0, alpha)
            radius = int(self.lighting_radius * (i / 10))
            pg.draw.circle(surface, color, center, radius)

        return surface

    def draw_lighting(self, surface, camera):
        """Малює зону освітлення."""
        if self.is_lighting_active and self.lighting_radius > 0:
            screen_center = camera.apply_point(self.rect.center)

            # Масштабуємо поверхню освітлення відповідно до масштабу камери
            scaled_lighting_surface = pg.transform.scale(
                self.lighting_surface,
                (int(self.lighting_radius * 2 * camera.zoom),
                 int(self.lighting_radius * 2 * camera.zoom))
            )
            lighting_rect = scaled_lighting_surface.get_rect(center=screen_center)
            surface.blit(scaled_lighting_surface, lighting_rect.topleft)

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
            raise ValueError(f"No animation frames found in {self.assets_path}")
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
            self.frame_index += self.animation_speed
            if self.frame_index >= len(self.frames):
                self.frame_index = 0
            self.image = self.frames[int(self.frame_index)]
        else:
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

        if self.progress > 1:
            self.is_lighting_active = True
            self.lighting_surface = self.create_lighting_surface()  # Оновлюємо освітлення
        else:
            self.is_lighting_active = False

    def add_progress(self):
        """Збільшує прогрес бар костра."""
        added_progress = random.randint(5, 20)
        if self.progress > 0:
            self.progress += added_progress
            if self.progress > 100:
                self.progress = 100
            self.is_lighting_active = True
            print(added_progress)

    def draw(self, surface, camera):
        """Малювання костра та його прогрес-бару."""
        # Малюємо костер
        screen_center = camera.apply_point(self.rect.center)
        scaled_image = camera.scale_surface(self.image)
        scaled_rect = scaled_image.get_rect(center=screen_center)

        # Перевіряємо, чи костер знаходиться у видимій зоні
        if surface.get_rect().colliderect(scaled_rect):
            surface.blit(scaled_image, scaled_rect.topleft)



        self.draw_lighting(surface, camera)