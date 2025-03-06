
import pygame
import os

def load_cat_image():
    cat_path = os.path.join("Game", "Assets", "IMG_6816.png")
    if os.path.exists(cat_path):
        try:
            # Load and scale the image
            original_img = pygame.image.load(cat_path)
            return pygame.transform.scale(original_img, (800, 600))
        except pygame.error:
            print(f"Error loading cat image from {cat_path}")
    else:
        print(f"Cat image not found at {cat_path}")
    
    # Create a fallback image with a simple pattern
    fallback = pygame.Surface((800, 600))
    fallback.fill((30, 30, 50))  # Dark background
    
    # Add some pattern
    for x in range(0, 800, 40):
        for y in range(0, 600, 40):
            if (x // 40 + y // 40) % 2 == 0:
                pygame.draw.rect(fallback, (50, 50, 70), (x, y, 20, 20))
    
    return fallback
