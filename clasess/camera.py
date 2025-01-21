import pygame


class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height, zoom=1):
        self.width = screen_width
        self.height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.zoom = zoom  # Масштаб (1.0 = без змін)
        self.x = 0
        self.y = 0

    def update(self, target_rect):
        # Центруємо камеру на гравці
        self.x = target_rect.centerx - (self.width // (2 * self.zoom))
        self.y = target_rect.centery - (self.height // (2 * self.zoom))

        # Обмеження камери в межах карти
        self.x = max(0, min(self.x, self.map_width - (self.width / self.zoom)))
        self.y = max(0, min(self.y, self.map_height - (self.height / self.zoom)))

    def apply_zoom(self, pos):
        """Застосовує масштаб до позиції."""
        return (pos[0] * self.zoom, pos[1] * self.zoom)

    def scale_surface(self, surface):
        """Масштабує спрайт відповідно до камери."""
        width = int(surface.get_width() * self.zoom)
        height = int(surface.get_height() * self.zoom)
        return pygame.transform.scale(surface, (width, height))
