import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong - Single Player with Smooth AI')
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Paddle and ball properties
player_paddle = pygame.Rect(50, height // 2 - 50, 20, 100)  # Left paddle
ai_paddle = pygame.Rect(750, height // 2 - 50, 20, 100)     # Right paddle
ball = pygame.Rect(width // 2 - 10, height // 2 - 10, 20, 20)
ball_speed = 7
ball_dx = ball_speed  # Horizontal speed
ball_dy = random.randint(-ball_speed, ball_speed)  # Initial vertical speed
paddle_speed = 5  # Player paddle speed
ai_max_speed = 6  # Max speed for AI paddle

# Scores
player_score = 0
ai_score = 0

# Font for scores
font = pygame.font.SysFont(None, 36)

# Function to calculate ball's vertical speed based on paddle contact point
def calculate_dy(paddle, ball):
    paddle_center = paddle.centery  # Y-coordinate of paddle's center
    ball_center = ball.centery      # Y-coordinate of ball's center
    offset = (ball_center - paddle_center) / (paddle.height / 2)  # Normalized: -1 to 1
    max_dy = ball_speed  # Maximum vertical speed
    return offset * max_dy  # Scale offset to vertical speed

# Main game loop
game_over = False
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True

    # Player controls (W = up, S = down)
    keys = pygame.key.get_pressed()
    player_dy = 0
    if keys[pygame.K_w]:
        player_dy = -paddle_speed
    if keys[pygame.K_s]:
        player_dy = paddle_speed
    player_paddle.top += player_dy
    if player_paddle.top < 0:
        player_paddle.top = 0
    if player_paddle.bottom > height:
        player_paddle.bottom = height

    # Smooth AI paddle movement
    ai_target_y = ball.centery  # Where the AI wants to go
    ai_distance = ai_target_y - ai_paddle.centery  # Distance to target
    ai_dy = ai_distance * 0.15  # Move 15% of the distance each frame
    ai_dy = max(min(ai_dy, ai_max_speed), -ai_max_speed)  # Cap the speed
    ai_paddle.top += ai_dy
    if ai_paddle.top < 0:
        ai_paddle.top = 0
    if ai_paddle.bottom > height:
        ai_paddle.bottom = height

    # Move the ball
    ball.left += ball_dx
    ball.top += ball_dy

    # Ball collision with top and bottom walls
    if ball.top <= 0 or ball.bottom >= height:
        ball_dy = -ball_dy

    # Ball collision with paddles
    if ball.colliderect(player_paddle) and ball_dx < 0:  # Left paddle hit
        ball_dx = -ball_dx  # Reverse horizontal direction
        ball_dy = calculate_dy(player_paddle, ball)  # Adjust vertical speed
    elif ball.colliderect(ai_paddle) and ball_dx > 0:    # Right paddle hit
        ball_dx = -ball_dx  # Reverse horizontal direction
        ball_dy = calculate_dy(ai_paddle, ball)  # Adjust vertical speed

    # Ball out of bounds (scoring)
    if ball.left <= 0:  # AI scores
        ai_score += 1
        ball.center = (width // 2, height // 2)  # Reset ball
        ball_dx = ball_speed
        ball_dy = random.randint(-ball_speed, ball_speed)
    elif ball.right >= width:  # Player scores
        player_score += 1
        ball.center = (width // 2, height // 2)  # Reset ball
        ball_dx = -ball_speed
        ball_dy = random.randint(-ball_speed, ball_speed)

    # Draw everything
    window.fill(BLACK)
    pygame.draw.rect(window, WHITE, player_paddle)
    pygame.draw.rect(window, WHITE, ai_paddle)
    pygame.draw.rect(window, WHITE, ball)
    score_text = font.render(f"Player: {player_score}  AI: {ai_score}", True, WHITE)
    window.blit(score_text, (width // 2 - score_text.get_width() // 2, 10))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()
