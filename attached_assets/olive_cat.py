
import pygame
import os

def load_olive_cat_image():
    cat_path = os.path.join("olive_cat.png")
    if os.path.exists(cat_path):
        try:
            # Load and scale the image
            original_img = pygame.image.load(cat_path)
            # Return a scaled version for the rotating sprites
            return pygame.transform.scale(original_img, (40, 40))
        except pygame.error:
            print(f"Error loading Olive cat image from {cat_path}")
    else:
        print(f"Olive cat image not found at {cat_path}")
    
    # Create a fallback image
    fallback = pygame.Surface((40, 40), pygame.SRCALPHA)
    fallback.fill((200, 200, 200, 200))
    pygame.draw.circle(fallback, (150, 150, 150), (20, 20), 15)
    
    return fallback
