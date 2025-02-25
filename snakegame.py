import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game with More Obstacles')
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Snake and game properties
block_size = 20

class Snake:
    def __init__(self):
        self.position = [width / 2, height / 2]
        self.body = [[width / 2, height / 2]]
        self.direction = "RIGHT"
        self.change = self.direction

    def change_direction(self, new_direction):
        if new_direction == 'LEFT' and self.direction != 'RIGHT':
            self.direction = new_direction
        if new_direction == 'RIGHT' and self.direction != 'LEFT':
            self.direction = new_direction
        if new_direction == 'UP' and self.direction != 'DOWN':
            self.direction = new_direction
        if new_direction == 'DOWN' and self.direction != 'UP':
            self.direction = new_direction

    def move(self, food_pos):
        if self.direction == "RIGHT":
            self.position[0] += block_size
        if self.direction == "LEFT":
            self.position[0] -= block_size
        if self.direction == "UP":
            self.position[1] -= block_size
        if self.direction == "DOWN":
            self.position[1] += block_size
        
        self.body.insert(0, list(self.position))
        if self.position == food_pos:
            return True
        self.body.pop()
        return False

    def check_collision(self, obstacles):
        if self.position[0] >= width or self.position[0] < 0:
            return True
        if self.position[1] >= height or self.position[1] < 0:
            return True
        if self.position in obstacles:
            return True
        for segment in self.body[1:]:
            if self.position == segment:
                return True
        return False

def spawn_food(obstacles, snake_body):
    """Generate a random food position not overlapping with obstacles or snake body."""
    while True:
        x = random.randrange(0, width // block_size) * block_size
        y = random.randrange(0, height // block_size) * block_size
        pos = [x, y]
        if pos not in obstacles and pos not in snake_body:
            food_type = 'special' if random.random() < 0.1 else 'regular'
            return pos, food_type

def draw_objects(snake, food_pos, food_type, score, obstacles):
    """Draw the snake, food, obstacles, and score on the screen."""
    window.fill(BLACK)
    for pos in snake.body:
        pygame.draw.rect(window, GREEN, [pos[0], pos[1], block_size, block_size])
    color = RED if food_type == 'regular' else BLUE
    pygame.draw.rect(window, color, [food_pos[0], food_pos[1], block_size, block_size])
    for obs in obstacles:
        pygame.draw.rect(window, WHITE, [obs[0], obs[1], block_size, block_size])
    
    font = pygame.font.SysFont(None, 50)
    score_text = font.render(f'Score: {score}', True, WHITE)
    window.blit(score_text, [0, 0])

def main():
    snake = Snake()
    
    # Generate random obstacles (increased to 10 for more challenge)
    all_positions = [[x * block_size, y * block_size] 
                     for x in range(width // block_size) 
                     for y in range(height // block_size)]
    available_positions = [pos for pos in all_positions if pos != snake.position]
    num_obstacles = 10  # Adjustable; increase for more obstacles
    obstacles = random.sample(available_positions, min(num_obstacles, len(available_positions)))
    
    food_pos, food_type = spawn_food(obstacles, snake.body)
    score = 0
    foods_eaten = 0
    speed = 15
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction('LEFT')
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction('RIGHT')
                elif event.key == pygame.K_UP:
                    snake.change_direction('UP')
                elif event.key == pygame.K_DOWN:
                    snake.change_direction('DOWN')
        
        # Move snake and check if it eats the food
        if snake.move(food_pos):
            foods_eaten += 1
            if food_type == 'regular':
                score += 1
            else:
                score += 5
            food_pos, food_type = spawn_food(obstacles, snake.body)
            if foods_eaten % 5 == 0:
                speed += 1
        
        # Check for collisions with walls, obstacles, or itself
        game_over = snake.check_collision(obstacles)
        
        # Update the display
        draw_objects(snake, food_pos, food_type, score, obstacles)
        pygame.display.flip()
        clock.tick(speed)

    # Display game over message
    font = pygame.font.SysFont(None, 50)
    game_over_text = font.render(f'Game Over! Final Score: {score}', True, WHITE)
    window.blit(game_over_text, [width//4, height//2])
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    print(f"Game Over! Final Score: {score}")

# Start the game
main()