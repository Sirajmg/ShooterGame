import pygame
import math
import os

BULLET_IMAGES = {
    'basic': os.path.join('assets', 'Images','Enemy', 'Bullets', 'Laser.png'),
    'double': os.path.join('assets', 'Images','Enemy' 'Bullets', 'Laser_beam.png'),
    'laser': os.path.join('assets', 'Images', 'Guns', 'Laser.png'),
    'spread': os.path.join('assets', 'Images', 'Enemy', 'Bullets', 'Laser_beam.png'),
    'enemy': os.path.join('assets', 'Images', 'Guns', 'Laser.png')
}
BULLET_COLORS = {
    'basic': (255, 255, 0),
    'double': (0, 120, 255),
    'laser': (255, 0, 255),
    'spread': (0, 255, 0),
    'enemy': (255, 60, 60)
}

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y, speed=10, damage=1, is_enemy=False, bullet_type='basic'):
        super().__init__()
        img_path = BULLET_IMAGES.get(bullet_type)
        if img_path and os.path.exists(img_path):
            self.image = pygame.image.load(img_path).convert_alpha()
        else:
            color = BULLET_COLORS.get(bullet_type, (255, 255, 255))
            self.image = pygame.Surface((12, 24), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, color, [0, 0, 12, 24])
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.damage = damage
        self.is_enemy = is_enemy

        # حساب اتجاه الحركة
        dx = target_x - x
        dy = target_y - y
        distance = max(1, math.sqrt(dx**2 + dy**2))
        self.dx = (dx / distance) * speed
        self.dy = (dy / distance) * speed

        # حساب زاوية الدوران
        self.angle = math.degrees(math.atan2(-dy, dx))
        self.image = pygame.transform.rotate(self.image, 180)  # أو -90 حسب اتجاه الصورة

    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

    def draw(self, surface):
        surface.blit(self.image, self.rect)