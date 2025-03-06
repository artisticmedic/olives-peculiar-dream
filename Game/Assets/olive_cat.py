
import pygame
import os

def load_olive_cat_image():
    olive_path = os.path.join("Game", "Assets", "olive_cat.png")
    if os.path.exists(olive_path):
        try:
            return pygame.image.load(olive_path)
        except pygame.error:
            print(f"Error loading olive cat from {olive_path}")
    
    # Fallback: create a simple cat
    fallback = pygame.Surface((40, 40), pygame.SRCALPHA)
    fallback.fill((0, 0, 0, 0))  # Transparent
    
    # Draw a simple cat shape
    pygame.draw.ellipse(fallback, (200, 180, 120), (5, 5, 30, 25))  # Head
    pygame.draw.polygon(fallback, (200, 180, 120), [(15, 5), (20, 0), (25, 5)])  # Left ear
    pygame.draw.polygon(fallback, (200, 180, 120), [(25, 5), (30, 0), (35, 5)])  # Right ear
    pygame.draw.circle(fallback, (50, 100, 50), (15, 15), 3)  # Left eye
    pygame.draw.circle(fallback, (50, 100, 50), (25, 15), 3)  # Right eye
    pygame.draw.ellipse(fallback, (255, 150, 150), (18, 20, 4, 3))  # Nose
    
    return fallback
