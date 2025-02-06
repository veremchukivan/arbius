import os
import pygame as pg

class Firebar:
    def __init__(self, bars_path, scale_factor=3):
        self.bars_path = bars_path
        self.scale_factor = scale_factor  # Фактор масштабування
        self.bar_images = self.load_bar_images(self.bars_path)
        self.current_bar_image = None

    def load_bar_images(self, bars_path):
        """Завантаження зображень прогрес-бару з масштабуванням."""
        bar_images = {}
        for filename in os.listdir(bars_path):
            if filename.endswith('.png'):
                try:
                    percentage = int(filename.replace('bar.png', ''))
                    bar_image = pg.image.load(os.path.join(bars_path, filename)).convert_alpha()

                    # Масштабування зображення
                    new_width = int(bar_image.get_width() * self.scale_factor)
                    new_height = int(bar_image.get_height() * self.scale_factor)
                    scaled_image = pg.transform.scale(bar_image, (new_width, new_height))

                    bar_images[percentage] = scaled_image
                except ValueError:
                    print(f"Unable to determine percentage from file {filename}")
        return bar_images


    def update(self, progress):
        """Оновлення зображення прогрес-бару."""
        rounded_progress = int(progress // 10) * 10
        if rounded_progress > 100:
            rounded_progress = 100
        elif rounded_progress < 0:
            rounded_progress = 0
        self.current_bar_image = self.bar_images.get(rounded_progress, None)


    def draw(self, surface, position):
        """Малювання прогрес-бару."""
        if self.current_bar_image:
            bar_width = self.current_bar_image.get_width()
            bar_height = self.current_bar_image.get_height()
            bar_x = position.centerx - bar_width // 2
            bar_y = position.top - bar_height - 10
            surface.blit(self.current_bar_image, (bar_x, bar_y))
