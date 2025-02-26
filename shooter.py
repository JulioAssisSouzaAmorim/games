import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Shooter')
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.centerx = width // 2
        self.rect.bottom = height - 10
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > width:
            self.rect.right = width

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

# Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed

# Sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Score and lives
score = 0
invaders_crossed = 0
lives_left = 3  # Start with 3 lives
font = pygame.font.SysFont(None, 36)

# Enemy spawn timer
enemy_timer = 0
enemy_interval = 60

# Main game loop
game_over = False
while not game_over:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            if event.key == pygame.K_SPACE:
                player.shoot()

    # Update all sprites
    all_sprites.update()

    # Check for enemies crossing the line
    for enemy in enemies:
        if enemy.rect.bottom >= height:
            enemy.kill()
            invaders_crossed += 1

    # Update remaining lives
    lives_left = 3 - invaders_crossed

    # Lose condition
    if lives_left <= 0:
        game_over = True

    # Spawn enemies
    enemy_timer += 1
    if enemy_timer >= enemy_interval:
        enemy_timer = 0
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    # Check collisions: bullets and enemies
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        score += 1

    # Draw everything
    window.fill(BLACK)
    all_sprites.draw(window)
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))
    lives_text = font.render(f"Lives: {lives_left}", True, WHITE)
    window.blit(lives_text, (width - lives_text.get_width() - 10, 10))
    pygame.draw.line(window, WHITE, (0, height - 1), (width, height - 1), 2)

    # Update display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()