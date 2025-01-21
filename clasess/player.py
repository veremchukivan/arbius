import os
import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed, assets_path, scale_factor=2):
        super().__init__()
        self.rect = pygame.Rect(x, y, width * scale_factor, height * scale_factor)  # Масштабувати розмір гравця
        self.speed = speed
        self.velocity = pygame.math.Vector2(0, 0)

        # Анімація
        self.assets_path = os.path.join(assets_path, "player")
        self.scale_factor = scale_factor
        self.animations = self.load_animations()
        self.current_animation = "down"  # Стандартний напрямок
        self.frame_index = 0
        self.animation_speed = 0.1
        self.image = self.animations[self.current_animation][0]
        self.is_moving = False  # Флаг руху

    def load_animations(self):
        """Завантаження анімацій із папки з урахуванням масштабування."""
        animations = {}
        for direction in ["up", "right", "left", "down"]:
            path = os.path.join(self.assets_path, direction)
            frames = []
            for i in range(4):  # Кадри названі 0.png, 1.png, 2.png, 3.png
                frame_path = os.path.join(path, f"{i}.png")
                if os.path.exists(frame_path):
                    # Завантаження та масштабування кадру
                    frame = pygame.image.load(frame_path).convert_alpha()
                    scaled_frame = pygame.transform.scale(
                        frame,
                        (int(frame.get_width() * self.scale_factor), int(frame.get_height() * self.scale_factor))
                    )
                    frames.append(scaled_frame)
                else:
                    print(f"Файл {frame_path} не знайдено!")
            animations[direction] = frames
        return animations

    def update_animation(self):
        """Оновлення кадру анімації."""
        if self.is_moving:  # Оновлювати анімацію тільки якщо є рух
            frames = self.animations[self.current_animation]
            self.frame_index += self.animation_speed
            if self.frame_index >= len(frames):
                self.frame_index = 0
            self.image = frames[int(self.frame_index)]
        else:
            # Якщо немає руху, залишити перший кадр анімації
            self.image = self.animations[self.current_animation][0]

    def update(self, map_width, map_height):
        """Оновлення позиції та анімації гравця."""
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        self.velocity.y = 0
        self.is_moving = False  # За замовчуванням гравець не рухається

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
            self.current_animation = "left"
            self.is_moving = True
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
            self.current_animation = "right"
            self.is_moving = True
        elif keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity.y = -self.speed
            self.current_animation = "up"
            self.is_moving = True
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity.y = self.speed
            self.current_animation = "down"
            self.is_moving = True

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

        # Обмеження в межах карти
        self.rect.x = max(0, min(self.rect.x, map_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, map_height - self.rect.height))

        # Оновлення анімації
        self.update_animation()

    def draw(self, surface, camera):
        """Малювання гравця."""
        surface.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))
