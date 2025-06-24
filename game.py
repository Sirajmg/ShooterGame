import pygame
import random
import sys
import os
from player import Player
from enemy import Enemy
from boss import Boss
from bullet import Bullet
from weapon import Weapon
from powerup import PowerUp

WHITE = (255, 255, 255)
RED = (200, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
PURPLE = (180, 0, 255)

# إنشاء مجلدات إذا لم تكن موجودة
if not os.path.exists("assets"):
    os.makedirs("assets")
if not os.path.exists("data"):
    os.makedirs("data")

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
hit_sound = pygame.mixer.Sound("assets/hit.wav")
MAX_LEVEL = 5

explosion_dir = os.path.join("assets", "Images", "Expolsion")
class Explosion(pygame.sprite.Sprite):
    try:
        explosion_files = sorted(
            [f for f in os.listdir(explosion_dir) if f.endswith('.png')],
            key=lambda x: int(os.path.splitext(x)[0])
        )
        explosion_images = [pygame.image.load(os.path.join(explosion_dir, f)).convert_alpha() for f in explosion_files]
    except Exception as e:
        print("Error loading explosion images:", e)
        explosion_images = []
    def __init__(self, x, y):
        super().__init__()
        self.images = self.explosion_images
        self.index = 0
        self.image = self.images[self.index] if self.images else pygame.Surface((32,32), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.timer = 0
        self.frame_rate = 3  # كل كم فريم تتغير الصورة
    def update(self):
        self.timer += 1
        if self.timer % self.frame_rate == 0:
            self.index += 1
            if self.index < len(self.images):
                self.image = self.images[self.index]
            else:
                self.kill()
    def draw(self, surface):
        surface.blit(self.image, self.rect)

def run_game(screen, WIDTH, HEIGHT):
    clock = pygame.time.Clock()
    player = Player(WIDTH // 2, HEIGHT // 2)
    bullets = []
    enemies = []
    boss = None
    weapons = []
    powerups = []
    boss_bullets = []
    enemy_spawn_timer = 0
    enemy_spawn_delay = 40
    weapon_spawn_timer = 0
    weapon_spawn_delay = 500
    powerup_spawn_timer = 0
    powerup_spawn_delay = 600
    score = 0
    level = 1
    kills = 0
    enemies_per_level = 10
    boss_defeated = False
    paused = False
    running = True
    explosions = pygame.sprite.Group()

    # تحميل صورة الخلفية وتحجيمها
    bg_img = pygame.image.load(os.path.join("assets", "Images", "Playing", "0.jpg")).convert()
    bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))
    bg_y = 0

    while running:
        clock.tick(60)
        # تحريك الخلفية
        bg_y += 1
        if bg_y >= HEIGHT:
            bg_y = 0
        screen.blit(bg_img, (0, bg_y - HEIGHT))
        screen.blit(bg_img, (0, bg_y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_SPACE and not paused:
                    # إطلاق الرصاص بناءً على نوع السلاح الحالي
                    if player.weapon_type == "basic":
                        bullets.append(Bullet(player.rect.centerx, player.rect.top, player.rect.centerx, 0, bullet_type='basic'))
                    elif player.weapon_type == "double":
                        bullets.append(Bullet(player.rect.centerx - 15, player.rect.top, player.rect.centerx - 15, 0, bullet_type='double'))
                        bullets.append(Bullet(player.rect.centerx + 15, player.rect.top, player.rect.centerx + 15, 0, bullet_type='double'))
                    elif player.weapon_type == "laser":
                        bullets.append(Bullet(player.rect.centerx, player.rect.top, player.rect.centerx, 0, bullet_type='laser'))
                    elif player.weapon_type == "spread":
                        for offset in [-30, -15, 0, 15, 30]:
                            bullets.append(Bullet(player.rect.centerx + offset, player.rect.top, player.rect.centerx + offset, 0, bullet_type='spread'))
                    shoot_sound.play()
                if event.key == pygame.K_ESCAPE:
                    return  # العودة للقائمة الرئيسية

        if paused:
            draw_text(screen, "TO CONTINUE CLICK P", WIDTH // 2 - 150, HEIGHT // 2)
            pygame.display.flip()
            continue

        keys = pygame.key.get_pressed()
        player.update(keys, WIDTH, HEIGHT)

        # تحديث الأسلحة المتساقطة
        weapon_spawn_timer += 1
        if weapon_spawn_timer >= weapon_spawn_delay:
            weapons.append(Weapon())
            weapon_spawn_timer = 0

        for weapon in weapons[:]:
            weapon.update()
            if weapon.rect.colliderect(player.rect):
                player.weapon_type = weapon.weapon_type
                weapons.remove(weapon)
            elif weapon.rect.top > HEIGHT:
                weapons.remove(weapon)

        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0 or bullet.rect.top > HEIGHT:
                bullets.remove(bullet)

        if kills < enemies_per_level:
            enemy_spawn_timer += 1
            if enemy_spawn_timer >= enemy_spawn_delay:
                enemies.append(Enemy(WIDTH, level))
                enemy_spawn_timer = 0

        # جعل البوس يطلق الرصاص
        if boss and random.random() < 0.03:  # 3% فرصة كل إطار
            boss_bullets.append(Bullet(
                boss.rect.centerx, 
                boss.rect.bottom, 
                player.rect.centerx, 
                player.rect.centery,
                speed=7,
                is_enemy=True,
                bullet_type='enemy'  # نوع رصاصة العدو
            ))

        for enemy in enemies[:]:
            enemy.update(player)
            for bullet in bullets[:]:
                if enemy.rect.colliderect(bullet.rect):
                    if bullet in bullets:
                        bullets.remove(bullet)
                    if enemy in enemies:
                        enemies.remove(enemy)
                        explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery))
                        score += 1
                        kills += 1
                    break
            if enemy.rect.colliderect(player.rect):
                if player.take_damage(10):
                    pygame.mixer.music.stop()
                    game_over(screen, score)
                    return
                hit_sound.play()
                if enemy in enemies:
                    enemies.remove(enemy)
                    explosions.add(Explosion(enemy.rect.centerx, enemy.rect.centery))
                    score += 1
                    kills += 1
                break

        if kills >= enemies_per_level and not boss and not boss_defeated:
            boss = Boss(WIDTH, level)

        if boss:
            boss.update(player)
            if boss.rect.colliderect(player.rect):
                if player.take_damage(20):
                    game_over(screen, score)
                    return
                hit_sound.play()
                # لا تزيل البوس عند لمس اللاعب، فقط قلل صحة اللاعب
                # explosions.add(Explosion(boss.rect.centerx, boss.rect.centery))
                # boss = None
                # boss_defeated = True
                # level += 1
                # kills = 0
                # enemies_per_level += 10
                # boss_defeated = False
                # if level > MAX_LEVEL:
                #     win_game(screen, score)
                #     return

        for bullet in bullets[:]:
            if boss and boss.rect.colliderect(bullet.rect):
                if bullet in bullets:
                    bullets.remove(bullet)
                boss.health -= 10
                if boss.health <= 0:
                    boss = None
                    boss_defeated = True
                    level += 1
                    kills = 0
                    enemies_per_level += 10  # زيادة عدد الأعداء في المستوى التالي
                    boss_defeated = False  # إعادة تعيين الحالة للسماح بظهور البوس في المستوى التالي
                    if level > MAX_LEVEL:
                        win_game(screen, score)
                        return

        # تحديث رصاصات البوس
        for boss_bullet in boss_bullets[:]:
            boss_bullet.update()
            if boss_bullet.rect.top > HEIGHT:
                boss_bullets.remove(boss_bullet)
            elif boss_bullet.rect.colliderect(player.rect):
                if player.take_damage(15):
                    pygame.mixer.music.stop()
                    game_over(screen, score)
                    return
                hit_sound.play()
                if boss_bullet in boss_bullets:
                    boss_bullets.remove(boss_bullet)

        # تحديث الباور-أب
        powerup_spawn_timer += 1
        if powerup_spawn_timer >= powerup_spawn_delay:
            powerups.append(PowerUp(random.randint(0, WIDTH - 20), -20))
            powerup_spawn_timer = 0

        for powerup in powerups[:]:
            powerup.update()
            if powerup.rect.colliderect(player.rect):
                powerup.apply_effect(player)
                powerups.remove(powerup)
            elif powerup.rect.top > HEIGHT:
                powerups.remove(powerup)

        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for boss_bullet in boss_bullets:
            boss_bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        for weapon in weapons:
            weapon.draw(screen)
        if boss:
            boss.draw(screen)
            # رسم شريط صحة البوس
            draw_boss_health_bar(screen, 10, 100, boss.health, 100 + level * 50)

        # رسم الباور-أب
        for powerup in powerups:
            powerup.draw(screen)

        draw_text(screen, f"Score: {score}", 10, 10)
        draw_text(screen, f"Health: {player.health}", 10, 40)
        draw_text(screen, f"Level: {level}", WIDTH - 140, 10)
       # draw_text(screen, f"Weapon: {player.weapon_type.upper()}", WIDTH - 140, 40)
        draw_health_bar(screen, 10, 70, player.health)

        # رسم حالة الباور-أب النشط
        if player.speed_boost:
            draw_text(screen, "SPEED BOOST", WIDTH - 140, 70, (0, 255, 255))
        if player.shield:
            draw_text(screen, "SHIELD", WIDTH - 140, 100, (255, 215, 0))
        if player.rapid_fire:
            draw_text(screen, "RAPID FIRE", WIDTH - 140, 130, (255, 0, 255))

        explosions.update()
        for explosion in explosions:
            explosion.draw(screen)

        pygame.display.flip()

# ... (بقية الدوال كما هي)# ... (بقية الدوال كما هي)

def draw_text(surface, text, x, y, color=(255,255,255), size=30):
    font = pygame.font.SysFont("Arial", size)
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def draw_boss_health_bar(surface, x, y, health, max_health):
    bar_width = 500  # زيادة طول الشريط
    bar_height = 24
    fill = int(bar_width * health / max_health)
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, (255, 80, 80), fill_rect)  # لون أحمر فاتح
    pygame.draw.rect(surface, (255,255,255), outline_rect, 3)

def draw_health_bar(surface, x, y, health, max_health=100):
    bar_width = 200
    bar_height = 20
    fill = int(bar_width * health / max_health)
    outline_rect = pygame.Rect(x, y, bar_width, bar_height)
    fill_rect = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, (0,255,0), fill_rect)
    pygame.draw.rect(surface, (255,255,255), outline_rect, 2)

def game_over(screen, score):
    screen.fill((0,0,0))
    draw_text(screen, "GAME OVER", 200, 200, (255,0,0), 60)
    draw_text(screen, f"Score: {score}", 200, 300, (255,255,255), 40)
    pygame.display.flip()
    pygame.time.wait(2000)

def win_game(screen, score):
    screen.fill((0,0,0))
    draw_text(screen, "YOU WIN!", 200, 200, (0,255,0), 60)
    draw_text(screen, f"Score: {score}", 200, 300, (255,255,255), 40)
    pygame.display.flip()
    pygame.time.wait(2000)