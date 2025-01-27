# clasess/player.py

import os
import pygame as pg

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, speed, assets_path, scale_factor=3):
        super().__init__()
        self.speed = speed
        self.scale_factor = scale_factor
        self.assets_path = os.path.join(assets_path, "player")

        # Завантажуємо всі анімації без масштабування
        self.animations = self.load_animations()

        # Початкова анімація
        self.current_animation = "down"
        self.frame_index = 0
        self.animation_speed = 0.1
        self.is_moving = False

        # Встановлюємо початковий кадр
        self.image = self.animations[self.current_animation][0]
        self.rect = self.image.get_rect(center=(x, y))  # Використовуємо центр
        self.rect = self.rect.inflate(-20, -20)  # Зменшуємо розмір rect

        # Лічильник зібраних предметів (бревно)
        self.count_wood = 0
        self.velocity = pg.math.Vector2(0, 0)

        # Атрибут для збереження піднятого бревна
        self.carried_log = None

        # Флаг для обробки натискання 'f'
        self.f_pressed = False

        # Створення маски для гравця
        self.mask = pg.mask.from_surface(self.image)

        # Атрибути для прогрес-бару та замерзання
        self.cold_progress = 0.0
        self.max_cold = 100.0
        self.cold_increase_amount = 10.0  # 10% кожні 3 секунди
        self.cold_increase_interval = 3.0  # Інтервал в секундах
        self.cold_timer = 0.0  # Таймер для збільшення холоду
        self.is_frozen = False

        # Завантаження графічного ресурсу для додаткового прогрес-бару
        self.additional_bar_images = self.load_additional_bars(os.path.join(assets_path, "bars", "playerB"))

    def load_animations(self):
        """Завантаження анімацій із папки без масштабування."""
        animations = {}
        directions = ["up", "right", "left", "down"]
        for direction in directions:
            path = os.path.join(self.assets_path, direction)
            frames = []
            for i in range(4):
                frame_path = os.path.join(path, f"{i}.png")
                if os.path.exists(frame_path):
                    frame = pg.image.load(frame_path).convert_alpha()
                    frames.append(frame)  # Не масштабуємо тут
                else:
                    print(f"Файл {frame_path} не знайдено!")
            animations[direction] = frames
        return animations

    def load_additional_bars(self, bars_path):
        """Завантаження зображень додаткового прогрес-бару."""
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

    def update_animation(self):
        """Оновлення кадру анімації."""
        if self.is_moving and not self.is_frozen:
            frames = self.animations[self.current_animation]
            self.frame_index += self.animation_speed
            if self.frame_index >= len(frames):
                self.frame_index = 0
            self.image = frames[int(self.frame_index)]
        else:
            self.image = self.animations[self.current_animation][0]

        # Оновлення маски після зміни зображення
        self.mask = pg.mask.from_surface(self.image)

    def update(self, map_width, map_height, delta_time, in_lighting_zone):
        """Оновлення позиції, анімації та прогрес-бару гравця."""
        if self.is_frozen:
            self.velocity = pg.math.Vector2(0, 0)
            self.is_moving = False
        else:
            keys = pg.key.get_pressed()
            self.velocity.x = 0
            self.velocity.y = 0
            self.is_moving = False

            if keys[pg.K_a] or keys[pg.K_LEFT]:
                self.velocity.x = -self.speed
                self.current_animation = "left"
                self.is_moving = True
            elif keys[pg.K_d] or keys[pg.K_RIGHT]:
                self.velocity.x = self.speed
                self.current_animation = "right"
                self.is_moving = True
            if keys[pg.K_w] or keys[pg.K_UP]:
                self.velocity.y = -self.speed
                self.current_animation = "up"
                self.is_moving = True
            elif keys[pg.K_s] or keys[pg.K_DOWN]:
                self.velocity.y = self.speed
                self.current_animation = "down"
                self.is_moving = True

        # Оновлення анімації
        self.update_animation()

        # Оновлення позиції
        self.rect.center += self.velocity

        # Обмеження в межах карти
        self.rect.centerx = max(self.rect.width // 2,
                                min(self.rect.centerx, map_width - self.rect.width // 2))
        self.rect.centery = max(self.rect.height // 2,
                                min(self.rect.centery, map_height - self.rect.height // 2))

        # Оновлення маски після руху
        self.mask = pg.mask.from_surface(self.image)

        # Оновлення прогрес-бару холоду
        if in_lighting_zone:
            self.decrease_cold(delta_time)
        else:
            self.increase_cold(delta_time)

    def increase_cold(self, delta_time):
        """Збільшення холоду на 10% кожні 3 секунди."""
        self.cold_timer += delta_time
        if self.cold_timer >= self.cold_increase_interval:
            self.cold_progress += self.cold_increase_amount
            self.cold_timer = 0.0
            if self.cold_progress >= self.max_cold:
                self.cold_progress = self.max_cold
                self.freeze()

    def decrease_cold(self, delta_time):
        """Зменшення холоду при знаходженні в зоні освітлення."""
        if self.cold_progress > 0 and not self.is_frozen:
            # Лінійна регенерація холоду
            warm_rate = 2.0  # Зменшення на 5% в секунду
            self.cold_progress -= warm_rate * delta_time
            if self.cold_progress < 0:
                self.cold_progress = 0.0

    def freeze(self):
        """Замороження гравця."""
        self.is_frozen = True
        print("Гравець замерз!")

    def draw(self, surface, camera, hud):
        """Малювання персонажа та його прогрес-бару."""
        if not self.is_frozen:
            # Отримати центр rect у екранних координатах
            screen_center = camera.apply_point(self.rect.center)

            # Масштабуємо зображення через камеру
            scaled_image = camera.scale_surface(self.image)

            # Отримати rect для scaled_image з центром у screen_center
            scaled_rect = scaled_image.get_rect(center=screen_center)

            # Малюємо зображення спрайта
            surface.blit(scaled_image, scaled_rect.topleft)
        else:
            # Можна додати спеціальне зображення або ефект для замерзлого стану
            pass

        # Малюємо прогрес-бар над персонажем
        self.draw_progress_bar_over_character(surface, camera)

        # Оновлюємо HUD
        hud.update(self.cold_progress)

    def draw_progress_bar_over_character(self, surface, camera):
        """Малювання прогрес-бару над персонажем."""
        # Визначаємо позицію бару над персонажем
        screen_center = camera.apply_point(self.rect.center)
        bar_y = screen_center[1] - self.rect.height // 2 - 30  # Розташування над персонажем

        # Округлення прогресу до найближчого 10%
        rounded_progress = int((self.cold_progress / self.max_cold) * 100)
        rounded_progress = (rounded_progress // 10) * 10  # Округлення до 10
        if rounded_progress > 100:
            rounded_progress = 100
        elif rounded_progress < 0:
            rounded_progress = 0

        # Отримуємо відповідне зображення для бару
        bar_image = self.additional_bar_images.get(rounded_progress)

        if bar_image:
            # Отримуємо rect для бару і центруємо його над персонажем
            bar_rect = bar_image.get_rect(center=(screen_center[0], bar_y))
            surface.blit(bar_image, bar_rect.topleft)

