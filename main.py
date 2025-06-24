import pygame
import sys
from game import run_game
import os

def draw_button(screen, rect, text, font, color, hover_color, mouse_pos, mouse_click, image=None):
    if rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, hover_color, rect, border_radius=8)
        if mouse_click[0]:
            return True
    else:
        pygame.draw.rect(screen, color, rect, border_radius=8)
    if image:
        img = pygame.image.load(image).convert_alpha()
        img = pygame.transform.scale(img, (rect.width, rect.height))
        screen.blit(img, rect)
    text_surf = font.render(text, True, (255,255,255))
    screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width())//2, rect.y + (rect.height - text_surf.get_height())//2))
    return False

def show_instructions(screen, WIDTH, HEIGHT):
    font = pygame.font.SysFont("Arial", 32)
    running = True
    while running:
        screen.fill((20, 20, 40))
        lines = [
            "Instructions:",
            "- Move: Arrow keys or WASD",
            "- Shoot: Spacebar",
            "- Pause: P",
            "- Collect weapons to upgrade",
            "- Destroy enemies and avoid collisions",
            "- Press ESC to return"
        ]
        for i, line in enumerate(lines):
            text = font.render(line, True, (255,255,255))
            screen.blit(text, (WIDTH//2 - text.get_width()//2, 100 + i*50))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        pygame.display.flip()

def show_game_over(screen, WIDTH, HEIGHT, score, win=False):
    font = pygame.font.SysFont("Arial", 48)
    small_font = pygame.font.SysFont("Arial", 32)
    running = True
    while running:
        screen.fill((30, 0, 0) if not win else (0, 30, 0))
        msg = "لقد فزت!" if win else " game over"
        text = font.render(msg, True, (255,255,0) if win else (255,0,0))
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 120))
        score_text = small_font.render(f"Score {score}", True, (255,255,255))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 200))
        info = small_font.render("Press ENTER to return to the main menu", True, (200,200,200))
        screen.blit(info, (WIDTH//2 - info.get_width()//2, 350))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                running = False
        pygame.display.flip()

def main_menu():
    pygame.init()
    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Survivor Shooter")
    font = pygame.font.SysFont("Arial", 40)
    small_font = pygame.font.SysFont("Arial", 28)
    clock = pygame.time.Clock()
    # صور الأزرار إذا توفرت
    play_img = os.path.join("assets", "Images", "Menu", "PlayBTN.png")
    play_img_hl = os.path.join("assets", "Images", "Menu", "PlayBTN_HL.png")
    game_name_img = os.path.join("assets", "Images", "Menu", "GameName.png")
    running = True
    while running:
        screen.fill((10, 10, 30))
        # اسم اللعبة
        if os.path.exists(game_name_img):
            img = pygame.image.load(game_name_img).convert_alpha()
            img = pygame.transform.scale(img, (400, 120))
            screen.blit(img, (WIDTH//2 - 200, 40))
        else:
            title = font.render("Survivor Shooter", True, (255,255,0))
            screen.blit(title, (WIDTH//2 - title.get_width()//2, 60))
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        # أزرار
        play_rect = pygame.Rect(WIDTH//2 - 100, 200, 200, 60)
        inst_rect = pygame.Rect(WIDTH//2 - 100, 280, 200, 60)
        quit_rect = pygame.Rect(WIDTH//2 - 100, 360, 200, 60)
        # زر ابدأ
        play_pressed = draw_button(screen, play_rect, "", font, (0,80,200), (0,120,255), mouse_pos, mouse_click, play_img if os.path.exists(play_img) else None)
        inst_pressed = draw_button(screen, inst_rect, "Instructions", font, (80,80,80), (120,120,120), mouse_pos, mouse_click)
        quit_pressed = draw_button(screen, quit_rect, "Quit", font, (120,0,0), (200,0,0), mouse_pos, mouse_click)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if play_pressed:
            run_game(screen, WIDTH, HEIGHT)
        if inst_pressed:
            show_instructions(screen, WIDTH, HEIGHT)
        if quit_pressed:
            pygame.quit()
            sys.exit()
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()