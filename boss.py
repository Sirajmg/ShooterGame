import pygame
import math
import os
import random

class Boss(pygame.sprite.Sprite):
    boss_images = [
        os.path.join("assets", "Images", "Enemy", "Bosses", f"Boss_0.png")
    ]
    def __init__(self, screen_width, level):
        super().__init__()
        # استخدم صورة الزعيم (يمكن التوسعة لاحقاً)
        img_path = random.choice(self.boss_images)
        image = pygame.image.load(img_path).convert_alpha()
        # صغر حجم الزعيم
        self.image = pygame.transform.scale(image, (150, 150))
        self.rect = self.image.get_rect()
        self.rect.x = screen_width // 2 - self.rect.width // 2
        self.rect.y = -self.rect.height
        self.speed = 1 + (level * 0.5)
        self.health = 10 * level
        self.max_health = self.health
        self.attack_timer = 0
        self.attack_delay = 2000  # تأخير بين الهجمات (بالميلي ثانية)

    def update(self, player):
        # حركة الزعيم
        if self.rect.y < 50:  # الوصول إلى موضع البداية
            self.rect.y += int(self.speed)
        else:
            # حركة متذبذبة
            self.rect.x += int(math.sin(pygame.time.get_ticks() * 0.001) * 2)
        # تحديث مؤقت الهجوم
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_timer > self.attack_delay:
            self.attack_timer = current_time
            return True  # إشارة للهجوم
        return False

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = 100
        bar_height = 8
        health_ratio = self.health / self.max_health
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 10, int(bar_width * health_ratio), bar_height))

    def hit(self, damage=1):
        self.health = max(0, self.health - damage)
        return self.health <= 0