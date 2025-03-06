import pygame
import sys
import random
import os
import math
from pygame.locals import *
from Game.Assets.cat_image import load_cat_image
from Game.Assets.olive_cat import load_olive_cat_image

# Initialize pygame with optimized settings
pygame.init()

# Set up display with hardware acceleration and double buffering
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
DISPLAYSURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.HWSURFACE | pygame.DOUBLEBUF)
pygame.display.set_caption('Olive\'s Peculiar Dream')
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, pygame.MOUSEBUTTONDOWN])  # Only process necessary events

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

# Load cat background
cat_image = load_cat_image()
parallax_offset = 0

# Digital rain toggle
rain_enabled = False  # Default off
rain_toggle_rect = pygame.Rect(20, 20, 40, 40)

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

# Speech bubble properties
speech_bubble = {
    "active": True,
    "text": "Pst! Up here!",
    "timer": 0,
    "duration": 2000,  # How long to display each part of text
    "char_index": 0,
    "offset_x": 0,
    "offset_y": 0
}

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

# Camera properties
camera_offset_x = 0

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

# Kibble properties
kibbles = [
    {"x": 250, "y": WINDOW_HEIGHT - 150, "radius": 8, "collected": False, "color": (255, 200, 100)},
    {"x": 350, "y": WINDOW_HEIGHT - 220, "radius": 8, "collected": False, "color": (255, 180, 80)},
    {"x": 430, "y": WINDOW_HEIGHT - 290, "radius": 8, "collected": False, "color": (255, 160, 60)},
    {"x": 510, "y": WINDOW_HEIGHT - 360, "radius": 8, "collected": False, "color": (255, 140, 40)},
    {"x": 300, "y": WINDOW_HEIGHT - 80, "radius": 8, "collected": False, "color": (255, 120, 20)},
]
kibble_count = 0
kibble_message = {"active": False, "text": "", "timer": 0, "duration": 1000}
kibble_messages = ["Yum!", "Mmm!", "Tasty!", "Meow!", "Delicious!"]

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
        self.type = random.choice(["square", "ribbon", "circle", "star"])
        self.size = random.randint(6, 12)  # Larger size

        # More vibrant colors
        bright_colors = [
            (255, 0, 0),      # Red
            (255, 165, 0),    # Orange
            (255, 255, 0),    # Yellow
            (0, 255, 0),      # Green
            (0, 255, 255),    # Cyan
            (0, 0, 255),      # Blue
            (255, 0, 255),    # Magenta
            (255, 20, 147),   # Pink
            (255, 215, 0),    # Gold
            (138, 43, 226)    # Purple
        ]
        self.color = random.choice(bright_colors)

        self.speed_x = random.uniform(-4, 4)  # More horizontal movement
        self.speed_y = random.uniform(-10, -5)  # Higher initial velocity
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-8, 8)  # Faster rotation
        self.gravity = random.uniform(0.1, 0.25)
        self.lifetime = 150 + random.randint(0, 100)  # Longer lifetime
        self.wave_offset = random.uniform(0, 2 * math.pi)  # For ribbon movement
        self.wave_speed = random.uniform(0.05, 0.15)

    def update(self):
        self.x += self.speed_x

        # Add some waviness to ribbons
        if self.type == "ribbon":
            self.x += math.sin(self.wave_offset + pygame.time.get_ticks() * self.wave_speed) * 0.5

        self.y += self.speed_y
        self.speed_y += self.gravity
        self.rotation += self.rotation_speed
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime <= 0:
            return False

        # Calculate alpha for fade out near end of lifetime
        alpha = min(255, self.lifetime * 2)

        # Create a rotated shape based on type
        confetti_surf = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)

        if self.type == "square":
            # Square confetti
            pygame.draw.rect(confetti_surf, self.color + (alpha,), (self.size/2, self.size/2, self.size, self.size))

        elif self.type == "ribbon":
            # Ribbon (longer rectangle)
            ribbon_length = self.size * 4
            pygame.draw.rect(confetti_surf, self.color + (alpha,), 
                            (self.size/2, self.size - ribbon_length/2, self.size/2, ribbon_length))

        elif self.type == "circle":
            # Circle confetti
            pygame.draw.circle(confetti_surf, self.color + (alpha,), (self.size, self.size), self.size/2)

        elif self.type == "star":
            # Star confetti (simplified)
            points = []
            for i in range(5):
                # Outer points
                angle = math.pi * 2 * i / 5 - math.pi / 2
                points.append((self.size + math.cos(angle) * self.size, 
                               self.size + math.sin(angle) * self.size))
                # Inner points
                angle += math.pi / 5
                points.append((self.size + math.cos(angle) * (self.size/2), 
                               self.size + math.sin(angle) * (self.size/2)))
            pygame.draw.polygon(confetti_surf, self.color + (alpha,), points)

        rotated = pygame.transform.rotate(confetti_surf, self.rotation)
        rect = rotated.get_rect(center=(self.x, self.y))
        surface.blit(rotated, rect)
        return True

# Add confetti burst function
def add_confetti_burst(x, y, amount=100):
    for _ in range(amount):
        confetti_particles.append(Confetti(x, y))

# Delta time for frame-independent movement
last_time = pygame.time.get_ticks()

#World width calculation.  This needs to be calculated dynamically based on the level generation
world_width = WINDOW_WIDTH

# Main game loop
while True:
    # Calculate delta time for smoother movement regardless of framerate
    current_time = pygame.time.get_ticks()
    dt = (current_time - last_time) / 1000.0  # Convert to seconds
    last_time = current_time

    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Mouse click events
        if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
            mouse_pos = pygame.mouse.get_pos()

            # Check if rain toggle button was clicked
            if rain_toggle_rect.collidepoint(mouse_pos):
                rain_enabled = not rain_enabled

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

    # Update player position with delta time for consistent movement speed
    player_x += player_vel_x * dt * 60  # Scale by target 60 FPS
    player_y += player_vel_y * dt * 60

    # Apply gravity with delta time
    player_vel_y += gravity * dt * 60

    # Update camera position (centered on player horizontally)
    if player_x > WINDOW_WIDTH / 2 and player_x < world_width - WINDOW_WIDTH / 2:
        camera_offset_x = player_x - WINDOW_WIDTH / 2
    elif player_x >= world_width - WINDOW_WIDTH / 2:
        camera_offset_x = world_width - WINDOW_WIDTH
    else:
        camera_offset_x = 0

    # Update parallax effect based on player movement
    if player_vel_x != 0:
        parallax_offset += player_vel_x * 0.1 * dt * 60
        parallax_offset %= WINDOW_WIDTH

    # Update rain drops
    for drop in rain_drops:
        drop.update()

    # Check kibble collection using rectangle-based collision for better performance
    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    for kibble in kibbles:
        if not kibble["collected"]:
            # Create a rectangle around the kibble
            kibble_rect = pygame.Rect(
                kibble["x"] - kibble["radius"], 
                kibble["y"] - kibble["radius"],
                kibble["radius"] * 2, 
                kibble["radius"] * 2
            )

            if player_rect.colliderect(kibble_rect):
                kibble["collected"] = True
                kibble_count += 1
                # Show a random message
                kibble_message["active"] = True
                kibble_message["text"] = random.choice(kibble_messages)
                kibble_message["timer"] = pygame.time.get_ticks()

    # Update kibble message timing
    if kibble_message["active"] and pygame.time.get_ticks() - kibble_message["timer"] > kibble_message["duration"]:
        kibble_message["active"] = False

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
    if player_x + player_width > world_width:
        player_x = world_width - player_width
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
        DISPLAYSURF.blit(cat_image, (-parallax_offset - camera_offset_x, 0))
        DISPLAYSURF.blit(cat_image, (WINDOW_WIDTH - parallax_offset - camera_offset_x, 0))

        # Apply a semi-transparent overlay for better visibility
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        overlay.fill(GRAY)
        overlay.set_alpha(100)
        DISPLAYSURF.blit(overlay, (0, 0))

    # Draw digital rain effect if enabled
    if rain_enabled:
        for drop in rain_drops:
            drop.draw(DISPLAYSURF)

    # Draw rain toggle button with text
    # Make the button wider to accommodate text
    rain_toggle_rect = pygame.Rect(20, 20, 100, 40)
    pygame.draw.rect(DISPLAYSURF, (40, 40, 60), rain_toggle_rect, border_radius=10)
    pygame.draw.rect(DISPLAYSURF, (100, 100, 120), rain_toggle_rect, width=2, border_radius=10)

    # Create text for the toggle
    toggle_font = pygame.font.Font(None, 24)
    if rain_enabled:
        toggle_text = "Rain: ON"
        toggle_bg_color = (100, 200, 255)
        toggle_text_color = (20, 20, 80)
    else:
        toggle_text = "Rain: OFF"
        toggle_bg_color = (60, 60, 80)
        toggle_text_color = (200, 200, 220)

    # Draw toggle background with color based on state
    pygame.draw.rect(DISPLAYSURF, toggle_bg_color, rain_toggle_rect, border_radius=10)
    pygame.draw.rect(DISPLAYSURF, (100, 100, 120), rain_toggle_rect, width=2, border_radius=10)

    # Draw toggle text
    text_surface = toggle_font.render(toggle_text, True, toggle_text_color)
    text_rect = text_surface.get_rect(center=rain_toggle_rect.center)
    DISPLAYSURF.blit(text_surface, text_rect)

    # Draw kibble counter
    kibble_font = pygame.font.Font(None, 32)
    # Draw container background
    kibble_rect = pygame.Rect(WINDOW_WIDTH - 120, 20, 100, 40)
    pygame.draw.rect(DISPLAYSURF, (40, 40, 60), kibble_rect, border_radius=10)
    pygame.draw.rect(DISPLAYSURF, (100, 100, 120), kibble_rect, width=2, border_radius=10)

    # Add a kibble icon
    pygame.draw.circle(DISPLAYSURF, (255, 160, 60), (WINDOW_WIDTH - 100, 40), 8)
    pygame.draw.circle(DISPLAYSURF, (200, 120, 40), (WINDOW_WIDTH - 100, 40), 8, width=1)

    # Draw kibble count
    count_text = kibble_font.render(f"x {kibble_count}", True, (220, 220, 220))
    DISPLAYSURF.blit(count_text, (WINDOW_WIDTH - 80, 31))

    # Draw platforms with a more skeuomorphic look
    for platform in platforms:
        # Draw platform with a 3D effect
        pygame.draw.rect(DISPLAYSURF, GREEN, 
                         (platform["x"] - camera_offset_x, platform["y"], platform["width"], platform["height"]))
        # Add highlight at the top
        pygame.draw.line(DISPLAYSURF, (180, 230, 180), 
                         (platform["x"] - camera_offset_x, platform["y"]), 
                         (platform["x"] + platform["width"] - camera_offset_x, platform["y"]), 2)
        # Add shadow at the bottom
        pygame.draw.line(DISPLAYSURF, (90, 150, 90), 
                         (platform["x"] - camera_offset_x, platform["y"] + platform["height"]), 
                         (platform["x"] + platform["width"] - camera_offset_x, platform["y"] + platform["height"]), 2)

    # Draw kibbles - with pre-calculated time values for better performance
    current_time = pygame.time.get_ticks()
    sin_value = math.sin(current_time * 0.01) * 2

    for kibble in kibbles:
        if not kibble["collected"]:
            # Adjust for camera position
            screen_x = kibble["x"] - camera_offset_x

            # Draw kibble as a small circle with slight glow effect
            glow_radius = kibble["radius"] + 2 + sin_value

            # Only create and draw glow if on screen (optimization)
            if (0 <= screen_x <= WINDOW_WIDTH and 0 <= kibble["y"] <= WINDOW_HEIGHT):
                glow_color = (kibble["color"][0], kibble["color"][1]//2, kibble["color"][2]//4, 150)
                glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
                DISPLAYSURF.blit(glow_surf, (screen_x-glow_radius, kibble["y"]-glow_radius))

                # Main kibble
                pygame.draw.circle(DISPLAYSURF, kibble["color"], (screen_x, kibble["y"]), kibble["radius"])
                # Shine effect
                pygame.draw.circle(DISPLAYSURF, (255, 255, 200), 
                                (screen_x-2, kibble["y"]-2), 2)

    # Draw player as a cat sprite
    DISPLAYSURF.blit(cat_sprites[current_sprite], (player_x - camera_offset_x, player_y))

    # Draw player speech bubble when collecting kibble
    if kibble_message["active"]:
        # Position above player
        bubble_x = player_x + player_width // 2 - 30 - camera_offset_x
        bubble_y = player_y - 40

        # Draw the speech bubble
        pygame.draw.ellipse(DISPLAYSURF, WHITE, 
                           (bubble_x, bubble_y, 60, 30))
        pygame.draw.ellipse(DISPLAYSURF, BLACK, 
                           (bubble_x, bubble_y, 60, 30), 2)

        # Draw pointer to player
        pointer_points = [
            (bubble_x + 20, bubble_y + 30),
            (bubble_x + 10, bubble_y + 40),
            (bubble_x + 30, bubble_y + 30)
        ]
        pygame.draw.polygon(DISPLAYSURF, WHITE, pointer_points)
        pygame.draw.polygon(DISPLAYSURF, BLACK, pointer_points, 2)

        # Draw text
        font = pygame.font.Font(None, 20)
        text_surface = font.render(kibble_message["text"], True, BLACK)
        text_rect = text_surface.get_rect(center=(bubble_x + 30, bubble_y + 15))
        DISPLAYSURF.blit(text_surface, text_rect)

    # Draw trophy if not collected (as a cat toy)
    trophy_screen_x = trophy["x"] - camera_offset_x
    if not trophy["collected"]:
        # Draw a cat toy (mouse)
        pygame.draw.ellipse(DISPLAYSURF, (150, 150, 150), 
                           (trophy_screen_x, trophy["y"], trophy["width"], trophy["height"] * 0.7))
        # Ears
        pygame.draw.circle(DISPLAYSURF, (150, 150, 150), 
                          (trophy_screen_x + 10, trophy["y"]), 8)
        pygame.draw.circle(DISPLAYSURF, (150, 150, 150), 
                          (trophy_screen_x + trophy["width"] - 10, trophy["y"]), 8)
        # Tail
        pygame.draw.line(DISPLAYSURF, (150, 150, 150), 
                        (trophy_screen_x + trophy["width"] // 2, trophy["y"] + trophy["height"] * 0.7),
                        (trophy_screen_x + trophy["width"] // 2 + 15, trophy["y"] + trophy["height"]), 3)

        # Draw speech bubble for the mouse
        if speech_bubble["active"] and (0 <= trophy_screen_x <= WINDOW_WIDTH):
            # Update speech bubble movement
            current_time = pygame.time.get_ticks()
            speech_bubble["offset_x"] = math.sin(current_time * 0.005) * 3
            speech_bubble["offset_y"] = math.cos(current_time * 0.003) * 2

            # Position of speech bubble (adjust for camera)
            bubble_x = trophy_screen_x + trophy["width"] + 5 + speech_bubble["offset_x"]
            bubble_y = trophy["y"] - 50 + speech_bubble["offset_y"]

            # Progress the text animation
            if current_time - speech_bubble["timer"] > 100:  # Control character reveal speed
                speech_bubble["timer"] = current_time
                if speech_bubble["char_index"] < len(speech_bubble["text"]):
                    speech_bubble["char_index"] += 1

            # Current text to display
            current_text = speech_bubble["text"][:speech_bubble["char_index"]]

            if current_text:
                # Draw the speech bubble
                font = pygame.font.Font(None, 24)
                text_surface = font.render(current_text, True, BLACK)
                text_rect = text_surface.get_rect()

                # Make bubble size fit text
                padding = 10
                bubble_width = text_rect.width + padding * 2
                bubble_height = text_rect.height + padding * 2

                # Draw bubble background
                pygame.draw.ellipse(DISPLAYSURF, WHITE, 
                                   (bubble_x, bubble_y, bubble_width, bubble_height))
                pygame.draw.ellipse(DISPLAYSURF, BLACK, 
                                   (bubble_x, bubble_y, bubble_width, bubble_height), 2)

                # Draw pointer to mouse
                pointer_points = [
                    (bubble_x + 10, bubble_y + bubble_height - 5),
                    (bubble_x - 5, bubble_y + bubble_height + 10),
                    (bubble_x + 20, bubble_y + bubble_height)
                ]
                pygame.draw.polygon(DISPLAYSURF, WHITE, pointer_points)
                pygame.draw.polygon(DISPLAYSURF, BLACK, pointer_points, 2)

                # Draw text
                DISPLAYSURF.blit(text_surface, 
                              (bubble_x + padding, bubble_y + padding))

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

        # Draw container shadow first (pure black with offset)
        pygame.draw.rect(DISPLAYSURF, (0, 0, 0), 
                         (container_x + 4, container_y + 4, container_width, container_height), 
                         border_radius=30)  # More rounded corners

        # Draw container with a skeuomorphic look (on top of shadow)
        pygame.draw.rect(DISPLAYSURF, (85, 85, 105), 
                         (container_x, container_y, container_width, container_height), 
                         border_radius=30)  # More rounded corners

        # Add a highlight effect at the top and left edges (softer glow)
        pygame.draw.line(DISPLAYSURF, (110, 110, 130), 
                        (container_x + 15, container_y + 15), 
                        (container_x + container_width - 15, container_y + 15), 
                        4)
        pygame.draw.line(DISPLAYSURF, (110, 110, 130), 
                        (container_x + 15, container_y + 15), 
                        (container_x + 15, container_y + container_height - 15), 
                        4)

        # Add an inner border glow
        pygame.draw.rect(DISPLAYSURF, (100, 100, 120), 
                        (container_x + 8, container_y + 8, container_width - 16, container_height - 16), 
                        width=2, border_radius=25)

        # Draw Olive cat images as decorative elements around the container
        current_time = pygame.time.get_ticks()
        # Load the olive cat image once
        olive_cat_img = load_olive_cat_image()

        for i in range(12):
            angle = (i * 30 + current_time // 50) % 360
            radius = 250
            x = WINDOW_WIDTH // 2 + int(radius * math.cos(angle * 0.0174533))
            y = WINDOW_HEIGHT // 2 + int(radius * math.sin(angle * 0.0174533))

            # Create rotating Olive images with rainbow effects - optimized
            rotation = (angle + current_time // 20) % 360
            # Use fewer scale values (just 3 instead of continuous)
            scale_index = int((current_time * 0.001 + i * 0.5) % 3)
            # Reduced scales to 1/3 of original size
            scales = [0.23, 0.28, 0.33]  # Pre-computed scales (1/3 of original)
            scale = scales[scale_index]

            # Use a cache for rotated images to avoid expensive transforms
            # Simple caching mechanism - 12 angles (30 degree increments) x 3 scales = 36 images max
            cache_key = f"{rotation//10}_{scale_index}"

            # Create the cache if it doesn't exist
            if not hasattr(load_olive_cat_image, 'cache'):
                load_olive_cat_image.cache = {}

            if cache_key not in load_olive_cat_image.cache:
                rotated_cat = pygame.transform.rotozoom(olive_cat_img, rotation, scale)
                load_olive_cat_image.cache[cache_key] = rotated_cat
            else:
                rotated_cat = load_olive_cat_image.cache[cache_key]

            rect = rotated_cat.get_rect(center=(x, y))

            # Simplified color calculations - fewer trig functions
            # Pre-calculated color table (12 colors for the 12 positions)
            r = (i * 20 + current_time // 30) % 255
            g = (i * 20 + 85 + current_time // 30) % 255
            b = (i * 20 + 170 + current_time // 30) % 255

            # Apply colored overlay with alpha blending
            DISPLAYSURF.blit(rotated_cat, rect, special_flags=pygame.BLEND_RGB_ADD)

        # Display thank you message with a clean style (no shadows)
        font = pygame.font.Font(None, 42)

        lines = [
            "Ariel,",
            "Thank you for being an incredible",
            "team member (and for bringing",
            "Olive to all of our meetings)."
        ]

        for i, line in enumerate(lines):
            # Draw text (no shadows)
            text = font.render(line, True, WHITE)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, container_y + 120 + i * 45))
            DISPLAYSURF.blit(text, text_rect)

        # Add sparkle effects at specific locations with clusters
        current_time = pygame.time.get_ticks()

        # Define sparkle cluster positions (as requested: top-left, bottom-left, middle-right)
        sparkle_clusters = [
            # Top-left corner cluster
            [(container_x + 20, container_y + 20), 
             (container_x + 32, container_y + 15),
             (container_x + 25, container_y + 32),
             (container_x + 12, container_y + 28)],

            # Bottom-left corner cluster
            [(container_x + 20, container_y + container_height - 20),
             (container_x + 15, container_y + container_height - 35),
             (container_x + 32, container_y + container_height - 28),
             (container_x + 28, container_y + container_height - 12)],

            # Middle-right side cluster
            [(container_x + container_width - 15, container_y + container_height // 2),
             (container_x + container_width - 25, container_y + container_height // 2 - 12),
             (container_x + container_width - 20, container_y + container_height // 2 + 15),
             (container_x + container_width - 32, container_y + container_height // 2 + 5)]
        ]

        # Draw sparkle clusters with slow, gentle fade in/out effect
        for cluster_idx, cluster in enumerate(sparkle_clusters):
            # Each cluster has its own base phase offset for out-of-sync animation
            cluster_phase = cluster_idx * 2.1  # Ensure clusters are out of sync

            # Process each sparkle in the cluster
            for pos_idx, pos in enumerate(cluster):
                # Individual sparkle phase offset within cluster
                sparkle_phase = pos_idx * 0.7

                # Calculate very slow fade cycle (4-6 seconds per cycle)
                # Convert milliseconds to seconds, divide by cycle duration (4-6 seconds)
                cycle_duration = 4 + (cluster_idx + pos_idx) % 3  # 4, 5, or 6 seconds
                time_factor = (current_time / 1000 / cycle_duration + cluster_phase + sparkle_phase) % 1.0

                # Create gentle sine wave between 0 and 1 for fade effect
                fade = (math.sin(time_factor * 2 * math.pi) + 1) / 2

                # Size ratio based on position in cluster (maintain 1:3 ratio between sizes)
                size_ratio = 1.0 - (pos_idx % 3) * 0.25  # Gives ratios of 1, 0.75, 0.5

                # Only draw visible sparkles
                if fade > 0.05:  # Lower threshold to make fade more gradual
                    base_size = 6 + pos_idx % 3  # Base sizes vary between sparkles
                    size = int(base_size * size_ratio)  # Apply ratio
                    alpha = int(fade * 200)  # Max alpha 200 for gentler appearance

                    # Calculate color with gentle cycling
                    hue = (current_time / 5000 + cluster_idx * 0.3 + pos_idx * 0.1) % 1.0  # Very slow color change

                    # Convert HSV to RGB (simplified conversion)
                    if hue < 1/6:
                        r, g, b = 255, int(255 * 6 * hue), 0
                    elif hue < 2/6:
                        r, g, b = int(255 * (2 - 6 * hue)), 255, 0
                    elif hue < 3/6:
                        r, g, b = 0, 255, int(255 * 6 * (hue - 2/6))
                    elif hue < 4/6:
                        r, g, b = 0, int(255 * (4 - 6 * hue)), 255
                    elif hue < 5/6:
                        r, g, b = int(255 * 6 * (hue - 4/6)), 0, 255
                    else:
                        r, g, b = 255, 0, int(255 * (6 - 6 * hue))

                    # Make colors more pastel by adding white
                    pastel_factor = 0.7
                    r = int(r * (1 - pastel_factor) + 255 * pastel_factor)
                    g = int(g * (1 - pastel_factor) + 255 * pastel_factor)
                    b = int(b * (1 - pastel_factor) + 255 * pastel_factor)

                    # Draw a simple sparkle shape
                    sparkle_surf = pygame.Surface((size * 4, size * 4), pygame.SRCALPHA)

                    # Cross shape
                    pygame.draw.line(sparkle_surf, (r, g, b, alpha), 
                                    (size * 2, 0), (size * 2, size * 4), size // 2)
                    pygame.draw.line(sparkle_surf, (r, g, b, alpha), 
                                    (0, size * 2), (size * 4, size * 2), size // 2)

                    # X shape (diagonal lines)
                    pygame.draw.line(sparkle_surf, (r, g, b, alpha), 
                                    (size, size), (size * 3, size * 3), size // 2)
                    pygame.draw.line(sparkle_surf, (r, g, b, alpha), 
                                    (size * 3, size), (size, size * 3), size // 2)

                    # Small center glow with slightly brighter color
                    center_color = (min(r + 50, 255), min(g + 50, 255), min(b + 50, 255), alpha)
                    pygame.draw.circle(sparkle_surf, center_color, 
                                      (size * 2, size * 2), size)

                    # Apply very slow rotation for gentle twinkling effect
                    rot_angle = (current_time / 50 + cluster_idx * 30 + pos_idx * 45) % 360
                    rotated_sparkle = pygame.transform.rotate(sparkle_surf, rot_angle)
                    sparkle_rect = rotated_sparkle.get_rect(center=pos)
                    DISPLAYSURF.blit(rotated_sparkle, sparkle_rect)

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

        # Draw Restart button (black with white text) - clean version without shadows
        # Draw the black fill slightly smaller than the border
        inner_restart = pygame.Rect(
            restart_button.x + 2,
            restart_button.y + 2,
            restart_button.width - 4,
            restart_button.height - 4
        )
        pygame.draw.rect(DISPLAYSURF, BLACK, inner_restart, border_radius=8)
        pygame.draw.rect(DISPLAYSURF, WHITE, restart_button, width=2, border_radius=10)

        # Restart button text (white)
        restart_text = button_font.render("Restart", True, WHITE)
        restart_text_rect = restart_text.get_rect(center=restart_button.center)
        DISPLAYSURF.blit(restart_text, restart_text_rect)

        # Draw Confetti button with multi-color animation
        current_time = pygame.time.get_ticks()
        confetti_button_base = pygame.Surface((button_width, button_height), pygame.SRCALPHA)

        # Create gradient background for confetti button
        for i in range(button_width):
            hue = (i * 2 + current_time // 20) % 360
            r = int(abs(math.sin(hue * 0.0174533)) * 255)
            g = int(abs(math.sin((hue + 120) * 0.0174533)) * 255)
            b = int(abs(math.sin((hue + 240) * 0.0174533)) * 255)
            pygame.draw.line(confetti_button_base, (r, g, b), 
                            (i, 0), (i, button_height))

        # Add some animated "confetti" to the button background
        for _ in range(10):
            x = (current_time // 50 + random.randint(0, button_width)) % button_width
            y = (current_time // 70 + random.randint(0, button_height)) % button_height
            size = random.randint(2, 5)
            hue = (x + y + current_time // 10) % 360
            r = int(abs(math.sin(hue * 0.0174533)) * 255)
            g = int(abs(math.sin((hue + 120) * 0.0174533)) * 255)
            b = int(abs(math.sin((hue + 240) * 0.0174533)) * 255)
            pygame.draw.rect(confetti_button_base, (r, g, b), 
                            (x, y, size, size))

        # Create button content that fits within the border
        # First create the base with correct dimensions
        confetti_button_base = pygame.transform.scale(confetti_button_base, 
                                                   (confetti_button.width-4, confetti_button.height-4))

        # Apply button base to screen (positioned within the border)
        DISPLAYSURF.blit(confetti_button_base, (confetti_button.x+2, confetti_button.y+2))

        # Add button border after content
        pygame.draw.rect(DISPLAYSURF, WHITE, confetti_button, width=2, border_radius=10)

        # Create animated confetti button text (no shadow)
        confetti_text = button_font.render("Confetti!", True, WHITE)

        # Make text "bounce" slightly
        bounce_offset = int(math.sin(current_time * 0.01) * 3)

        # Calculate exact center position of the button
        text_x = confetti_button.x + confetti_button.width // 2
        text_y = confetti_button.y + confetti_button.height // 2 + bounce_offset

        # Apply main text (no shadow)
        confetti_text_rect = confetti_text.get_rect(center=(text_x, text_y))
        DISPLAYSURF.blit(confetti_text, confetti_text_rect)

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