import pygame
import random
import time
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1282
SCREEN_HEIGHT = 750
FONT_SIZE = 13  # Adjust this value to make the font size smaller
NUM_COLUMNS = SCREEN_WIDTH // FONT_SIZE
BLUE_FADE_DURATION = 600
  # Seconds before blue opening occurs

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 123, 255)  # A lighter blue, hacking kind of blue
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Matrix")

# Load fonts
font = pygame.font.SysFont("monospace", FONT_SIZE, bold=True)
trailer_font = pygame.font.SysFont("comicsansms", 50, bold=True)  # Cartoonish font for the trailer text

# Matrix columns
columns = [2] * NUM_COLUMNS
symbols_in_column = [random.randint(5, 20) for _ in range(NUM_COLUMNS)]  # Random initial cluster sizes

# Time tracking
start_time = time.time()

# Generate random character
def get_random_char():
    return chr(random.randint(33, 126))  # ASCII characters from '!' to '~'

# Function to generate a jagged, rocky shape
def generate_rocky_rip(center, max_radius, num_points=50, jaggedness=0.2):
    points = []
    angle_step = 2 * math.pi / num_points
    for i in range(num_points):
        angle = i * angle_step
        # Create a random variation for the radius to make it jagged
        radius = max_radius + random.uniform(-jaggedness * max_radius, jaggedness * max_radius)
        x = center[0] + math.cos(angle) * radius
        y = center[1] + math.sin(angle) * radius
        points.append((x, y))
    return points

# Main loop
running = True
clock = pygame.time.Clock()
blue_expanding = False
blue_max_radius = 0
blue_opening_started = False
project_baymax_displayed = False

while running:
    elapsed_time = time.time() - start_time
    
    if elapsed_time < BLUE_FADE_DURATION:
        # Clear the screen with black background
        screen.fill(BLACK)
        
        # Increase symbols over time based on elapsed time
        max_symbols = int(min(50, elapsed_time // 15 + 10))  # Increase max number of symbols in clusters over time
        
        # Draw matrix effect
        for i in range(len(columns)):
            for j in range(symbols_in_column[i]):  # Draw multiple symbols per column
                char = font.render(get_random_char(), True, GREEN)
                pos_x = i * FONT_SIZE
                pos_y = (columns[i] + j) * FONT_SIZE
                
                if pos_y < SCREEN_HEIGHT:
                    screen.blit(char, (pos_x, pos_y))
            
            # Randomly reset column or move down
            if columns[i] * FONT_SIZE > SCREEN_HEIGHT or random.random() > 0.975:
                columns[i] = 0
                symbols_in_column[i] = random.randint(5, max_symbols)  # New cluster size based on time
            else:
                columns[i] += 1
    
    # After 15 seconds, start the blue opening effect
    if elapsed_time >= BLUE_FADE_DURATION and not blue_opening_started:
        blue_opening_started = True
        blue_expanding = True
        blue_start_time = time.time()
    
    if blue_expanding:
        blue_max_radius += 6  # Speed of the expanding rip
        
        # Generate and draw jagged rocky rip
        rocky_rip = generate_rocky_rip((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), blue_max_radius)
        pygame.draw.polygon(screen, BLUE, rocky_rip)

        
        # Stop expanding when the "rip" covers the entire screen
        if blue_max_radius > math.sqrt(SCREEN_WIDTH**2 + SCREEN_HEIGHT**2):
            blue_expanding = False
            screen.fill(BLACK)
            project_baymax_displayed = True
    
    # After the blue opening completes, display the text
    if project_baymax_displayed:
        screen.fill(BLACK)
        trailer_text = "I AM LOOKING THROUGH YOUR SYSTEMS NOW!!"
        rendered_text = trailer_font.render(trailer_text, True, WHITE)
        text_rect = rendered_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(rendered_text, text_rect)
    
    # Check for quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    pygame.display.flip()
    clock.tick(30)

# Quit Pygame
pygame.quit()
