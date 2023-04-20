import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 400, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Pipe settings
PIPE_GAP = 300
PIPE_INTERVAL = 2000
pipe_speed = 2

# Bird settings
bird_y = HEIGHT // 2
bird_speed = 0
gravity = 0.5

# Game settings
clock = pygame.time.Clock()
pygame.time.set_timer(pygame.USEREVENT, PIPE_INTERVAL)

def add_pipe():
    pipe_height = random.randint(100, HEIGHT - PIPE_GAP - 100)
    pipes.append({'upper': pygame.Rect(WIDTH, 0, 100, pipe_height),
                  'lower': pygame.Rect(WIDTH, pipe_height + PIPE_GAP, 100, HEIGHT - pipe_height - PIPE_GAP)})

def move_pipes():
    for pipe in pipes:
        pipe['upper'].x -= pipe_speed
        pipe['lower'].x -= pipe_speed

def remove_offscreen_pipes():
    global pipes
    pipes = [pipe for pipe in pipes if pipe['upper'].x + pipe['upper'].width > 0]

def collision():
    for pipe in pipes:
        if pipe['upper'].colliderect(bird_rect) or pipe['lower'].colliderect(bird_rect):
            return True
    if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT:
        return True
    return False

def reset_game():
    global bird_y, bird_speed, pipes
    bird_y = HEIGHT // 2
    bird_speed = 0
    pipes = []
    add_pipe()

pipes = []
add_pipe()

running = True
game_over = False
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.USEREVENT:
            add_pipe()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if game_over:
                game_over = False
                reset_game()
            else:
                bird_speed = -10

    if not game_over:
        bird_speed += gravity
        bird_y += bird_speed
        bird_rect = pygame.Rect(50, bird_y, 30, 30)
        pygame.draw.rect(screen, GREEN, bird_rect)

        move_pipes()
        remove_offscreen_pipes()

        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe['upper'])
            pygame.draw.rect(screen, GREEN, pipe['lower'])

        if collision():
            game_over = True

    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
