import pygame
import numpy as np
import json
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 40, 30
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
green = (0, 255, 0)

# Initialize game state
if os.path.exists('save_state.json'):
    with open('save_state.json', 'r') as file:
        game_state = np.array(json.load(file))
else:
    game_state = np.random.choice([0, 1], size=(n_cells_x, n_cells_y), p=[0.8, 0.2])

# Simulation control
running = True
paused = False
tick_interval = 0.5
last_tick_time = 0

def draw_button(text, position, size=(200, 50), color=green):
    button_x, button_y = position
    button_width, button_height = size
    pygame.draw.rect(screen, color, (button_x, button_y, button_width, button_height))
    font = pygame.font.Font(None, 36)
    text = font.render(text, True, black)
    text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text, text_rect)

def button_click_check(position, size, mouse_pos):
    button_x, button_y = position
    button_width, button_height = size
    if button_x <= mouse_pos[0] <= button_x + button_width and button_y <= mouse_pos[1] <= button_y + button_height:
        return True
    return False

def save_game_state():
    with open('save_state.json', 'w') as file:
        json.dump(game_state.tolist(), file)

def load_game_state():
    global game_state
    with open('save_state.json', 'r') as file:
        game_state = np.array(json.load(file))

def update_game():
    global last_tick_time, game_state
    current_time = pygame.time.get_ticks() / 1000
    if current_time - last_tick_time > tick_interval and not paused:
        last_tick_time = current_time
        next_generation()
        draw()

def draw():
    screen.fill(white)
    draw_grid()
    draw_cells()
    draw_button("Pause" if not paused else "Resume", (50, height - 60))
    draw_button("Save", (300, height - 60))
    draw_button("Load", (550, height - 60))
    pygame.display.flip()

def draw_grid():
    for y in range(0, height, cell_height):
        for x in range(0, width, cell_width):
            cell = pygame.Rect(x, y, cell_width, cell_height)
            pygame.draw.rect(screen, gray, cell, 1)

def next_generation():
    global game_state
    new_state = np.copy(game_state)

    for y in range(n_cells_y):
        for x in range(n_cells_x):
            n_neighbors = np.sum(game_state[(x - 1) % n_cells_x:(x + 2) % n_cells_x, (y - 1) % n_cells_y:(y + 2) % n_cells_y]) - game_state[x, y]

            if game_state[x, y] == 1 and (n_neighbors < 2 or n_neighbors > 3):
                new_state[x, y] = 0
            elif game_state[x, y] == 0 and n_neighbors == 3:
                new_state[x, y] = 1

    game_state = new_state

def draw_cells():
    for y in range(n_cells_y):
        for x in range(n_cells_x):
            cell = pygame.Rect(x * cell_width, y * cell_height, cell_width, cell_height)
            if game_state[x, y] == 1:
                pygame.draw.rect(screen, black, cell)

draw()  # Initial draw

while running:
    update_game()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_click_check((50, height - 60), (200, 50), event.pos):
                paused = not paused
            elif button_click_check((300, height - 60), (200, 50), event.pos):
                save_game_state()
            elif button_click_check((550, height - 60), (200, 50), event.pos):
                load_game_state()
                draw()
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                game_state[x, y] = not game_state[x, y]
                draw()

pygame.quit()
