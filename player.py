import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # استخدم صورة ثابتة للاعب
        self.image = pygame.image.load(os.path.join("assets", "Images", "Player", "Player_0.png")).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5
        self.health = 100
        self.max_health = 100
        self.weapon_type = "basic"
        self.weapon_timer = 0
        self.weapon_duration = 500
        # Power-up related attributes
        self.speed_boost = False
        self.speed_boost_timer = 0
        self.shield = False
        self.shield_timer = 0
        self.rapid_fire = False
        self.rapid_fire_timer = 0
        self.shoot_delay = 20  # Frames between shots
        self.shoot_timer = 0

    def update(self, keys, WIDTH, HEIGHT):
        # Update power-up timers
        if self.speed_boost:
            self.speed_boost_timer -= 1
            if self.speed_boost_timer <= 0:
                self.speed_boost = False
        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False
        if self.rapid_fire:
            self.rapid_fire_timer -= 1
            if self.rapid_fire_timer <= 0:
                self.rapid_fire = False
                self.shoot_delay = 20
        # Calculate movement speed
        current_speed = self.speed * 1.5 if self.speed_boost else self.speed
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= int(current_speed)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += int(current_speed)
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= int(current_speed)
        if keys[pygame.K_DOWN] and self.rect.bottom < HEIGHT:
            self.rect.y += int(current_speed)
        # تحديث السلاح
        if self.weapon_type != "basic":
            self.weapon_timer += 1
            if self.weapon_timer >= self.weapon_duration:
                self.weapon_type = "basic"
                self.weapon_timer = 0

    def draw(self, surface):
        # Draw shield effect if active
        if self.shield:
            shield_rect = self.rect.inflate(20, 20)
            pygame.draw.ellipse(surface, (0, 255, 255), shield_rect, 2)
        surface.blit(self.image, self.rect)
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = 50
        bar_height = 5
        health_ratio = self.health / self.max_health
        # رسم خلفية شريط الصحة
        pygame.draw.rect(surface, (255, 0, 0), (self.rect.x, self.rect.y - 10, bar_width, bar_height))
        # رسم شريط الصحة الحالي
        pygame.draw.rect(surface, (0, 255, 0), (self.rect.x, self.rect.y - 10, int(bar_width * health_ratio), bar_height))

    def take_damage(self, amount):
        if not self.shield:
            self.health -= amount
        return self.health <= 0