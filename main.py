
import pygame
import sys
import random
import os
import math
from pygame.locals import *
from attached_assets.cat_image import load_cat_image
from attached_assets.olive_cat import load_olive_cat_image

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
BLUE = (100, 149, 237)  # More cat-themed blue
GREEN = (129, 199, 132)  # Softer green
RED = (255, 0, 0)
YELLOW = (255, 215, 0)  # Golden
PURPLE = (255, 0, 255)
GRAY = (50, 50, 50)

# Define game variables
FPS = 60
clock = pygame.time.Clock()

# Load cat background and Olive cat sprite
cat_image = load_cat_image()
olive_cat_image = load_olive_cat_image()
parallax_offset = 0

# Digital rain properties
class RainDrop:
    def __init__(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(-100, 0)
        self.speed = random.uniform(2, 8)
        self.color = random.choice([
            (135, 206, 250),  # Light blue
            (144, 238, 144),  # Light green
            (255, 182, 193),  # Light pink
            (255, 255, 224),  # Light yellow
            (230, 230, 250)   # Lavender
        ])
        self.length = random.randint(5, 15)
        self.thickness = random.randint(1, 3)
        
    def update(self):
        self.y += self.speed
        if self.y > WINDOW_HEIGHT:
            self.reset()
            
    def draw(self, surface):
        pygame.draw.line(
            surface, 
            self.color, 
            (self.x, self.y), 
            (self.x, self.y + self.length), 
            self.thickness
        )
            
    def reset(self):
        self.x = random.randint(0, WINDOW_WIDTH)
        self.y = random.randint(-100, -10)
        self.speed = random.uniform(2, 8)
        self.color = random.choice([
            (135, 206, 250),  # Light blue
            (144, 238, 144),  # Light green
            (255, 182, 193),  # Light pink
            (255, 255, 224),  # Light yellow
            (230, 230, 250)   # Lavender
        ])

# Create rain drops
rain_drops = [RainDrop() for _ in range(100)]

# Player properties
player_width = 40
player_height = 40
player_x = 50
player_y = WINDOW_HEIGHT - player_height - 50
player_vel_x = 0
player_vel_y = 0
player_speed = 5
player_jump = -15
gravity = 0.8
is_jumping = False

# Cat player sprites
cat_sprites = {
    "idle": pygame.Surface((player_width, player_height), pygame.SRCALPHA),
    "run": pygame.Surface((player_width, player_height), pygame.SRCALPHA),
    "jump": pygame.Surface((player_width, player_height), pygame.SRCALPHA)
}

# Draw a cat-like sprite
def create_cat_sprites():
    # Idle cat
    pygame.draw.ellipse(cat_sprites["idle"], BLUE, (0, 10, player_width, player_height-10))  # Body
    pygame.draw.ellipse(cat_sprites["idle"], BLUE, (5, 0, 15, 15))  # Head
    pygame.draw.ellipse(cat_sprites["idle"], BLUE, (20, 0, 15, 15))  # Head
    pygame.draw.ellipse(cat_sprites["idle"], (200, 200, 200), (0, player_height-10, 10, 10))  # Tail
    
    # Running cat (slight variation)
    pygame.draw.ellipse(cat_sprites["run"], BLUE, (0, 12, player_width, player_height-12))  # Body
    pygame.draw.ellipse(cat_sprites["run"], BLUE, (7, 2, 15, 15))  # Head
    pygame.draw.ellipse(cat_sprites["run"], BLUE, (22, 2, 15, 15))  # Head
    pygame.draw.ellipse(cat_sprites["run"], (200, 200, 200), (5, player_height-10, 10, 10))  # Tail
    
    # Jumping cat
    pygame.draw.ellipse(cat_sprites["jump"], BLUE, (0, 5, player_width, player_height-5))  # Body
    pygame.draw.ellipse(cat_sprites["jump"], BLUE, (5, 0, 15, 10))  # Head
    pygame.draw.ellipse(cat_sprites["jump"], BLUE, (20, 0, 15, 10))  # Head
    pygame.draw.ellipse(cat_sprites["jump"], (200, 200, 200), (5, player_height-8, 12, 8))  # Tail

create_cat_sprites()
current_sprite = "idle"

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

# Trophy properties (make it a cat toy)
trophy = {"x": 560, "y": WINDOW_HEIGHT - 450, "width": 40, "height": 40, "collected": False}

# Celebration properties
celebration_active = False
celebration_time = 0
celebration_duration = 5000  # 5 seconds
confetti_particles = []

# Confetti particle class
class Confetti:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = random.randint(5, 10)
        self.color = (
            random.randint(100, 255),
            random.randint(100, 255),
            random.randint(100, 255)
        )
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-8, -4)
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-5, 5)
        self.gravity = random.uniform(0.1, 0.3)
        self.lifetime = 100 + random.randint(0, 100)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.speed_y += self.gravity
        self.rotation += self.rotation_speed
        self.lifetime -= 1
        
    def draw(self, surface):
        if self.lifetime <= 0:
            return False
            
        # Create a rotated rectangle for the confetti
        confetti_surf = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.rect(confetti_surf, self.color, (0, 0, self.size, self.size))
        rotated = pygame.transform.rotate(confetti_surf, self.rotation)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)
        return True

# Add confetti burst function
def add_confetti_burst(x, y, amount=100):
    for _ in range(amount):
        confetti_particles.append(Confetti(x, y))

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
                current_sprite = "run"
            if event.key == K_RIGHT:
                player_vel_x = player_speed
                current_sprite = "run"
            if event.key == K_SPACE and not is_jumping:
                player_vel_y = player_jump
                is_jumping = True
                current_sprite = "jump"
        
        # Key release events
        if event.type == KEYUP:
            if event.key == K_LEFT and player_vel_x < 0:
                player_vel_x = 0
                current_sprite = "idle"
            if event.key == K_RIGHT and player_vel_x > 0:
                player_vel_x = 0
                current_sprite = "idle"
    
    # Update player position
    player_x += player_vel_x
    player_y += player_vel_y
    
    # Apply gravity
    player_vel_y += gravity
    
    # Update parallax effect based on player movement
    if player_vel_x != 0:
        parallax_offset += player_vel_x * 0.1
        parallax_offset %= WINDOW_WIDTH
    
    # Update rain drops
    for drop in rain_drops:
        drop.update()
    
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
            if current_sprite == "jump":
                current_sprite = "idle"
    
    # Check boundaries
    if player_x < 0:
        player_x = 0
    if player_x + player_width > WINDOW_WIDTH:
        player_x = WINDOW_WIDTH - player_width
    if player_y + player_height > WINDOW_HEIGHT:
        player_y = WINDOW_HEIGHT - player_height
        player_vel_y = 0
        is_jumping = False
        if current_sprite == "jump":
            current_sprite = "idle"
    
    # Check trophy collection
    if (not trophy["collected"] and 
        player_x + player_width > trophy["x"] and
        player_x < trophy["x"] + trophy["width"] and
        player_y + player_height > trophy["y"] and
        player_y < trophy["y"] + trophy["height"]):
        trophy["collected"] = True
        celebration_active = True
        celebration_time = pygame.time.get_ticks()
        # Add initial confetti bursts when trophy is collected
        for _ in range(5):
            add_confetti_burst(
                random.randint(0, WINDOW_WIDTH),
                random.randint(0, WINDOW_HEIGHT // 2),
                100
            )
    
    # Draw everything
    DISPLAYSURF.fill(GRAY)
    
    # Draw parallax cat background
    if cat_image:
        # Draw the cat image in two positions for seamless scrolling
        DISPLAYSURF.blit(cat_image, (-parallax_offset, 0))
        DISPLAYSURF.blit(cat_image, (WINDOW_WIDTH - parallax_offset, 0))
        
        # Apply a semi-transparent overlay for better visibility
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(GRAY)
        overlay.set_alpha(100)
        DISPLAYSURF.blit(overlay, (0, 0))
    
    # Draw digital rain effect
    for drop in rain_drops:
        drop.draw(DISPLAYSURF)
    
    # Draw platforms with a more skeuomorphic look
    for platform in platforms:
        # Draw platform with a 3D effect
        pygame.draw.rect(DISPLAYSURF, GREEN, 
                         (platform["x"], platform["y"], platform["width"], platform["height"]))
        # Add highlight at the top
        pygame.draw.line(DISPLAYSURF, (180, 230, 180), 
                         (platform["x"], platform["y"]), 
                         (platform["x"] + platform["width"], platform["y"]), 2)
        # Add shadow at the bottom
        pygame.draw.line(DISPLAYSURF, (90, 150, 90), 
                         (platform["x"], platform["y"] + platform["height"]), 
                         (platform["x"] + platform["width"], platform["y"] + platform["height"]), 2)
    
    # Draw player as a cat sprite
    DISPLAYSURF.blit(cat_sprites[current_sprite], (player_x, player_y))
    
    # Draw trophy if not collected (as a cat toy)
    if not trophy["collected"]:
        # Draw a cat toy (mouse)
        pygame.draw.ellipse(DISPLAYSURF, (150, 150, 150), 
                           (trophy["x"], trophy["y"], trophy["width"], trophy["height"] * 0.7))
        # Ears
        pygame.draw.circle(DISPLAYSURF, (150, 150, 150), 
                          (trophy["x"] + 10, trophy["y"]), 8)
        pygame.draw.circle(DISPLAYSURF, (150, 150, 150), 
                          (trophy["x"] + trophy["width"] - 10, trophy["y"]), 8)
        # Tail
        pygame.draw.line(DISPLAYSURF, (150, 150, 150), 
                        (trophy["x"] + trophy["width"] // 2, trophy["y"] + trophy["height"] * 0.7),
                        (trophy["x"] + trophy["width"] // 2 + 15, trophy["y"] + trophy["height"]), 3)
    
    # Handle celebration
    if celebration_active:
        # Draw a darkened overlay for the alert effect
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(BLACK)
        overlay.set_alpha(150)
        DISPLAYSURF.blit(overlay, (0, 0))
        
        # Create container for the celebration message
        container_width = 600
        container_height = 400
        container_x = (WINDOW_WIDTH - container_width) // 2
        container_y = (WINDOW_HEIGHT - container_height) // 2
        
        # Draw container with a skeuomorphic look
        pygame.draw.rect(DISPLAYSURF, (80, 80, 100), 
                         (container_x, container_y, container_width, container_height), 
                         border_radius=20)
        
        # Add a highlight effect at the top and left edges
        pygame.draw.line(DISPLAYSURF, (100, 100, 120), 
                        (container_x + 5, container_y + 5), 
                        (container_x + container_width - 5, container_y + 5), 
                        3)
        pygame.draw.line(DISPLAYSURF, (100, 100, 120), 
                        (container_x + 5, container_y + 5), 
                        (container_x + 5, container_y + container_height - 5), 
                        3)
        
        # Add a shadow effect at the bottom and right edges
        pygame.draw.line(DISPLAYSURF, (60, 60, 80), 
                        (container_x + 5, container_y + container_height - 5), 
                        (container_x + container_width - 5, container_y + container_height - 5), 
                        3)
        pygame.draw.line(DISPLAYSURF, (60, 60, 80), 
                        (container_x + container_width - 5, container_y + 5), 
                        (container_x + container_width - 5, container_y + container_height - 5), 
                        3)
        
        # Draw Olive cat sprites as decorative elements around the container
        current_time = pygame.time.get_ticks()
        for i in range(12):
            angle = (i * 30 + current_time // 50) % 360
            radius = 250
            x = WINDOW_WIDTH // 2 + int(radius * math.cos(angle * 0.0174533))
            y = WINDOW_HEIGHT // 2 + int(radius * math.sin(angle * 0.0174533))
            
            # Create rainbow-colored tint effect that changes over time
            hue = (i * 30 + current_time // 30) % 360
            r = int(abs(math.sin(hue * 0.0174533)) * 255)
            g = int(abs(math.sin((hue + 120) * 0.0174533)) * 255)
            b = int(abs(math.sin((hue + 240) * 0.0174533)) * 255)
            
            # Calculate rotation angle for the sprite
            rotation = (angle + current_time // 100) % 360
            
            # Draw the Olive cat sprite with rotation
            if olive_cat_image:
                # Create a copy of the image for rotation
                rotated_image = pygame.transform.rotate(olive_cat_image, rotation)
                # Create a colored overlay
                colored_overlay = pygame.Surface(rotated_image.get_size(), pygame.SRCALPHA)
                colored_overlay.fill((r, g, b, 100))  # Semi-transparent color
                # Apply the overlay
                rotated_image.blit(colored_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                # Get the rect for positioning
                img_rect = rotated_image.get_rect(center=(x, y))
                # Draw the image
                DISPLAYSURF.blit(rotated_image, img_rect)
            else:
                # Fallback if image loading failed
                size = 20
                pygame.draw.circle(DISPLAYSURF, (r, g, b), (x, y), size)
        
        # Display thank you message with a more elegant style
        font = pygame.font.Font(None, 42)
        shadow_offset = 2
        
        lines = [
            "Ariel,",
            "thank you for being an incredible team member",
            "(and for bringing Olive to all of our meetings)."
        ]
        
        for i, line in enumerate(lines):
            # Draw text shadow
            shadow_text = font.render(line, True, (30, 30, 30))
            shadow_rect = shadow_text.get_rect(center=(WINDOW_WIDTH // 2 + shadow_offset, container_y + 120 + i * 45 + shadow_offset))
            DISPLAYSURF.blit(shadow_text, shadow_rect)
            
            # Draw text
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, container_y + 120 + i * 45))
            DISPLAYSURF.blit(text, text_rect)
        
        # Draw buttons
        button_font = pygame.font.Font(None, 32)
        button_width = 180
        button_height = 50
        
        # Restart button
        restart_button = pygame.Rect(
            container_x + container_width // 4 - button_width // 2,
            container_y + container_height - 80,
            button_width,
            button_height
        )
        
        # Confetti button
        confetti_button = pygame.Rect(
            container_x + container_width * 3 // 4 - button_width // 2,
            container_y + container_height - 80,
            button_width,
            button_height
        )
        
        # Draw buttons with custom styling
        # Restart button - black with white text
        pygame.draw.rect(DISPLAYSURF, BLACK, restart_button, border_radius=10)
        
        # Button highlight (top and left)
        pygame.draw.line(DISPLAYSURF, (80, 80, 80), 
                        (restart_button.x + 3, restart_button.y + 3),
                        (restart_button.x + restart_button.width - 3, restart_button.y + 3), 
                        2)
        pygame.draw.line(DISPLAYSURF, (80, 80, 80), 
                        (restart_button.x + 3, restart_button.y + 3),
                        (restart_button.x + 3, restart_button.y + restart_button.height - 3), 
                        2)
        
        # Button shadow (bottom and right)
        pygame.draw.line(DISPLAYSURF, (40, 40, 40), 
                        (restart_button.x + 3, restart_button.y + restart_button.height - 3),
                        (restart_button.x + restart_button.width - 3, restart_button.y + restart_button.height - 3), 
                        2)
        pygame.draw.line(DISPLAYSURF, (40, 40, 40), 
                        (restart_button.x + restart_button.width - 3, restart_button.y + 3),
                        (restart_button.x + restart_button.width - 3, restart_button.y + restart_button.height - 3), 
                        2)
        
        # Restart button text (white)
        restart_text_surf = button_font.render("Restart", True, WHITE)
        restart_text_rect = restart_text_surf.get_rect(center=restart_button.center)
        DISPLAYSURF.blit(restart_text_surf, restart_text_rect)
        
        # Confetti button - multi-color changing
        current_time = pygame.time.get_ticks()
        
        # Create gradient background for confetti button
        for i in range(confetti_button.width):
            hue = (current_time // 20 + i * 2) % 360
            r = int(abs(math.sin(hue * 0.0174533)) * 255)
            g = int(abs(math.sin((hue + 120) * 0.0174533)) * 255)
            b = int(abs(math.sin((hue + 240) * 0.0174533)) * 255)
            pygame.draw.line(
                DISPLAYSURF, 
                (r, g, b), 
                (confetti_button.x + i, confetti_button.y),
                (confetti_button.x + i, confetti_button.y + confetti_button.height),
                1
            )
        
        # Border for confetti button
        pygame.draw.rect(DISPLAYSURF, WHITE, confetti_button, width=2, border_radius=10)
        
        # Create animated/moving text for confetti button
        confetti_text = "Confetti!"
        text_offset = int(math.sin(current_time * 0.01) * 5)
        
        # Render each letter with its own color and position
        text_width = button_font.size(confetti_text)[0]
        start_x = confetti_button.centerx - text_width // 2
        
        for i, letter in enumerate(confetti_text):
            letter_hue = (current_time // 50 + i * 30) % 360
            letter_r = int(abs(math.sin(letter_hue * 0.0174533)) * 255)
            letter_g = int(abs(math.sin((letter_hue + 120) * 0.0174533)) * 255)
            letter_b = int(abs(math.sin((letter_hue + 240) * 0.0174533)) * 255)
            
            # Calculate vertical offset for each letter (wave effect)
            y_offset = int(math.sin((current_time * 0.01) + (i * 0.5)) * 5)
            
            letter_surf = button_font.render(letter, True, (letter_r, letter_g, letter_b))
            letter_rect = letter_surf.get_rect()
            letter_rect.x = start_x + button_font.size(confetti_text[:i])[0]
            letter_rect.y = confetti_button.centery - letter_rect.height // 2 + y_offset
            
            DISPLAYSURF.blit(letter_surf, letter_rect)
        
        # Check for button clicks
        mouse_pos = pygame.mouse.get_pos()
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        if mouse_clicked:
            if restart_button.collidepoint(mouse_pos):
                # Reset game
                player_x = 50
                player_y = WINDOW_HEIGHT - player_height - 50
                player_vel_x = 0
                player_vel_y = 0
                is_jumping = False
                trophy["collected"] = False
                celebration_active = False
                confetti_particles.clear()
            
            elif confetti_button.collidepoint(mouse_pos):
                # Add confetti burst
                add_confetti_burst(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, 200)
        
        # Auto-generate initial confetti when celebration starts
        if pygame.time.get_ticks() - celebration_time < 100:
            for i in range(5):
                add_confetti_burst(
                    random.randint(0, WINDOW_WIDTH),
                    random.randint(0, WINDOW_HEIGHT // 3),
                    50
                )
    
        # Update and draw confetti particles
        for particle in confetti_particles[:]:
            particle.update()
            if not particle.draw(DISPLAYSURF):
                confetti_particles.remove(particle)
    
    # Update display
    pygame.display.update()
    clock.tick(FPS)
