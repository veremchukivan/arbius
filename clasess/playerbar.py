import os
import pygame as pg

class PlayerBar(pg.sprite.Sprite):
    def __init__(self, assets_path, screen):
        super().__init__()
        self.screen = screen
        self.bars_path = os.path.join(assets_path, "bars", "playerB")
        self.bar_images = self.load_bar_images(self.bars_path)
        self.current_bar_image = self.bar_images.get(0, None)

        # Визначаємо позицію на екрані (наприклад, верхній лівий кут)
        self.bar_x = 20
        self.bar_y = 20

    @staticmethod
    def load_bar_images(bars_path):
        """Завантаження зображень додаткового прогрес-бару."""
        bar_images = {}
        for filename in os.listdir(bars_path):
            if filename.endswith('.png'):
                try:
                    # Витягуємо відсоток з назви файлу, наприклад, '10bar.png' -> 10
                    percentage_str = filename.replace('bar.png', '')
                    percentage = int(percentage_str)
                    bar_image = pg.image.load(os.path.join(bars_path, filename)).convert_alpha()
                    bar_images[percentage] = bar_image
                except ValueError:
                    print(f"Не вдалося визначити відсоток з файлу {filename}")
        return bar_images

    def update(self, progress):
        # Округлюємо прогрес до найближчого 10%
        rounded_progress = (int(progress / 10) * 10)
        if rounded_progress > 100:
            rounded_progress = 100
        elif rounded_progress < 0:
            rounded_progress = 0

        # Отримуємо відповідне зображення
        self.current_bar_image = self.bar_images.get(rounded_progress, self.bar_images.get(0, None))

    def draw(self):
        """Малювання додаткового прогрес-бару на екрані."""
        if self.current_bar_image:
            self.screen.blit(self.current_bar_image, (self.bar_x, self.bar_y))
