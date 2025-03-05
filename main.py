
import pygame
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Thank You Ariel!')

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)

# Define game variables
FPS = 60
clock = pygame.time.Clock()

# Player properties
player_width = 30
player_height = 50
player_x = 50
player_y = WINDOW_HEIGHT - player_height - 50
player_vel_x = 0
player_vel_y = 0
player_speed = 5
player_jump = -15
gravity = 0.8
is_jumping = False

# Platform properties
platforms = [
    # Base platforms
    {"x": 0, "y": WINDOW_HEIGHT - 50, "width": WINDOW_WIDTH, "height": 50},
    # Pyramid platforms
    {"x": 200, "y": WINDOW_HEIGHT - 120, "width": 150, "height": 20},
    {"x": 280, "y": WINDOW_HEIGHT - 190, "width": 150, "height": 20},
    {"x": 360, "y": WINDOW_HEIGHT - 260, "width": 150, "height": 20},
    {"x": 440, "y": WINDOW_HEIGHT - 330, "width": 150, "height": 20},
    {"x": 520, "y": WINDOW_HEIGHT - 400, "width": 120, "height": 20},
]

# Trophy properties
trophy = {"x": 560, "y": WINDOW_HEIGHT - 450, "width": 40, "height": 40, "collected": False}

# Celebration properties
celebration_active = False
celebration_time = 0
celebration_duration = 5000  # 5 seconds

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        
        # Key press events
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                player_vel_x = -player_speed
            if event.key == K_RIGHT:
                player_vel_x = player_speed
            if event.key == K_SPACE and not is_jumping:
                player_vel_y = player_jump
                is_jumping = True
        
        # Key release events
        if event.type == KEYUP:
            if event.key == K_LEFT and player_vel_x < 0:
                player_vel_x = 0
            if event.key == K_RIGHT and player_vel_x > 0:
                player_vel_x = 0
    
    # Update player position
    player_x += player_vel_x
    player_y += player_vel_y
    
    # Apply gravity
    player_vel_y += gravity
    
    # Check collision with platforms
    is_jumping = True
    for platform in platforms:
        # Check if player is on top of a platform
        if (player_y + player_height >= platform["y"] and 
            player_y + player_height <= platform["y"] + platform["height"] + 10 and
            player_x + player_width > platform["x"] and 
            player_x < platform["x"] + platform["width"] and
            player_vel_y > 0):
            player_y = platform["y"] - player_height
            player_vel_y = 0
            is_jumping = False
    
    # Check boundaries
    if player_x < 0:
        player_x = 0
    if player_x + player_width > WINDOW_WIDTH:
        player_x = WINDOW_WIDTH - player_width
    if player_y + player_height > WINDOW_HEIGHT:
        player_y = WINDOW_HEIGHT - player_height
        player_vel_y = 0
        is_jumping = False
    
    # Check trophy collection
    if (not trophy["collected"] and 
        player_x + player_width > trophy["x"] and
        player_x < trophy["x"] + trophy["width"] and
        player_y + player_height > trophy["y"] and
        player_y < trophy["y"] + trophy["height"]):
        trophy["collected"] = True
        celebration_active = True
        celebration_time = pygame.time.get_ticks()
    
    # Draw everything
    DISPLAYSURF.fill(BLACK)
    
    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(DISPLAYSURF, GREEN, 
                        (platform["x"], platform["y"], platform["width"], platform["height"]))
    
    # Draw player
    pygame.draw.rect(DISPLAYSURF, BLUE, (player_x, player_y, player_width, player_height))
    
    # Draw trophy if not collected
    if not trophy["collected"]:
        pygame.draw.polygon(DISPLAYSURF, YELLOW, [
            (trophy["x"] + trophy["width"] // 2, trophy["y"]),
            (trophy["x"], trophy["y"] + trophy["height"] // 2),
            (trophy["x"] + trophy["width"] // 2, trophy["y"] + trophy["height"]),
            (trophy["x"] + trophy["width"], trophy["y"] + trophy["height"] // 2),
        ])
    
    # Handle celebration
    if celebration_active:
        current_time = pygame.time.get_ticks()
        if current_time - celebration_time < celebration_duration:
            # Draw celebration elements
            for i in range(20):
                x = (i * 40) % WINDOW_WIDTH
                y = (i * 30) % WINDOW_HEIGHT
                size = 10 + (i % 10)
                color = [c % 256 for c in [i * 20, 100 + i * 10, 200 - i * 5]]
                pygame.draw.circle(DISPLAYSURF, color, (x, y), size)
            
            # Display thank you message
            font = pygame.font.Font(None, 36)
            lines = [
                "Ariel,",
                "thank you so much for being",
                "an incredible team member",
                "and working with me."
            ]
            
            for i, line in enumerate(lines):
                text = font.render(line, True, WHITE)
                text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, 150 + i * 40))
                DISPLAYSURF.blit(text, text_rect)
    
    # Update display
    pygame.display.update()
    clock.tick(FPS)
