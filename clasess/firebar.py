import os
import pygame as pg

class Firebar:
    def __init__(self, bars_path):
        self.bars_path = bars_path
        self.bar_images = self.load_bar_images(self.bars_path)
        self.current_bar_image = None

    @staticmethod
    def load_bar_images(bars_path):
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

    def update(self, progress):
        """Оновлення зображення прогрес-бару."""
        rounded_progress = int(progress // 10) * 10
        if rounded_progress > 100:
            rounded_progress = 100
        elif rounded_progress < 0:
            rounded_progress = 0
        self.current_bar_image = self.bar_images.get(rounded_progress, None)

    def draw(self, surface, fire_rect):
        """Малювання прогрес-бару над костром."""
        if self.current_bar_image:
            bar_width = self.current_bar_image.get_width()
            bar_height = self.current_bar_image.get_height()
            bar_x = fire_rect.centerx - bar_width // 2
            bar_y = fire_rect.top - bar_height - 10
            surface.blit(self.current_bar_image, (bar_x, bar_y))
