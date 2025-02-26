import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the display
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption('Tetris-like Game')
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # Cyan for I
    (255, 255, 0),  # Yellow for O
    (128, 0, 128),  # Purple for T
    (0, 255, 0),    # Green for S
    (255, 0, 0),    # Red for Z
    (0, 0, 255),    # Blue for J
    (255, 127, 0)   # Orange for L
]

# Grid properties
grid_width = 10
grid_height = 20
cell_size = 30
grid_x = (width - grid_width * cell_size) // 2
grid_y = (height - grid_height * cell_size) // 2

# Tetrimino shapes (list of [shape, color] pairs)
tetriminos = [
    [[(0,0), (0,1), (0,2), (0,3)], COLORS[0]],  # I
    [[(0,0), (0,1), (1,0), (1,1)], COLORS[1]],  # O
    [[(0,0), (0,1), (0,2), (1,1)], COLORS[2]],  # T
    [[(0,0), (0,1), (1,1), (1,2)], COLORS[3]],  # S
    [[(0,1), (0,2), (1,0), (1,1)], COLORS[4]],  # Z
    [[(0,0), (0,1), (0,2), (1,0)], COLORS[5]],  # J
    [[(0,0), (0,1), (0,2), (1,2)], COLORS[6]]   # L
]

# Initialize game state
grid = [[BLACK for _ in range(grid_width)] for _ in range(grid_height)]
current_tetrimino = random.choice(tetriminos)
current_position = [grid_width // 2 - 1, 0]
score = 0
font = pygame.font.SysFont(None, 36)
fall_counter = 0
base_fall_speed = 30  # Frames per fall at normal speed
game_over = False

# Functions

def rotate_shape(shape):
    """Rotate the Tetrimino shape 90 degrees clockwise."""
    return [(-dy, dx) for dx, dy in shape]

def check_collision(position, shape):
    """Check if the Tetrimino at the given position collides with boundaries or blocks."""
    for dx, dy in shape:
        grid_x = position[0] + dx
        grid_y = position[1] + dy
        if grid_x < 0 or grid_x >= grid_width or grid_y >= grid_height:
            return True
        if grid_y >= 0 and grid[grid_y][grid_x] != BLACK:
            return True
    return False

def add_to_grid(position, tetrimino):
    """Add the Tetrimino to the grid when it lands."""
    shape, color = tetrimino
    for dx, dy in shape:
        grid_x = position[0] + dx
        grid_y = position[1] + dy
        if grid_y >= 0:  # Only add blocks within the grid
            grid[grid_y][grid_x] = color

def check_lines():
    """Check for and clear completed lines, updating the score."""
    global score
    lines_to_clear = [y for y in range(grid_height) if all(grid[y][x] != BLACK for x in range(grid_width))]
    for y in lines_to_clear:
        del grid[y]
        grid.insert(0, [BLACK for _ in range(grid_width)])
    score += len(lines_to_clear) * 100

def spawn_new_tetrimino():
    """Spawn a new Tetrimino at the top center of the grid."""
    global current_tetrimino, current_position, game_over
    current_tetrimino = random.choice(tetriminos)
    current_position = [grid_width // 2 - 1, 0]
    if check_collision(current_position, current_tetrimino[0]):
        game_over = True

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_over = True
            if event.key == pygame.K_LEFT:
                new_position = [current_position[0] - 1, current_position[1]]
                if not check_collision(new_position, current_tetrimino[0]):
                    current_position = new_position
            if event.key == pygame.K_RIGHT:
                new_position = [current_position[0] + 1, current_position[1]]
                if not check_collision(new_position, current_tetrimino[0]):
                    current_position = new_position
            if event.key == pygame.K_UP:
                new_shape = rotate_shape(current_tetrimino[0])
                if not check_collision(current_position, new_shape):
                    current_tetrimino[0] = new_shape

    # Adjust fall speed based on player input
    keys = pygame.key.get_pressed()
    fall_speed = 5 if keys[pygame.K_DOWN] else base_fall_speed

    # Handle falling mechanism
    fall_counter += 1
    if fall_counter >= fall_speed:
        fall_counter = 0
        new_position = [current_position[0], current_position[1] + 1]
        if not check_collision(new_position, current_tetrimino[0]):
            current_position = new_position
        else:
            add_to_grid(current_position, current_tetrimino)
            check_lines()
            spawn_new_tetrimino()

    # Draw everything
    window.fill(BLACK)
    # Draw grid border
    pygame.draw.rect(window, WHITE, (grid_x - 1, grid_y - 1, grid_width * cell_size + 2, grid_height * cell_size + 2), 1)
    # Draw grid cells (landed blocks)
    for y in range(grid_height):
        for x in range(grid_width):
            if grid[y][x] != BLACK:
                pygame.draw.rect(window, grid[y][x], (grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size))
    # Draw current falling Tetrimino
    for dx, dy in current_tetrimino[0]:
        x = current_position[0] + dx
        y = current_position[1] + dy
        if y >= 0:  # Only draw blocks within the grid
            pygame.draw.rect(window, current_tetrimino[1], (grid_x + x * cell_size, grid_y + y * cell_size, cell_size, cell_size))
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    window.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

# Quit Pygame
pygame.quit()