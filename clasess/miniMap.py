import pygame as pg


class Minimap:
    def __init__(self, level, scale_factor, position):

        self.level = level
        self.scale_factor = scale_factor
        self.position = position
        self.surface = self.create_static_minimap()

    def create_static_minimap(self):

        mini_width = int(self.level.map_width * self.scale_factor)
        mini_height = int(self.level.map_height * self.scale_factor)
        minimap = pg.Surface((mini_width, mini_height))
        minimap.fill((50, 50, 50))  # Заповнюємо фон, можна змінити колір за потребою


        for sprite in self.level.minimapG:
            # Масштабуємо зображення плитки
            mini_tile = pg.transform.scale(
                sprite.image,
                (int(sprite.rect.width * self.scale_factor), int(sprite.rect.height * self.scale_factor))
            )
            # Обчислюємо позицію плитки на міні-карті
            mini_pos = (int(sprite.rect.x * self.scale_factor), int(sprite.rect.y * self.scale_factor))
            minimap.blit(mini_tile, mini_pos)

        # Можна додати і інші шари, якщо потрібно

        return minimap

    def draw(self, screen, player):

        minimap_copy = self.surface.copy()

        # Обчислюємо позицію гравця на міні-карті
        player_mini_x = int(player.rect.centerx * self.scale_factor)
        player_mini_y = int(player.rect.centery * self.scale_factor)

        # Малюємо маркер гравця (наприклад, зелений круг)
        pg.draw.circle(minimap_copy, (0, 255, 0), (player_mini_x, player_mini_y), 2)


        # Малюємо міні-карту на екрані у вказаній позиції
        screen.blit(minimap_copy, self.position)
