import pygame
import math
import os
import random

class Weapon(pygame.sprite.Sprite):
    def __init__(self, screen_width=800, screen_height=600, weapon_type=None):
        super().__init__()
        self.types = ["basic", "double", "laser", "spread"]
        if weapon_type is None:
            self.weapon_type = random.choice(self.types)
        else:
            self.weapon_type = weapon_type
        self.last_shot = 0
        self.setup_weapon()

        # تحميل صورة السلاح حسب النوع
        gun_images = [
            os.path.join("assets", "Images", "Guns", "laser.png")
        ]
        img_path = random.choice(gun_images)
        self.image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (32, 32))
        # تدوير صورة السلاح لتكون عمودية
        self.image = pygame.transform.rotate(self.image, 0)  # إذا كانت الصور أفقية، استخدم 90 أو -90 بدلاً من 0
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(20, screen_width - 50)
        self.rect.y = random.randint(-100, -30)
        self.speed = 3

    def setup_weapon(self):
        if self.weapon_type == "basic":
            self.fire_rate = 500
            self.damage = 1
            self.bullet_speed = 10
            self.bullet_size = (6, 12)
            self.bullet_color = (255, 255, 0)
            self.spread = 0
            self.bullets_per_shot = 1
        elif self.weapon_type == "double":
            self.fire_rate = 400
            self.damage = 1
            self.bullet_speed = 12
            self.bullet_size = (8, 15)
            self.bullet_color = (0, 120, 255)
            self.spread = 5
            self.bullets_per_shot = 2
        elif self.weapon_type == "laser":
            self.fire_rate = 300
            self.damage = 2
            self.bullet_speed = 15
            self.bullet_size = (4, 25)
            self.bullet_color = (255, 0, 255)
            self.spread = 0
            self.bullets_per_shot = 1
        elif self.weapon_type == "spread":
            self.fire_rate = 600
            self.damage = 1
            self.bullet_speed = 8
            self.bullet_size = (6, 10)
            self.bullet_color = (0, 255, 0)
            self.spread = 15
            self.bullets_per_shot = 5

    def can_shoot(self):
        current_time = pygame.time.get_ticks()
        return current_time - self.last_shot >= self.fire_rate

    def shoot(self, x, y, target_x, target_y, is_enemy=False):
        if not self.can_shoot():
            return []
        self.last_shot = pygame.time.get_ticks()
        bullets = []
        dx = target_x - x
        dy = target_y - y
        base_angle = math.degrees(math.atan2(-dy, dx))
        for i in range(self.bullets_per_shot):
            spread_angle = base_angle + (self.spread * (i - (self.bullets_per_shot - 1) / 2))
            rad_angle = math.radians(spread_angle)
            bullet_dx = math.cos(rad_angle) * self.bullet_speed
            bullet_dy = -math.sin(rad_angle) * self.bullet_speed
            bullet = {
                'x': x,
                'y': y,
                'dx': bullet_dx,
                'dy': bullet_dy,
                'damage': self.damage,
                'is_enemy': is_enemy,
                'size': self.bullet_size,
                'color': self.bullet_color
            }
            bullets.append(bullet)
        return bullets

    def upgrade(self):
        idx = self.types.index(self.weapon_type)
        if idx < len(self.types) - 1:
            self.weapon_type = self.types[idx + 1]
            self.setup_weapon()

    def update(self):
        self.rect.y += self.speed

    def draw(self, surface):
        surface.blit(self.image, self.rect)