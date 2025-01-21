from pytmx.util_pygame import load_pygame
import pytmx
import pygame as pg
from clasess.camera import Camera

TILE_SIZE = 32

# Клас спрайтів
class GameSprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft=pos)


class Level:
    def __init__(self, tmx_file, screen):
        self.screen = screen
        self.tmx_data = load_pygame(tmx_file)

        # Розміри карти
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight

        # Камера
        self.camera = Camera(screen.get_width(), screen.get_height(), self.map_width, self.map_height, zoom=2)

        # Групи спрайтів
        self.water_group = pg.sprite.Group()  # Шар води
        self.base_group = pg.sprite.Group()  # Базовий шар
        self.object_group = pg.sprite.Group()  # Група дерев
        self.decore_group =  pg.sprite.Group()
        self.flower_group = pg.sprite.Group()
        self.apple_group = pg.sprite.Group()


        # Завантаження шарів і об'єктів
        self.load_tiles()
        self.load_trees()

    def load_tiles(self):
        """Завантаження тайлів із шарів карти у відповідному порядку."""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):  # Якщо це шар плиток
                if layer.name == "water":  # Шар води
                    self._load_layer_tiles(layer, self.water_group)
                elif layer.name == "base":  # Базовий шар
                    self._load_layer_tiles(layer, self.base_group)
                elif layer.name =='decore':  #
                    self._load_layer_tiles(layer, self.decore_group)
                elif layer.name =='flower':  #
                    self._load_layer_tiles(layer, self.flower_group)
                elif layer.name == 'apple':  #
                    self._load_layer_tiles(layer, self.apple_group)

    def _load_layer_tiles(self, layer, group):
        """Завантаження тайлів із заданого шару в певну групу."""
        for x, y, gid in layer:
            tile_image = self.tmx_data.get_tile_image_by_gid(gid)
            if tile_image:
                pos = (x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight)
                GameSprite(pos, tile_image, group)

    def load_trees(self):
        """Завантаження тайлів дерева із шару."""
        for layer in self.tmx_data.visible_layers:
            if layer.name == "tree":  # Пошук шару дерев
                if isinstance(layer, pytmx.TiledTileLayer):  # Переконатися, що це шар плиток
                    for x, y, gid in layer:
                        tile_image = self.tmx_data.get_tile_image_by_gid(gid)
                        if tile_image:
                            # Корекція позиції для опускання дерев
                            pos = (
                            x * self.tmx_data.tilewidth, y * self.tmx_data.tileheight - tile_image.get_height() + 20)
                            GameSprite(pos, tile_image, self.object_group)  # Додати в групу дерев

    def render(self):
        # Рендеринг шару води
        for tile in self.water_group:
            zoomed_pos = self.camera.apply_zoom((tile.rect.x - self.camera.x, tile.rect.y - self.camera.y))
            zoomed_image = self.camera.scale_surface(tile.image)
            self.screen.blit(zoomed_image, zoomed_pos)

        # Рендеринг базового шару
        for tile in self.base_group:
            zoomed_pos = self.camera.apply_zoom((tile.rect.x - self.camera.x, tile.rect.y - self.camera.y))
            zoomed_image = self.camera.scale_surface(tile.image)
            self.screen.blit(zoomed_image, zoomed_pos)

        # Рендеринг декору
        for tile in self.decore_group:
            zoomed_pos = self.camera.apply_zoom((tile.rect.x - self.camera.x, tile.rect.y - self.camera.y))
            zoomed_image = self.camera.scale_surface(tile.image)
            self.screen.blit(zoomed_image, zoomed_pos)

        # Рендеринг квітів
        for tile in self.flower_group:
            zoomed_pos = self.camera.apply_zoom((tile.rect.x - self.camera.x, tile.rect.y - self.camera.y))
            zoomed_image = self.camera.scale_surface(tile.image)
            self.screen.blit(zoomed_image, zoomed_pos)

        # Рендеринг дерев
        for obj in self.object_group:
            zoomed_pos = self.camera.apply_zoom((obj.rect.x - self.camera.x, obj.rect.y - self.camera.y))
            zoomed_image = self.camera.scale_surface(obj.image)
            self.screen.blit(zoomed_image, zoomed_pos)

        # Рендеринг яблук
        for tile in self.apple_group:
            zoomed_pos = self.camera.apply_zoom((tile.rect.x - self.camera.x, tile.rect.y - self.camera.y))
            zoomed_image = self.camera.scale_surface(tile.image)
            self.screen.blit(zoomed_image, zoomed_pos)

    def update(self, player):
        """Оновлення рівня (камери та інших елементів)."""
        # Оновлення камери, орієнтуючись на гравця
        self.camera.update(player.rect)
