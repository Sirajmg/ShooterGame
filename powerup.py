import pygame
import random

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.types = ['speed', 'shield', 'rapid_fire']
        self.type = random.choice(self.types)
        
        # Create a colored surface for the power-up
        self.image = pygame.Surface((20, 20))
        if self.type == 'speed':
            self.image.fill((0, 255, 255))  # Cyan for speed
        elif self.type == 'shield':
            self.image.fill((255, 215, 0))  # Gold for shield
        else:  # rapid_fire
            self.image.fill((255, 0, 255))  # Magenta for rapid fire
            
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 3
        
    def update(self):
        self.rect.y += self.speed
        
    def apply_effect(self, player):
        if self.type == 'speed':
            player.speed_boost = True
            player.speed_boost_timer = 300  # 5 seconds at 60 FPS
        elif self.type == 'shield':
            player.shield = True
            player.shield_timer = 300
        else:  # rapid_fire
            player.rapid_fire = True
            player.rapid_fire_timer = 300

    def draw(self, surface):
        surface.blit(self.image, self.rect) 