# classes/player.py
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((255, 0, 0))  # Червоний прямокутник як приклад
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self):
        keys = pygame.key.get_pressed()
        self.velocity.x = 0
        self.velocity.y = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.velocity.x = -self.speed
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.velocity.x = self.speed
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.velocity.y = -self.speed
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.velocity.y = self.speed

        self.rect.x += self.velocity.x
        self.rect.y += self.velocity.y

    def draw(self, surface, camera):
        surface.blit(self.image, (self.rect.x - camera.x, self.rect.y - camera.y))
