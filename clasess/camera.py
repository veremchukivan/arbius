import pygame

class Camera:
    def __init__(self, screen_width, screen_height, map_width, map_height, zoom):
        self.width = screen_width
        self.height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.zoom = zoom  # Масштаб (1.0 = без змін)
        self.x = 0
        self.y = 0

        self.camera_rect = pygame.Rect(0, 0, screen_width // zoom, screen_height // zoom)

    def update(self, target_rect):
        # Центруємо камеру на гравці
        self.x = target_rect.centerx - (self.width // (2 * self.zoom))
        self.y = target_rect.centery - (self.height // (2 * self.zoom))

        # Обмеження камери в межах карти
        self.x = max(0, min(self.x, self.map_width - (self.width / self.zoom)))
        self.y = max(0, min(self.y, self.map_height - (self.height / self.zoom)))

    def apply(self, rect):
        """Перетворює координати об'єкта з урахуванням камери без масштабування."""
        return pygame.Rect(
            (rect.x - self.x) * self.zoom,
            (rect.y - self.y) * self.zoom,
            rect.width * self.zoom,
            rect.height * self.zoom,
        )

    def apply_point(self, point):
        """Перетворює координати точки з урахуванням камери та масштабування."""
        return (
            (point[0] - self.x) * self.zoom,
            (point[1] - self.y) * self.zoom,
        )

    def scale_surface(self, surface):
        """Масштабує спрайт відповідно до камери."""
        width = int(surface.get_width() * self.zoom)
        height = int(surface.get_height() * self.zoom)
        return pygame.transform.scale(surface, (width, height))

    def get_visible_area(self):
        """Повертає область видимості для камери."""
        return pygame.Rect(
            self.x,
            self.y,
            self.width / self.zoom,
            self.height / self.zoom,
        )