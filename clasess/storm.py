import pygame as pg
import os
import random


class Storm:
    def __init__(self, assets_path, screen):
        self.is_active = False  # Чи активний шторм
        self.duration = 6  # Тривалість шторму в секундах
        self.timer = 0  # Таймер для відстеження тривалості шторму
        self.frame_index = 0  # Поточний кадр анімації
        self.animation_speed = 0.1  # Швидкість анімації
        self.screen = screen  # Екран для малювання
        self.frames = self.load_frames(os.path.join(assets_path, "storm"))  # Завантаження кадрів
        self.opacity = 150  # Прозорість (0-255), де 150 приблизно 60%

        # Бонуси для костра та гравця під час шторму
        self.fire_decay_bonus = 0  # Додаткове зменшення прогресу костра
        self.player_freezing_bonus = 0  # Додаткове замерзання гравця

    def load_frames(self, folder_path):
        """Завантажує кадри анімації шторму з папки."""
        frames = []
        for filename in sorted(os.listdir(folder_path)):
            if filename.endswith(".png"):
                frame_path = os.path.join(folder_path, filename)
                frame_image = pg.image.load(frame_path).convert_alpha()
                frames.append(frame_image)
        if not frames:
            raise ValueError(f"Не знайдено кадрів у папці {folder_path}")
        return frames


    def try_start(self):
        """Спроба запустити шторм з 45% шансом."""
        if random.random() <= 0.45:
            self.start()


    def start(self):
        """Початок шторму."""
        self.is_active = True
        self.timer = 0
        self.frame_index = 0

        # Встановлюємо бонуси для костра та гравця
        self.fire_decay_bonus = random.randint(2, 4)
        self.player_freezing_bonus = random.randint(2, 4)
        print(f"Шторм почався! Бонуси: Fire - {self.fire_decay_bonus}, Player - {self.player_freezing_bonus}")


    def stop(self):
        """Зупинка шторму та скидання бонусів."""
        self.is_active = False
        self.fire_decay_bonus = 0  # Скидання бонусу костра
        self.player_freezing_bonus = 0  # Скидання бонусу гравця
        print("Шторм закінчився!")


    def update(self, delta_time):
        """Оновлення стану шторму."""
        if self.is_active:
            # Оновлення таймера
            self.timer += delta_time
            if self.timer >= self.duration:
                self.stop()  # Завершення шторму
            else:
                # Оновлення анімації
                self.frame_index += self.animation_speed
                if self.frame_index >= len(self.frames):
                    self.frame_index = 0


    def draw(self):
        """Малювання анімації шторму."""
        if self.is_active:
            current_frame = self.frames[int(self.frame_index)]
            scaled_frame = pg.transform.scale(current_frame, self.screen.get_size())
            scaled_frame.set_alpha(self.opacity)
            self.screen.blit(scaled_frame, (0, 0))


    def get_fire_decay_rate(self):
        """Додатковий відсоток зменшення прогресу багаття під час шторму."""
        return self.fire_decay_bonus if self.is_active else 0

    def get_player_freezing_rate(self):
        """Додатковий відсоток замерзання гравця під час шторму."""
        return self.player_freezing_bonus if self.is_active else 0
