import pygame
import sys
import random

# Constants
GRID_SIZE = 25
GRID_WIDTH = 10
GRID_HEIGHT = 20
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Tetromino shapes
SHAPES = [
    [['.....',
      '.....',
      '.OOO.',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '..O..',
      '.....'],
     ['.....',
      '..O..',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '.O...',
      '.OO..',
      '.O...',
      '.....']],
    [['.....',
      '.....',
      '.OOO.',
      '.O...',
      '.....'],
     ['.....',
      '.OO..',
      '..O..',
      '..O..',
      '.....'],
     ['.....',
      '...O.',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '.O...',
      '.O...',
      '.OO..',
      '.....']],
    [['.....',
      '.....',
      '.OOO.',
      '...O.',
      '.....'],
     ['.....',
      '..O..',
      '..O..',
      '.OO..',
      '.....'],
     ['.....',
      '.O...',
      '.OOO.',
      '.....',
      '.....'],
     ['.....',
      '.OO..',
      '.O...',
      '.O...',
      '.....']],
    [['.....',
      '.....',
      '.OO..',
      '.OO..',
      '.....']],
    [['.....',
      '.....',
      '..OO.',
      '.OO..',
      '.....'],
     ['.....',
      '.O...',
      '.OO..',
      '..O..',
      '.....']],
    [['.....',
      '.....',
      '.OO..',
      '..OO.',
      '.....'],
     ['.....',
      '..O..',
      '.OO..',
      '.O...',
      '.....']],
    [['.....',
      '.....',
      '..O..',
      '.OOO.',
      '.....'],
     ['.....',
      '..O..',
      '..OO.',
      '..O..',
      '.....'],
     ['.....',
      '.OOO.',
      '..O..',
      '.....',
      '.....'],
     ['.....',
      '.O...',
      '.OO..',
      '.O...',
      '.....']]
]
COLORS = [(0, 255, 255), (255, 165, 0), (0, 0, 255), (255, 255, 0), (0, 128, 0), (128, 0, 128), (255, 0, 0)]

# Initialize pygame
pygame.init()

# Create the screen
screen = pygame.display.set_mode((GRID_SIZE * GRID_WIDTH, GRID_SIZE * GRID_HEIGHT))
pygame.display.set_caption("Tetris (TBU)")


def create_tetromino(shape=None, x=None, y=None, color=None):
    if shape is None:
        shape = random.choice(SHAPES)
    if x is None:
        x = GRID_WIDTH // 2 - len(shape[0]) // 2
    if y is None:
        y = 0
    if color is None:
        color = random.choice(COLORS)

    return {'shape': [list(map(lambda cell: color if cell == 'O' else None, row)) for row in shape], 'x': x, 'y': y}


def new_tetromino():
    return create_tetromino()


def draw_tetromino(tetromino):
    for y, row in enumerate(tetromino['shape']):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, cell, (GRID_SIZE * (tetromino['x'] + x) + 1, GRID_SIZE * (tetromino['y'] + y) + 1, GRID_SIZE - 2, GRID_SIZE - 2))


def draw_grid():
    for x in range(GRID_WIDTH):
        for y in range(GRID_HEIGHT):
            pygame.draw.rect(screen, BLACK, (GRID_SIZE * x + 1, GRID_SIZE * y + 1, GRID_SIZE - 2, GRID_SIZE - 2), 1)


def check_collision(tetromino, dx=0, dy=0):
    for y, row in enumerate(tetromino['shape']):
        for x, cell in enumerate(row):
            if cell:
                new_x = tetromino['x'] + x + dx
                new_y = tetromino['y'] + y + dy
                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or grid[new_y][new_x]:
                    return True
    return False


def merge_tetromino(tetromino):
    for y, row in enumerate(tetromino['shape']):
        for x, cell in enumerate(row):
            if cell:
                grid[tetromino['y'] + y][tetromino['x'] + x] = cell


def clear_lines():
    full_lines = []
    for y, row in enumerate(grid):
        if all(cell for cell in row):
            full_lines.append(y)
    for y in full_lines:
        del grid[y]
        grid.insert(0, [None for _ in range(GRID_WIDTH)])
    return len(full_lines)


def rotate_tetromino(tetromino):
    rotated = list(zip(*reversed(tetromino['shape'])))
    new_tetromino = create_tetromino(rotated, tetromino['x'], tetromino['y'], tetromino['shape'][0][0])
    if not check_collision(new_tetromino):
        return new_tetromino
    return tetromino


grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

tetromino = new_tetromino()
score = 0
clock = pygame.time.Clock()
fall_time = 0
fall_speed = 300
running = True

while running:
    screen.fill(WHITE)
    dt = clock.tick(60)
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and not check_collision(tetromino, dx=-1):
                tetromino['x'] -= 1
            if event.key == pygame.K_RIGHT and not check_collision(tetromino, dx=1):
                tetromino['x'] += 1
            if event.key == pygame.K_DOWN and not check_collision(tetromino, dy=1):
                tetromino['y'] += 1
            if event.key == pygame.K_UP:
                tetromino = rotate_tetromino(tetromino)
            if event.key == pygame.K_SPACE:
                while not check_collision(tetromino, dy=1):
                    tetromino['y'] += 1

    if fall_time >= fall_speed:
        if not check_collision(tetromino, dy=1):
            tetromino['y'] += 1
            fall_time = 0
        else:
            merge_tetromino(tetromino)
            score += clear_lines()
            tetromino = new_tetromino()
            if check_collision(tetromino):
                running = False
            fall_time = 0  # Add this line

    draw_tetromino(tetromino)
    draw_grid()

    pygame.display.update()

pygame.quit()
sys.exit()
