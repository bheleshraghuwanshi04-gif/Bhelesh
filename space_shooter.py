import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Futuristic Space Shooter")

# Colors for futuristic neon theme
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 255, 255)
NEON_RED = (255, 0, 100)
NEON_GREEN = (0, 255, 100)

# Player settings
player_size = 50
player_rect = pygame.Rect(SCREEN_WIDTH // 2 - player_size // 2, SCREEN_HEIGHT - player_size - 10, player_size, player_size)
player_speed = 5

# Bullet settings
bullet_width = 5
bullet_height = 15
bullet_speed = 7
bullets = []  # List of bullet Rects

# Enemy settings
enemy_size = 20
enemy_speed = 3
enemies = []  # List of enemy Rects
num_enemies = 10
for _ in range(num_enemies):
    ex = random.randint(0, SCREEN_WIDTH - enemy_size)
    ey = random.randint(-SCREEN_HEIGHT, -enemy_size)
    enemies.append(pygame.Rect(ex, ey, enemy_size, enemy_size))

# Score
score = 0
font = pygame.font.SysFont(None, 36)

# Game over state
game_over = False

def show_game_over_screen():
    screen.fill(BLACK)
    game_over_font = pygame.font.SysFont(None, 72)
    game_over_text = game_over_font.render("GAME OVER", True, NEON_RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)

    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    pygame.display.flip()

    # Wait for player to close the window
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                waiting = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    waiting = False

# Game loop
clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                # Shoot bullet from the center of the player
                bullet_rect = pygame.Rect(player_rect.centerx - bullet_width // 2, player_rect.top, bullet_width, bullet_height)
                bullets.append(bullet_rect)

    if not game_over:
        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += player_speed

        # Update bullets
        new_bullets = []
        for bullet_rect in bullets:
            bullet_rect.y -= bullet_speed
            if bullet_rect.bottom > 0:
                new_bullets.append(bullet_rect)
        bullets = new_bullets

        # Update enemies
        for enemy_rect in enemies:
            enemy_rect.y += enemy_speed
            if enemy_rect.top > SCREEN_HEIGHT:
                # Respawn enemy if off-screen
                enemy_rect.x = random.randint(0, SCREEN_WIDTH - enemy_size)
                enemy_rect.y = random.randint(-100, -enemy_size)

        # --- COLLISION DETECTION ---
        # Check for bullet-enemy collisions
        for bullet_rect in bullets[:]:
            for enemy_rect in enemies[:]:
                if bullet_rect.colliderect(enemy_rect):
                    bullets.remove(bullet_rect)
                    enemies.remove(enemy_rect)
                    score += 1
                    # Respawn a new enemy to maintain the count
                    ex = random.randint(0, SCREEN_WIDTH - enemy_size)
                    ey = random.randint(-100, -enemy_size)
                    enemies.append(pygame.Rect(ex, ey, enemy_size, enemy_size))
                    break # Move to the next bullet

        # Check for player-enemy collisions
        for enemy_rect in enemies:
            if player_rect.colliderect(enemy_rect):
                game_over = True

        # --- DRAWING ---
        # Draw player spaceship (futuristic triangle)
        player_points = [
            (player_rect.centerx, player_rect.top),
            (player_rect.left, player_rect.bottom),
            (player_rect.right, player_rect.bottom)
        ]
        pygame.draw.polygon(screen, NEON_BLUE, player_points)

        # Draw bullets
        for bullet_rect in bullets:
            pygame.draw.rect(screen, NEON_GREEN, bullet_rect)

        # Draw enemies
        for enemy_rect in enemies:
            pygame.draw.circle(screen, NEON_RED, enemy_rect.center, enemy_size // 2)

        # Draw score
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # Show game over screen
        show_game_over_screen()
        running = False # End the main loop after showing the game over screen and waiting for quit

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit game
pygame.quit()
sys.exit()
