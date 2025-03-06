
import pygame
import os

def load_olive_cat_image():
    # Try multiple possible paths for the olive cat image
    possible_paths = [
        "olive_cat.png",
        os.path.join("attached_assets", "olive_cat.png"),
        os.path.join(".", "olive_cat.png")
    ]
    
    for cat_path in possible_paths:
        if os.path.exists(cat_path):
            try:
                # Load and scale the image
                original_img = pygame.image.load(cat_path)
                # Return a scaled version for the rotating sprites
                return pygame.transform.scale(original_img, (40, 40))
            except pygame.error:
                print(f"Error loading Olive cat image from {cat_path}")
                continue
    
    print("Olive cat image not found in any of the expected locations")
    
    # Create a more cat-like fallback image
    fallback = pygame.Surface((40, 40), pygame.SRCALPHA)
    # Cat head background
    pygame.draw.circle(fallback, (229, 186, 115), (20, 20), 18)  # Light orange/brown
    # Cat eyes
    pygame.draw.ellipse(fallback, (70, 160, 70), (12, 15, 6, 8))  # Left eye
    pygame.draw.ellipse(fallback, (70, 160, 70), (22, 15, 6, 8))  # Right eye
    # Cat ears
    pygame.draw.polygon(fallback, (200, 150, 100), [(10, 8), (15, 2), (20, 8)])  # Left ear
    pygame.draw.polygon(fallback, (200, 150, 100), [(20, 8), (25, 2), (30, 8)])  # Right ear
    # Cat nose
    pygame.draw.polygon(fallback, (200, 100, 100), [(18, 22), (20, 24), (22, 22)])
    
    return fallback
