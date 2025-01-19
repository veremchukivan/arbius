# classes/camera.py
class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.x = 0
        self.y = 0

    def update(self, target_rect):
        """Оновлення позиції камери на основі прямокутника цілі (гравця)."""
        self.x = target_rect.centerx - self.screen_width // 2
        self.y = target_rect.centery - self.screen_height // 2

        # Обмеження камери в межах карти
        self.x = max(0, min(self.x, self.map_width - self.screen_width))
        self.y = max(0, min(self.y, self.map_height - self.screen_height))
