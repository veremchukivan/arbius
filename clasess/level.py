import pygame
from pytmx.util_pygame import load_pygame
import pytmx

from clasess.camera import Camera


class Level:
    def __init__(self, tmx_file, screen):
        self.screen = screen
        self.tmx_data = load_pygame(tmx_file)

        # Розміри карти
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight

        # Камера
        self.camera = Camera(screen.get_width(), screen.get_height(), self.map_width, self.map_height)





    def draw_map(self):
        """Відображення карти на екрані."""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):  # Використовуємо pytmx.TiledTileLayer
                for x, y, gid in layer:
                    tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                    if tile_image:
                        self.screen.blit(tile_image, (x * self.tmx_data.tilewidth  - self.camera.x,
                                                      (y * self.tmx_data.tileheight) - self.camera.y))

    def render(self):
        """Рендеринг карти."""
        self.draw_map()
