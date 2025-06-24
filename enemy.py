import pygame
import math
import os
import random

class Enemy(pygame.sprite.Sprite):
    alien_images = [
        os.path.join("assets", "Images", "Enemy", "Aliens", f"Alien_{i}.png") for i in range(4)
    ]
    def __init__(self, screen_width, level):
        super().__init__()
        # استخدم صورة عشوائية للعدو
        img_path = random.choice(self.alien_images)
        self.image = pygame.image.load(img_path).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = pygame.time.get_ticks() % (screen_width - 40)
        self.rect.y = -40
        self.speed = 2 + level
        self.health = 1
        self.max_health = 1

    def update(self, player):
        # حساب اتجاه الحركة نحو اللاعب
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        distance = max(1, math.sqrt(dx**2 + dy**2))
        # تطبيق الحركة
        self.rect.x += int((dx / distance) * self.speed)
        self.rect.y += int((dy / distance) * self.speed)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = 40
        bar_height = 4
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 6, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 6, int(bar_width * health_ratio), bar_height))

    def hit(self, damage=1):
        self.health = max(0, self.health - damage)
        return self.health <= 0