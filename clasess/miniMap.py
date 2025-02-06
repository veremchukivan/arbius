import pygame as pg

class Minimap:
    def __init__(self, level, scale_factor, position):
        self.level = level
        self.scale_factor = scale_factor
        self.position = position
        self.surface = self.create_static_minimap()

    def create_static_minimap(self):
        # Обчислюємо розміри міні-карти
        mini_width = int(self.level.map_width * self.scale_factor)
        mini_height = int(self.level.map_height * self.scale_factor)
        minimap = pg.Surface((mini_width, mini_height))
        minimap.fill((50, 50, 50))  # Заповнюємо фон (за бажанням змініть колір)

        # Малюємо на міні-карті статичний шар (наприклад, плитки з групи minimapG)
        for sprite in self.level.minimapG:
            # Масштабуємо зображення плитки
            mini_tile = pg.transform.scale(
                sprite.image,
                (int(sprite.rect.width * self.scale_factor),
                 int(sprite.rect.height * self.scale_factor))
            )
            # Обчислюємо позицію плитки на міні-карті
            mini_pos = (int(sprite.rect.x * self.scale_factor), int(sprite.rect.y * self.scale_factor))
            minimap.blit(mini_tile, mini_pos)

        return minimap

    def draw(self, screen, player):
        # Створюємо копію статичної міні-карти для додавання динамічних елементів
        minimap_copy = self.surface.copy()

        # Відображення маркера гравця (зелений круг)
        player_mini_x = int(player.rect.centerx * self.scale_factor)
        player_mini_y = int(player.rect.centery * self.scale_factor)
        pg.draw.circle(minimap_copy, (0, 255, 0), (player_mini_x, player_mini_y), 2)

        # Відображення бревен як маленьких червоних точок
        # Використовуємо групу бревен, яку створюємо в класі Level як brevno_group
        for log in self.level.brevno_group:
            log_mini_x = int(log.rect.centerx * self.scale_factor)
            log_mini_y = int(log.rect.centery * self.scale_factor)
            pg.draw.circle(minimap_copy, (255, 0, 0), (log_mini_x, log_mini_y), 2)

        # Малюємо міні-карту на екрані у вказаній позиції
        screen.blit(minimap_copy, self.position)
