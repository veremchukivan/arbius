import random
import pygame as pg
from pytmx.util_pygame import load_pygame
import pytmx

from clasess.camera import Camera
from clasess.fire import Fire


class GameSprite(pg.sprite.Sprite):
    def __init__(self, pos, surf, group):
        super().__init__(group)
        self.image = surf
        self.visual_rect = self.image.get_rect(topleft=pos)
        self.rect = self.image.get_rect(topleft=pos)

        # Створення маски для спрайта
        self.mask = pg.mask.from_surface(self.image)

        # Отримання обмежуючого rect з маски
        mask_rects = self.mask.get_bounding_rects()
        if mask_rects:
            mask_rect = mask_rects[0]
            # Зберігаємо офсет відносно візуального прямокутника
            self.mask_offset = (mask_rect.left, mask_rect.top)
            # Коригуємо прямокутник для колізій (але не змінюємо self.visual_rect)
            self.rect = pg.Rect(
                self.visual_rect.left + mask_rect.left,
                self.visual_rect.top + mask_rect.top,
                mask_rect.width,
                mask_rect.height
            )
        else:
            self.mask_offset = (0, 0)


class Level:
    def __init__(self, tmx_file, screen, current_level=0, assets_path="assets"):
        self.screen = screen
        self.tmx_data = load_pygame(tmx_file)
        self.assets_path = assets_path
        self.current_level = current_level  # Збереження рівня всередині об'єкта

        # Розміри карти
        self.map_width = self.tmx_data.width * self.tmx_data.tilewidth
        self.map_height = self.tmx_data.height * self.tmx_data.tileheight

        # Камера
        self.camera = Camera(screen.get_width(), screen.get_height(), self.map_width, self.map_height, zoom=3.5)

        # Групи спрайтів
        self.water_group = pg.sprite.Group()
        self.base_group = pg.sprite.Group()
        self.decore_group = pg.sprite.Group()
        self.flower_group = pg.sprite.Group()
        self.apple_group = pg.sprite.Group()
        self.swamp_group = pg.sprite.Group()



        # Object group
        self.tree_group = pg.sprite.Group()
        self.brevno_group = pg.sprite.Group()
        self.fire_group = pg.sprite.Group()


        # Завантаження об'єктів
        self.load_tiles()
        self.load_trees()
        self.load_brevno_points()
        self.load_fire()  # Передаємо рівень у `load_fire`

        # Колізійна група
        self.collision_group = pg.sprite.Group()
        self.collision_group.add(*self.water_group, *self.decore_group, *self.tree_group, *self.fire_group)

        #minimap_group
        self.minimapG=pg.sprite.Group()
        self.minimapG.add(*self.water_group,*self.base_group,*self.swamp_group,*self.fire_group)

    def updatef(self,delta_time):
        for fire in self.fire_group:
            fire.update(delta_time)


    def load_brevno_points(self):
        """Завантаження об'єктів з name='brevno' з карти із зменшенням кількості бревен з кожним рівнем."""
        brevno_image = pg.image.load("map/Tilesets/wood.png").convert_alpha()

        # Масштабування зображення
        scale_factor = 0.4
        new_width = int(brevno_image.get_width() * scale_factor)
        new_height = int(brevno_image.get_height() * scale_factor)
        brevno_image_scaled = pg.transform.scale(brevno_image, (new_width, new_height))

        # Збираємо всі точки 'brevno' з карти
        brevno_positions = []
        for layer in self.tmx_data.objectgroups:
            if layer.name == "wood":  # Шар для бревен
                for obj in layer:
                    if getattr(obj, "name", None) == "brevno":
                        brevno_positions.append((int(obj.x), int(obj.y)))

        # Розраховуємо кількість бревен для поточного рівня
        # Наприклад, з кожним рівнем зменшуємо кількість бревен на 5 (це значення можна налаштувати)
        reduction = 5
        total_logs = len(brevno_positions)
        logs_to_use = max(1, total_logs - self.current_level * reduction)  # Не менше 1-го

        # Випадковий вибір точок із отриманої кількості
        random_positions = random.sample(brevno_positions, logs_to_use)

        # Створюємо спрайти для вибраних точок
        for x, y in random_positions:
            sprite = GameSprite((x, y), brevno_image_scaled, self.brevno_group)
            sprite.is_brevno = True


    def load_tiles(self):
        """Завантаження тайлів із шарів карти у відповідному порядку."""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):  # Якщо це шар плиток
                if layer.name == "water":
                    self._load_layer_tiles(layer, self.water_group)
                elif layer.name == "base":
                    self._load_layer_tiles(layer, self.base_group)
                elif layer.name == 'decore':
                    self._load_layer_tiles(layer, self.decore_group)
                elif layer.name == 'flower':
                    self._load_layer_tiles(layer, self.flower_group)
                elif layer.name == 'apple':
                    self._load_layer_tiles(layer, self.apple_group)
                elif layer.name == "swamp":
                    self._load_layer_tiles(layer, self.swamp_group)


    def _load_layer_tiles(self, layer, group, ):
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
                                x * self.tmx_data.tilewidth,
                                y * self.tmx_data.tileheight - tile_image.get_height() + 20
                            )
                            GameSprite(pos, tile_image, self.tree_group)


    def load_fire(self):
        """Завантаження об'єктів вогню з міткою 'campf'."""
        for layer in self.tmx_data.objectgroups:
            for obj in layer:
                if getattr(obj, "name", None) == "campf":
                    x = int(obj.x)
                    y = int(obj.y)


                    Fire(pos=(x, y), assets_path=self.assets_path, group=self.fire_group)


    def is_player_near_fire(self, player):
        """костер, з яким гравець може взаємодіяти."""
        player_center = pg.math.Vector2(player.rect.center)
        nearest_fire = None
        min_distance = float('inf')

        for fire in self.fire_group:
            fire_center = pg.math.Vector2(fire.rect.center)
            distance = player_center.distance_to(fire_center)
            if distance <= fire.izona_radius and distance < min_distance:
                min_distance = distance
                nearest_fire = fire

        if nearest_fire:
            return nearest_fire
        else:
            return None


    def is_player_in_lighting_zone(self, player):
        for fire in self.fire_group:
            if fire.is_lighting_active:
                distance = pg.math.Vector2(player.rect.center).distance_to(fire.rect.center)
                # print(f"[Debug] Distance to fire at {fire.rect.center}: {distance}, lighting_radius: {fire.lighting_radius}")
                if distance <= fire.lighting_radius:
                    return True
        return False


    def handle_log_to_fire(self, player):
        """Обробляє логіку додавання бревна до костра."""
        nearest_fire = self.is_player_near_fire(player)
        if nearest_fire and player.carried_log:
            for i in self.fire_group:
                if i.progress > 0:
                    nearest_fire.add_progress()
                    player.carried_log.kill()
                    player.carried_log = None
                    player.count_wood -= 1


    def update(self, player, delta_time):
        """Оновлення рівня: камера, костри, прогрес-бар."""
        # Оновлення камери
        self.camera.update(player.rect)

        # Оновлення кострів та інших об'єктів
        self.check_brevno_pickup(player)
        self.updatef(delta_time)

        # Оновлення позиції піднятого бревна
        if player.carried_log:
            offset = (10, 0)  # Зміщення можна налаштувати
            player.carried_log.rect.centerx = player.rect.centerx + offset[0]
            player.carried_log.rect.centery = player.rect.centery + offset[1]

        # Оновлення прогрес-бару холоду
        if self.is_player_in_lighting_zone(player):
            player.decrease_cold(delta_time)

        else:
            player.increase_cold(delta_time)

        if pg.sprite.spritecollide(player, self.swamp_group, False, pg.sprite.collide_rect):
            player.speed = player.base_speed * 0.5  # Зменшуємо швидкість (наприклад, вдвічі)
        else:
            player.speed = player.base_speed


    def check_brevno_pickup(self, player):
        """Перевіряє зіткнення гравця з бревнами."""

        if player.carried_log is not None:
            self.collision_group.add(*self.brevno_group)
        else:
            self.collision_group.remove(*self.brevno_group)
        for brevno in list(self.brevno_group):
            if player.rect.colliderect(brevno.rect):
                if player.carried_log is None:
                    # Видаляємо бревно зі спрайт-групи
                    self.brevno_group.remove(brevno)
                    self.collision_group.remove(brevno)
                    player.carried_log = brevno
                    carried_offset = (30, -10)  # Налаштуйте зміщення за потребою
                    player.carried_log.rect.centerx = player.rect.centerx + carried_offset[0]
                    player.carried_log.rect.centery = player.rect.centery + carried_offset[1]
                    player.count_wood += 1
                else:
                    self.collision_group.add(*self.brevno_group)


    def handle_collisions(self, player):
        # Рух по осі X
        player.rect.centerx += player.velocity.x
        collided_sprites = pg.sprite.spritecollide(player, self.collision_group, False, pg.sprite.collide_rect)
        if collided_sprites:
            if player.velocity.x > 0:  # Рух вправо
                player.rect.right = min(sprite.rect.left for sprite in collided_sprites)
            elif player.velocity.x < 0:  # Рух вліво
                player.rect.left = max(sprite.rect.right for sprite in collided_sprites)

        # Рух по осі Y
        player.rect.centery += player.velocity.y
        collided_sprites = pg.sprite.spritecollide(player, self.collision_group, False, pg.sprite.collide_rect)
        if collided_sprites:
            if player.velocity.y > 0:  # Рух вниз
                player.rect.bottom = min(sprite.rect.top for sprite in collided_sprites)
            elif player.velocity.y < 0:  # Рух вгору
                player.rect.top = max(sprite.rect.bottom for sprite in collided_sprites)

        # Обмеження в межах карти
        player.rect.centerx = max(player.rect.width // 2,
                                  min(player.rect.centerx, self.map_width - player.rect.width // 2))
        player.rect.centery = max(player.rect.height // 2,
                                  min(player.rect.centery, self.map_height - player.rect.height // 2))


    def draw_fire_progress_bar(self):
        # Беремо перший активний костер
        for fire in self.fire_group:
            if fire.progress > 0:  # Якщо костер активний
                if fire.progress_bar.current_bar_image:
                    bar_image = fire.progress_bar.current_bar_image
                    bar_x = self.screen.get_width() // 2 - bar_image.get_width() // 2
                    bar_y = 10  # Відстань від верхнього краю
                    self.screen.blit(bar_image, (bar_x, bar_y))
                break


    def render(self, player):
        """Відображаємо об'єкти"""
        visible_area = self.camera.get_visible_area()

        # Вода
        for tile in self.water_group:
            if tile.rect.colliderect(visible_area):
                zoomed_pos = self.camera.apply(tile.visual_rect)
                zoomed_image = self.camera.scale_surface(tile.image)
                self.screen.blit(zoomed_image, zoomed_pos.topleft)

        # База
        for tile in self.base_group:
            if tile.rect.colliderect(visible_area):
                zoomed_pos = self.camera.apply(tile.visual_rect)
                zoomed_image = self.camera.scale_surface(tile.image)
                self.screen.blit(zoomed_image, zoomed_pos.topleft)

        # Інші об'єкти: дерева, декор, бревна, вогонь
        for group in [self.swamp_group,self.decore_group, self.flower_group, self.tree_group, self.brevno_group, self.fire_group,]:
            for obj in group:
                if obj.rect.colliderect(visible_area):
                    zoomed_pos = self.camera.apply(obj.visual_rect)
                    zoomed_image = self.camera.scale_surface(obj.image)
                    self.screen.blit(zoomed_image, zoomed_pos.topleft)

        for fire in self.fire_group:
            fire.draw(self.screen, self.camera)

        # Відображення піднятого бревна
        if player.carried_log and player.carried_log.rect.colliderect(visible_area):
            zoomed_pos = self.camera.apply(player.carried_log.rect)
            zoomed_image = self.camera.scale_surface(player.carried_log.image)
            self.screen.blit(zoomed_image, zoomed_pos.topleft)

        # Відображення прогрес-бару активного костра у верхній частині екрану
        self.draw_fire_progress_bar()


